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
        cardsLeft : 51 as number,
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
        }
    },
})(globalPiniaInstance)