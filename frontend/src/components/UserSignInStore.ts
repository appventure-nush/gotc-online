import {defineStore} from "pinia";
import {globalPiniaInstance} from "../global";

//const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

// this store is used to store which user is signed in (the username)
// loginsessionkey is also accessible through a getter
// key can also be set through a setter action function
// NOTE: please use the store rather than the signin/signout events from now on

export const userSignInStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'userSignIn',
    state: () =>({
        username : "" as string
    }),
    getters: {
        isSignedIn: (state) => state.username !== "",


    },
    actions:{

        login_session_key () {
            // gets the log in key
            return localStorage.getItem("LoginSessionKey")
        },

        setLoginSessionKey (new_key : string){
            // sets the log in key
            localStorage.setItem("LoginSessionKey",new_key)
        }

    },
})(globalPiniaInstance)