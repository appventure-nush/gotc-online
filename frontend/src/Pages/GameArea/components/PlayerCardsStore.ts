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
        handList : [] as string[],
        discardDeck : ["back-black"] as string[],
        cardsLeft : 46 as number,

        // played cards such as the crisis cards, community support and defence cards should be stored server side
        // as they need to be displayed on opponent's end too
        // local variables are to be updated and have their relevant value fetched from backend
        // whenever they're needed (e.g. get crisis card at the start of a game, played cards before every turn)
        crisis : "back-white" as string,
        // field consists of defences & community supports in play
        field: ["military-1","military-2","military-3","psychological-1","psychological-2","psychological-3","social-1","social-2","social-3","communitysupport","communitysupport"] as string[],

        uuid: ""
    }),
    getters: {

    },
    actions:{
        async resetStore() {
            // reset the store to its default values
            this.handList = [] as string[]
            this.discardDeck = ["back-black"] as string[]
            this.cardsLeft = await this.getStdDeckSize()
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

                    this.handList = json_response["hand"] as string[]

                    return json_response["hand"] as string[]

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

        playHand(hand_card_index : number) : Promise<string> {
            // post get hand  request to the backend with username and sessionkey
            // the hand will be sent over
            return fetch(`${BACKEND_URL}/play_hand`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    request_username: userSignInStore.username,
                    game_id: this.uuid,
                    login_session_key : userSignInStore.login_session_key(),
                    card_index : hand_card_index
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

                    this.handList = json_response["hand"] as string[]
                    this.discardDeck = json_response["discard"] as string[]
                    this.cardsLeft = json_response["cardsLeft"] as number

                    return json_response["cardPlayed"] as string

                })
                .catch(error => {
                    console.log(error.toString())
                    return "Could not play hand"
                });
        }
    },
})(globalPiniaInstance)