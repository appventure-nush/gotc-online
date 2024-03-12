import {reactive} from "vue"
import { io } from "socket.io-client"
import {userSignInStore} from "./components/UserSignInStore";
import {router} from "./main";
import {opponentFieldStore} from "./Pages/GameArea/components/OpponentFieldStore";

export const state = reactive({
    connected: false,
    numlogin: 0,
    userStore: userSignInStore,
    oppField: opponentFieldStore
})

const URL = import.meta.env.VITE_BACKEND_URL

export const socket = io(URL, {
    withCredentials: true
})

socket.on("connect", () => {
    state.connected = true
})

socket.on("disconnect", () => {
    state.connected = false
})

socket.on("number logged in", (args) => {
    state.numlogin = args["data"]
})

socket.on("random match request", (args) => {
    if (args["username"] == state.userStore.username) {
        router.push("/GameArea/"+args["id"])
    }
})

socket.on("update opponent state", (args) => {
    if (args["username"] == state.userStore.username && args["uuid"] == state.oppField.uuid) {
        if ("cardsLeft" in args) {
            state.oppField.cardsLeft = args["cardsLeft"]
        }
        if ("crisis" in args) {
            state.oppField.crisis = args["crisis"]
        }
        if ("discard" in args) {
            state.oppField.discard = args["discard"]
        }
        if ("field" in args) {
            state.oppField.field = args["field"]
        }
    }
})