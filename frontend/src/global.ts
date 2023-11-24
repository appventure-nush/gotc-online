//import pinia for data storage
//we need the global pinia instance to use pinia globally (aka it doesn't work outside the Pages folder when i don't do this)
import {createPinia} from "pinia";
export const globalPiniaInstance = createPinia()