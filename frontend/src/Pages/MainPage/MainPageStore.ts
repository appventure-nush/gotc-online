import {defineStore} from "pinia";
import {globalPiniaInstance} from "../../global";

export const mainPageStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'mainPageStore',
    state: () =>({
        showSignInPrompt : false
    }),
    getters: {

        signInPrompDisplay : (state) => state.showSignInPrompt ? "flex" : "none",

    },
    actions:{



    },
})(globalPiniaInstance)