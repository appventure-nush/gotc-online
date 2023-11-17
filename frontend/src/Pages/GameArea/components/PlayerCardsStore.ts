import {defineStore} from "pinia";
import {userSignInStore} from "../../../components/UserSignInStore";
import {globalPiniaInstance} from "../../../global";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

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
        drawDeck(){
            fetch(`${BACKEND_URL}/pop_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    login_session_key : localStorage.getItem("LoginSessionKey")
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

                })
                .catch(error => {
                    console.log(error.toString())
                });
        },

        newDeck(){
            fetch(`${BACKEND_URL}/new_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    login_session_key : localStorage.getItem("LoginSessionKey")
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
            fetch(`${BACKEND_URL}/new_deck`, {
                method: "POST",
                body: JSON.stringify({
                    username : userSignInStore.username,
                    login_session_key : localStorage.getItem("LoginSessionKey")
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