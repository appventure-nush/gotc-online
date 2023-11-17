import {defineStore} from "pinia";
import {globalPiniaInstance} from "../global";

//const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export const userSignInStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'userSignIn',
    state: () =>({
        username : "" as string
    }),
    getters: {

    },
    actions:{

    },
})(globalPiniaInstance)