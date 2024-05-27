import {defineStore} from "pinia";
import {globalPiniaInstance} from "../../../global";


export const opponentFieldStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'opponentField',
    state: () =>({
        //as with the player, update the local variables whenever a turn happens
        discard : ["civil-placeholder","digital-placeholder","economic-placeholder","military-placeholder","psychological-placeholder","social-placeholder"] as string[],
        field : ["digital-1","digital-2","digital-3","economic-1","economic-2","economic-3","civil-1","civil-2","civil-3"] as string[], // defences & community supports in play
        crisis: "back-black" as string,
        cardsLeft : 46 as number,
        timer: 600.0,

        uuid: "",
        opponentsideusername: "NO GAME INITIATED",

    }),
    getters: {

    },
    actions:{

    },
})(globalPiniaInstance)