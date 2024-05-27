import {defineStore} from "pinia";
import {userSignInStore} from "../../../components/UserSignInStore";
import {globalPiniaInstance} from "../../../global";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

// this store is used to store the cards currently in hand the number of cards left, and the discard deck
// this store also has action functions that pop cards from the deck in server
// cardsLeft is manually updated in the deck functions whenever a card is popped. For the most, part don't worry about it


export const playerCardsStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'playerCards',
    state: () =>({
        handList : [] as {
            name: string, enablePlay: boolean,
            requiresDialogNormal: boolean, requiresOptionDefence: boolean,
            requiresOptionField: boolean, requiresDialogHand: boolean,
            requiresOptionHand: boolean,
            warn:any
        }[],
        discardDeck : ["back-black"] as string[],
        cardsLeft : 46 as number,

        // played cards such as the crisis cards, community support and defence cards should be stored server side
        // as they need to be displayed on opponent's end too
        // local variables are to be updated and have their relevant value fetched from backend
        // whenever they're needed (e.g. get crisis card at the start of a game, played cards before every turn)
        crisis : "back-white" as string,
        // field consists of defences & community supports in play
        field: ["military-1","military-2","military-3","psychological-1","psychological-2","psychological-3","social-1","social-2","social-3","communitysupport","communitysupport"] as string[],

        uuid : "", // the game id
        playersideusername : "",

        // notifier shown
        moveNotifier : "Move Notifier",
        timer : 600.0, // temporary variable! due to delays in window.onTimeout functions, may not be accurate

        // variables (most described in backend classes.py)
        lastmove : Date.now(),
        timeoutID : NaN,
        intervalID : NaN,
        showDialogNormal : false,
        showDialogDefence : false,
        showOptionDefence : false,
        selectionDefence : [] as (number|string)[],
        showOptionDefence2 : false,
        showOptionField : false,
        showDialogField : false,
        showDiscardPlay : false,
        showOptionHand : false,
        showDialogHand : false,
        opponentHandTemp : [] as any[],
        discardHand : false,
        canClickEndTurn: true,
        index : -1,
        showForfeitButton : true,
        // variables above here need to be added to beforeMount storage writer in GameAreaApp.vue
        // variables below do not need to be saved, as they do not need to be restored
        // show forfeit dialog
        showForfeit : false,
        // this variable is described in Hand.vue
        vetoShowOpponentHand : false,
        // accurate timer functionally equivalent to backend game.player.timer so not needed to store
        storedAccurateTimer : 600.0,
    }),
    actions:{
        async resetStore() {
            // reset the store to its default values
            this.handList = []
            this.discardDeck = ["back-black"] as string[]
            this.cardsLeft = await this.getStdDeckSize()
            this.playersideusername = ""
            this.uuid = ""
        },

        getStdDeckSize() : Promise<number> {
            return fetch(`${BACKEND_URL}/deck_size`)
                // fetch() returns a promise. When we have received a response from the server,
                // the promise's `then()` handler is called with the response.
                .then((response) => {
                    // Our handler throws an error if the request did not succeed.
                    if (!response.ok) {
                        throw new Error(`HTTP error: ${response.status}`);
                    }
                    // Otherwise (if the response succeeded), our handler fetches the response
                    // as text by calling response.text(), and immediately returns the promise
                    // returned by `response.text()`.
                    return response.text();
                })
                // When response.text() has succeeded, the `then()` handler is called with
                // the text, and we copy it into the `poemDisplay` box.
                .then((text) => {
                    return parseInt(text)
                })
                // Catch any errors that might happen, and display a message
                // in the `poemDisplay` box.
                .catch((error) => {
                    console.log("Cannot get deck size")
                    console.log(error.toString())
                    return NaN
                })

        },

        drawDeck() : Promise<string> {
            // post draw deck request to the backend with username and sessionkey
            // the drawn card will be sent over and the hand will be updated
            return fetch(`${BACKEND_URL}/pop_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    if(json_response["cardsLeft"] === 0){
                        this.newDeck()
                    }

                    this.getHand()

                    this.getDiscard()

                    this.cardsLeft = json_response["cardsLeft"]

                    return json_response["card"] as string

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not draw deck"
                });
        },

        newDeck() : Promise<string|string[]> {
            // post new deck request to the backend with username and sessionkey
            // an entirely new full deck will be generated
            return fetch(`${BACKEND_URL}/new_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    return json_response["deck"] as string[]

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not make new deck"
                });
        },

        getDeck() : Promise<string|string[]>  {
            // post get deck request to the packend with username and sessionkey
            // the whole undrawn deck will be sent over
            return fetch(`${BACKEND_URL}/get_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    return json_response["deck"] as string[]

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not get deck"
                });
        },

        getCardsLeft() : Promise<number> {
            // post get cards left request to the packend with username and sessionkey
            // the number of cards in the deck will be returned & updated
            return fetch(`${BACKEND_URL}/get_cardsleft`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    this.cardsLeft = json_response["cardsLeft"] as number

                    return json_response["cardsLeft"] as number

                })
                .catch(error => {
                    console.log(error.toString())
                    return NaN
                });
        },


        // get crisis and new crisis
        newCrisis() : Promise<string> {
            // post new deck request to the backend with username and sessionkey
            // an entirely new full deck will be generated
            return fetch(`${BACKEND_URL}/new_crisis`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    this.crisis = json_response["crisis"] as string

                    return json_response["crisis"] as string

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not get new crisis"
                });
        },
        getCrisis() : Promise<string> {
            // post get crisis  request to the backend with username and sessionkey
            // the crisis will be sent over
            return fetch(`${BACKEND_URL}/get_crisis`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    this.crisis = json_response["crisis"] as string
                    //console.log(this.crisis)

                    return json_response["crisis"] as string

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not get crisis"
                });
        },

        getHand() : Promise<string|string[]> {
            // post get hand  request to the backend with username and sessionkey
            // the hand will be sent over
            return fetch(`${BACKEND_URL}/get_hand`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    this.handList = json_response["hand"] as {
                        name: string, enablePlay: boolean,
                        requiresDialogNormal: boolean, requiresOptionDefence: boolean,
                        requiresOptionField: boolean, requiresDialogHand: boolean,
                        requiresOptionHand: boolean,
                        warn:any
                    }[]

                    return json_response["hand"] as string[]

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not get hand"
                });
        },

        getOpponentHand() : Promise<string|string[]|any[]> {
            // post get opponent hand request to the backend with username and sessionkey
            // the hand will be sent over
            return fetch(`${BACKEND_URL}/get_opponent_hand`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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
                    this.opponentHandTemp = json_response["hand"] as any[]
                    return json_response["hand"] as any[]

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not get hand"
                });
        },

        getDiscard() : Promise<string|string[]> {
            // post get hand  request to the backend with username and sessionkey
            // the hand will be sent over
            return fetch(`${BACKEND_URL}/get_discard`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key()
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

                    this.discardDeck = json_response["discard"] as string[]

                    return json_response["discard"] as string[]

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not get discard"
                });
        },

        playHand(hand_card_index : number, extra? : any, extra2? : any) : Promise<string> {
            // post get hand  request to the backend with username and sessionkey
            // the hand will be sent over
            return fetch(`${BACKEND_URL}/play_hand`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key(),
                    card_index : hand_card_index,
                    extra: extra, // additional arguments that some cards might need
                    extra2: extra2
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

                    if (json_response["nextTurn"]) {
                        this.endTimer()
                    }

                    this.handList = json_response["hand"] as {
                        name: string, enablePlay: boolean,
                        requiresDialogNormal: boolean, requiresOptionDefence: boolean,
                        requiresOptionField: boolean, requiresDialogHand: boolean,
                        requiresOptionHand: boolean,
                        warn:any
                    }[]
                    this.discardDeck = json_response["discard"] as string[]
                    this.cardsLeft = json_response["cardsLeft"] as number
                    this.field = json_response["field"] as string[]
                    this.moveNotifier = json_response["moveNotifier"] as string
                    this.canClickEndTurn = json_response["canClickEndTurn"] as boolean

                    if (json_response["needDiscard"]) {
                        this.discardHand = true
                    }

                    if (json_response["winThisTurn"]) {
                        this.canClickEndTurn = false
                        this.showForfeitButton = false
                        this.endTimer()
                    }

                    return json_response["cardPlayed"] as string

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not play hand"
                });
        },
        discardCardFromHand(hand_card_index : number) : Promise<string> {
            this.showForfeit = false

            return fetch(`${BACKEND_URL}/discard_hand`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key(),
                    card_index : hand_card_index,
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

                    if (json_response["nextTurn"]) {
                        this.endTimer()
                    }

                    this.handList = json_response["hand"] as {
                        name: string, enablePlay: boolean,
                        requiresDialogNormal: boolean, requiresOptionDefence: boolean,
                        requiresOptionField: boolean, requiresDialogHand: boolean,
                        requiresOptionHand: boolean,
                        warn:any
                    }[]
                    this.discardDeck = json_response["discard"] as string[]
                    this.cardsLeft = json_response["cardsLeft"] as number
                    this.field = json_response["field"] as string[]
                    this.moveNotifier = json_response["moveNotifier"] as string
                    this.canClickEndTurn = json_response["canClickEndTurn"] as boolean

                    if (json_response["winThisTurn"]) {
                        this.canClickEndTurn = false
                        this.showForfeitButton = false
                        this.endTimer()
                    }

                    this.discardHand = !json_response["nextTurn"]

                    return json_response["cardPlayed"] as string

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not play hand"
                });
        },
        passTurn() : Promise<string> {
            this.showDialogNormal = false // no stray dialogs
            this.showOptionDefence = false
            this.showDialogDefence = false
            this.showOptionField = false
            this.showDialogField = false
            this.showDialogHand = false
            this.showOptionHand = false
            this.showDiscardPlay = false
            this.showOptionDefence2 = false
            this.selectionDefence = []
            this.showForfeit = false

            return fetch(`${BACKEND_URL}/pass_turn`, {
                method: "POST",
                body: JSON.stringify({
                    username: userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
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

                    if (json_response["nextTurn"]) {
                        this.endTimer()
                    }

                    this.handList = json_response["hand"] as {
                        name: string, enablePlay: boolean,
                        requiresDialogNormal: boolean, requiresOptionDefence: boolean,
                        requiresOptionField: boolean, requiresDialogHand: boolean,
                        requiresOptionHand: boolean,
                        warn:any
                    }[]
                    this.discardDeck = json_response["discard"] as string[]
                    this.cardsLeft = json_response["cardsLeft"] as number
                    this.field = json_response["field"] as string[]
                    this.moveNotifier = json_response["moveNotifier"] as string
                    this.canClickEndTurn = json_response["canClickEndTurn"] as boolean

                    if (json_response["winThisTurn"]) {
                        this.canClickEndTurn = false
                        this.showForfeitButton = false
                        this.endTimer()
                    }

                    this.discardHand = !json_response["nextTurn"]

                    return "Success"

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not play hand"
                });
        },
        forfeitGame() {
            this.showDialogNormal = false // no stray dialogs
            this.showOptionDefence = false
            this.showDialogDefence = false
            this.showOptionField = false
            this.showDialogField = false
            this.showDialogHand = false
            this.showOptionHand = false
            this.showDiscardPlay = false
            this.showOptionDefence2 = false
            this.selectionDefence = []
            this.showForfeit = false
            this.showForfeitButton = false

            return fetch(`${BACKEND_URL}/forfeit`, {
                method: "POST",
                body: JSON.stringify({
                    username: userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
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

                    this.moveNotifier = json_response["moveNotifier"] as string
                    this.canClickEndTurn = json_response["canClickEndTurn"] as boolean

                    if (json_response["winThisTurn"]) { // always true
                        this.canClickEndTurn = false
                        this.endTimer()
                    }

                    this.discardHand = false

                    return "Success"

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not play hand"
                });
        },
        /*
        start timer basically creates a function that updates the time every (about) 200ms (and checks for timeout)
        it does not constantly update the backend timer (the source of truth) because of delays in calculation
        instead it is updated only in end timer
        */
        startTimer() {
            // check for loss by timeout
            if (this.storedAccurateTimer - (Date.now() - this.lastmove)/1000 < 0) {
                this.endTimer()
            } else {
                let next_update_ms: number = 50 * (this.storedAccurateTimer % 0.2)
                this.timeoutID = window.setTimeout(() => {
                    if (this.storedAccurateTimer - (Date.now() - this.lastmove) / 1000 > 0) {
                        fetch(`${BACKEND_URL}/update_timer`, {
                            method: "POST",
                            body: JSON.stringify({
                                username: userSignInStore.username,
                                request_username: userSignInStore.username,
                                game_id: this.uuid,
                                login_session_key: userSignInStore.login_session_key(),
                                delta: (Date.now() - this.lastmove) / 1000
                            }),
                            headers: {
                                "Content-type": "application/json; charset=UTF-8"
                            }
                        })
                        // create timer updating function (which also needs to check for timer ending)
                        this.timer = this.storedAccurateTimer - (Date.now() - this.lastmove) / 1000
                        this.intervalID = window.setInterval(() => {
                            if (this.storedAccurateTimer - (Date.now() - this.lastmove) / 1000 > 0) {
                                fetch(`${BACKEND_URL}/update_timer`, {
                                    method: "POST",
                                    body: JSON.stringify({
                                        username: userSignInStore.username,
                                        request_username: userSignInStore.username,
                                        game_id: this.uuid,
                                        login_session_key: userSignInStore.login_session_key(),
                                        delta: (Date.now() - this.lastmove) / 1000
                                    }),
                                    headers: {
                                        "Content-type": "application/json; charset=UTF-8"
                                    }
                                })
                                this.timer = this.storedAccurateTimer - (Date.now() - this.lastmove) / 1000
                            } else {
                                // timeout
                                this.timer = 0.0
                                this.endTimer()
                            }
                        }, 198) // 10ms delay is too laggy
                        // 198ms to compensate for the fact that delays will not be exact
                    } else {
                        // timeout
                        this.timer = 0.0
                        this.endTimer()
                    }
                }, next_update_ms)
            }
        },
        endTimer() {
            // todo call in log out
            // todo: update opponent's timer if opponent is logged out (not connected to socket)
            window.clearTimeout(this.timeoutID)
            window.clearInterval(this.intervalID)
            let delta: number = (Date.now() - this.lastmove)/1000
            this.timer = Math.max(0, this.storedAccurateTimer-delta)
            this.storedAccurateTimer -= delta
            if (this.storedAccurateTimer < 0) {
                this.showDialogNormal = false // no stray dialogs
                this.showOptionDefence = false
                this.showDialogDefence = false
                this.showOptionField = false
                this.showDialogField = false
                this.showDialogHand = false
                this.showOptionHand = false
                this.showDiscardPlay = false
                this.showOptionDefence2 = false
                this.selectionDefence = []
                this.showForfeit = false
                this.showForfeitButton = false

                fetch(`${BACKEND_URL}/timeout`, {
                    method: "POST",
                    body: JSON.stringify({
                        username: userSignInStore.username,
                        request_username: userSignInStore.username,
                        game_id: this.uuid,
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

                        this.moveNotifier = json_response["moveNotifier"] as string
                        this.canClickEndTurn = json_response["canClickEndTurn"] as boolean

                        if (json_response["winThisTurn"]) { // always true
                            this.canClickEndTurn = false
                        }

                        this.discardHand = false

                        return "Success"

                    })
                    .catch(error => {
                        console.log(error.toString())
                        return "Could not play hand"
                    });
            } else {
                // send over delta to game server
                fetch(`${BACKEND_URL}/update_timer`, {
                    method: "POST",
                    body: JSON.stringify({
                        username: userSignInStore.username,
                        request_username: userSignInStore.username,
                        game_id: this.uuid,
                        login_session_key: userSignInStore.login_session_key(),
                        delta: delta,
                        store: true
                    }),
                    headers: {
                        "Content-type": "application/json; charset=UTF-8"
                    }
                })
            }
        }
    },
})(globalPiniaInstance)