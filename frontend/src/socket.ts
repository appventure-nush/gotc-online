import { reactive } from "vue"
import { io } from "socket.io-client"
import socketconnection from "./Pages/FrontPage/components/socketconnection.vue";

export const state = reactive({
    connected: false,
})

const URL = process.env.NODE_ENV === "production" ? window.location.toString() : "http://localhost:5000"

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
    socketconnection.numlogin = args["data"]
});