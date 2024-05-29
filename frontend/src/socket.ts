import {reactive} from "vue"
import { io } from "socket.io-client"
import {userSignInStore} from "./components/UserSignInStore";
import {router} from "./main";
import {opponentFieldStore} from "./Pages/GameArea/components/OpponentFieldStore";
import {playerCardsStore} from "./Pages/GameArea/components/PlayerCardsStore";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
const VITE_BACKEND_SOCKETIO_SUBDIRECTORY = import.meta.env.VITE_BACKEND_SOCKETIO_SUBDIRECTORY

export const state = reactive({
    connected: false,
    numlogin: 0,
    userStore: userSignInStore,
    yourField: playerCardsStore,
    oppField: opponentFieldStore
})

const URL = import.meta.env.VITE_BACKEND_URL

export const socket = io(URL, {
    path : VITE_BACKEND_SOCKETIO_SUBDIRECTORY,
    withCredentials: true
})

socket.on("connect", () => {
    state.connected = true
})

socket.on("disconnect", () => {
    state.connected = false
})

socket.on("number logged in", (args) => {
    state.numlogin = args["data"]
})

socket.on("match request", (args) => {
    if (args["username"] == state.userStore.username) {
        router.push("/GameArea/"+args["id"]) // jump into a game
    }
})

socket.on("update your state", (args) => {
    // sends your username and your data
    if (args["username"] == state.userStore.username && args["uuid"] == state.yourField.uuid) {
        state.yourField.playersideusername = args["username"]
        if ("cardsLeft" in args) {
            state.yourField.cardsLeft = args["cardsLeft"]
        }
        if ("crisis" in args) {
            state.yourField.crisis = args["crisis"]
        }
        if ("discard" in args) {
            state.yourField.discardDeck = args["discard"]
        }
        if ("field" in args) {
            state.yourField.field = args["field"]
        }
        if ("hand" in args) {
            state.yourField.handList = args["hand"]
        }
        // notifications are specific to the person
        if ("storage" in args && args["storage"].length != 0) {
            // update all the other game logic variables (described in backend classes.py)
            state.yourField.showDialogNormal = args["storage"]["showDialogNormal"]
            state.yourField.showDialogDefence = args["storage"]["showDialogDefence"]
            state.yourField.showOptionDefence = args["storage"]["showOptionDefence"]
            state.yourField.selectionDefence = args["storage"]["selectionDefence"]
            state.yourField.showOptionDefence2 = args["storage"]["showOptionDefence2"]
            state.yourField.showOptionField = args["storage"]["showOptionField"]
            state.yourField.showDialogField = args["storage"]["showDialogField"]
            state.yourField.showDiscardPlay = args["storage"]["showDiscardPlay"]
            state.yourField.showOptionHand = args["storage"]["showOptionHand"]
            state.yourField.showDialogHand = args["storage"]["showDialogHand"]
            state.yourField.opponentHandTemp = args["storage"]["opponentHandTemp"]
            state.yourField.discardHand = args["storage"]["discardHand"]
            state.yourField.canClickEndTurn = args["storage"]["canClickEndTurn"]
            state.yourField.index = args["storage"]["index"]
            state.yourField.showForfeitButton = args["storage"]["showForfeitButton"]
            state.yourField.lastmove = args["storage"]["lastmove"]
            state.yourField.timeoutID = args["storage"]["timeoutID"]
            state.yourField.intervalID = args["storage"]["intervalID"]
        }
        if ("moveNotifier" in args) {
            state.yourField.moveNotifier =
                (args["storage"]["moveNotifier"] != undefined) ?
                    args["storage"]["moveNotifier"] + "\n(" + args["moveNotifier"] + ")" : args["moveNotifier"]
            console.log(state.yourField.moveNotifier)
        }
        if ("canClickEndTurn" in args) {
            state.yourField.canClickEndTurn = args["canClickEndTurn"]
        }
        if ("timer" in args) {
            state.yourField.timer = args["timer"]
            state.yourField.storedAccurateTimer = args["timer"]
        }
        if ("fresh" in args) {
            // new game, or (re)fresh -> reinitialise last move counter as a move was just played
            if (args["fresh"]) {
                state.yourField.lastmove = Date.now()
            }
        }
        if ("startTimer" in args) {
            if (args["startTimer"]) {
                state.yourField.startTimer()
            }
        }
    }
})

socket.on("update opponent state", (args) => {
    // sends your username but sends your opponent's data
    if (args["username"] == state.userStore.username && args["uuid"] == state.oppField.uuid) {
        if ("cardsLeft" in args) {
            state.oppField.cardsLeft = args["cardsLeft"]
        }
        if ("crisis" in args) {
            state.oppField.crisis = args["crisis"]
        }
        if ("discard" in args) {
            state.oppField.discard = args["discard"]
        }
        if ("field" in args) {
            state.oppField.field = args["field"]
        }
        // notifications are specific to the person
        if ("moveNotifier" in args) {
            state.yourField.moveNotifier = args["moveNotifier"]
        }
        if ("opponentSideUsername" in args) {
            state.oppField.opponentsideusername = args["opponentSideUsername"]
        }
        if ("gameEnd" in args) {
            state.yourField.showForfeitButton = !args["gameEnd"]
            // cleanup
            window.clearTimeout(state.yourField.timeoutID)
            window.clearInterval(state.yourField.intervalID)
            window.clearInterval(state.yourField.tickOpponentTimer)
        }
        if ("timer" in args) {
            state.oppField.timer = args["timer"]
        }
        if ("opponentDisconnected" in args) {
            state.oppField.disconnected = args["opponentDisconnected"]
        }
        if ("takeover" in args) {
            if (args["takeover"]) {
                if (args["startNow"]) {
                    let a = Date.now()
                    state.yourField.tickOpponentTimer = window.setInterval(() => {
                        state.oppField.timer = args["timer"]-(Date.now()-a)/1000
                        if (state.oppField.timer < 0) {
                            state.yourField.showDialogNormal = false // no stray dialogs
                            state.yourField.showOptionDefence = false
                            state.yourField.showDialogDefence = false
                            state.yourField.showOptionField = false
                            state.yourField.showDialogField = false
                            state.yourField.showDialogHand = false
                            state.yourField.showOptionHand = false
                            state.yourField.showDiscardPlay = false
                            state.yourField.showOptionDefence2 = false
                            state.yourField.selectionDefence = []
                            state.yourField.showForfeit = false
                            state.yourField.showForfeitButton = false

                            fetch(`${BACKEND_URL}/timeout`, {
                                method: "POST",
                                body: JSON.stringify({
                                    username: userSignInStore.username,
                                    request_username: state.oppField.opponentsideusername,
                                    game_id: state.yourField.uuid,
                                    login_session_key: userSignInStore.login_session_key(),
                                }),
                                headers: {
                                    "Content-type": "application/json; charset=UTF-8"
                                }
                            })
                                .then((response) => {
                                    if (!response.ok) return Promise.reject(response)
                                    else return response.text()
                                })
                                .then((json_text) => {
                                    let json_response = JSON.parse(json_text)

                                    // note that json response is returning opponent's move notifier
                                    // in this special case
                                    state.yourField.moveNotifier = "Your opponent ran out of time!\nYou win!"
                                    state.yourField.canClickEndTurn = json_response["canClickEndTurn"] as boolean

                                    if (json_response["winThisTurn"]) { // always true
                                        state.yourField.canClickEndTurn = false
                                    }

                                    state.yourField.discardHand = false

                                    return "Success"

                                })
                                .catch(error => {
                                    console.log(error.toString())
                                    return "Could not timeout"
                                });
                        }
                    }, 198)
                } else {
                    state.yourField.runOpponentTimerOnTurnSwitch = true
                }
            } else {
                state.yourField.runOpponentTimerOnTurnSwitch = false
                window.clearInterval(state.yourField.tickOpponentTimer)
            }
        }
    }
})

socket.on("challenge", async (args) => {
    // are we the opponent?
    if (args["opponent"] == state.userStore.username) {
        if (window.confirm(args["username"] + " has challenged you. Accept?")) {
            // yes
            let x = await fetch(`${BACKEND_URL}/accept_match`, {
                method: "POST",
                body: JSON.stringify({
                    username: state.userStore.username,
                    requested_username: args["username"],
                    login_session_key: localStorage.getItem("LoginSessionKey")
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            }).then((response) => response.json())
            if (x["status"] == "Opponent not logged in") {
                alert("Opponent is not logged in.")
            } else {
                router.push("/GameArea/"+x["id"])
            }
        } else {
            // no
            await fetch(`${BACKEND_URL}/deny_match`, {
                method: "POST",
                body: JSON.stringify({
                    username: state.userStore.username,
                    requested_username: args["username"],
                    login_session_key: localStorage.getItem("LoginSessionKey")
                }),
                headers: {
                    "Content-type": "application/json; charset=UTF-8"
                }
            })
        }
    }
})

socket.on("deny opponent", (args) => {
    // are we the opponent?
    if (args["opponent"] == state.userStore.username) {
        alert(args["username"]+" has denied your challenge.")
    }
})