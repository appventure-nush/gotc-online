import {defineStore} from "pinia";
import {globalPiniaInstance} from "../../../global";


// this store stores the fact if a card needs to be enlarged and what card needs to be enlarged (via logging the cards image source)
// stores are reactive so vue components will be able to detect changes to the variables here if the expandButtonStore is imported

export const expandButtonStore  = defineStore({
    // id is required so that Pinia can connect the store to the devtools
    id: 'expandButton',
    state: () =>({
        expand : false as boolean,
        imageSrc : "" as string
    }),
    getters: {},
    actions:{

    }
})(globalPiniaInstance)