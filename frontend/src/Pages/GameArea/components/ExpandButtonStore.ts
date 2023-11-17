import {defineStore} from "pinia";
import {globalPiniaInstance} from "../../../global";

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