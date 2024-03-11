import {reactive} from "vue"
import { io } from "socket.io-client"
import {userSignInStore} from "./components/UserSignInStore";
import {router} from "./main";

export const state = reactive({
    connected: false,
    numlogin: 0,
    userStore: userSignInStore
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