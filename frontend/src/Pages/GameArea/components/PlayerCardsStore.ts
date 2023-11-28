import {defineStore} from "pinia";
import {userSignInStore} from "../../../components/UserSignInStore";
import {globalPiniaInstance} from "../../../global";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

// this store is used to store the cards currently in handm the number of cards left, and the discard deck
// this store also has action functions that pop cards from the deck in server
// cardsLeft is manually updated in the deck functions whenever a card is popped. For the most, part don't worry about it


export const playerCardsStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'playerCards',
    state: () =>({
        handList : [] as string[],
        discardDeck : ["back-black"] as string[],
        cardsLeft : 45 as number,

        // played cards such as the crisis cards, community support and defence cards should be stored server side
        // as they need to be displayed on opponent's end too
        // local variables are to be updated and have their relevant value fetched from backend
        // whenever they're needed (e.g. get crisis card at the start of a game, played cards before every turn)
        crisis : "back-white" as string,
        // field consists of defences & community supports in play
        field: ["military-1","military-2","military-3","psychological-1","psychological-2","psychological-3","social-1","social-2","social-3","communitysupport","communitysupport"] as string[],


    }),
    getters: {

    },
    actions:{
        resetStore (){
            // reset the store to its default values
            this.handList = [] as string[]
            this.discardDeck = ["back-black"] as string[]
            this.cardsLeft = 51
        },

        drawDeck() : string | void {
            // post draw deck request to the packend with username and sessionkey
            // the top card in the undrawn deck will be sent over
            // use this over getdeck when possible as it pops out the top card & doesn't send the whole deck
            fetch(`${BACKEND_URL}/pop_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
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

                    if(this.handList.length < 7){
                        this.handList.push(json_response["card"])
                    }
                    else {
                        this.discardDeck.push(this.handList.shift()!)
                        this.handList.push(json_response["card"])
                    }

                    this.cardsLeft = json_response["cardsLeft"]

                    if(json_response["cardsLeft"] === 0){
                        this.newDeck()
                    }

                    return json_response["card"]

                })
                .catch(error => {
                    console.log(error.toString())
                });

            return
        },

        newDeck(){
            // post new deck request to the backend with username and sessionkey
            // an entirely new full deck will be generated
            fetch(`${BACKEND_URL}/new_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
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

                    console.log(json_response["deck"])

                })
                .catch(error => {
                    console.log(error.toString())
                });
        },

        getDeck(): string[] | string {
            // post get deck request to the packend with username and sessionkey
            // the whole undrawn deck will be sent over
            fetch(`${BACKEND_URL}/get_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
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

                    return json_response["deck"]

                })
                .catch(error => {
                    console.log(error.toString())
                });
            return "something wrong happened"
        },


        // get crisis and new crisis
        newCrisis(){
            // post new deck request to the backend with username and sessionkey
            // an entirely new full deck will be generated
            fetch(`${BACKEND_URL}/new_crisis`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
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

                    this.crisis = json_response["crisis"]

                    return json_response["crisis"]

                })
                .catch(error => {
                    console.log(error.toString())
                });
        },
        getCrisis(){
            // post get deck request to the packend with username and sessionkey
            // the whole undrawn deck will be sent over
            fetch(`${BACKEND_URL}/get_crisis`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
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

                    this.crisis = json_response["crisis"]
                    console.log(this.crisis)

                    return json_response["crisis"]

                })
                .catch(error => {
                    console.log(error.toString())
                });
            return "something wrong happened"
        }
    },
})(globalPiniaInstance)