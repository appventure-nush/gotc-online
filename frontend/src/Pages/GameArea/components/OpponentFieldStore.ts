import {defineStore} from "pinia";
import {globalPiniaInstance} from "../../../global";


export const opponentFieldStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'opponentField',
    state: () =>({
        //as with the player, update the local variables whenever a turn happens
        field : ["digital-1","digital-2","digital-3","economic-1","economic-2","economic-3","civil-1","civil-2","civil-3"] as string[], // defences & community supports in play
        crisis: "back-black",



    }),
    getters: {

    },
    actions:{

    },
})(globalPiniaInstance)