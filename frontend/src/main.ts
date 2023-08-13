import FrontPageApp from "./Pages/FrontPage/FrontPageApp.vue";
import MainPageApp from "./Pages/MainPage/MainPageApp.vue";
import { createRouter, createWebHistory } from 'vue-router'
import App from "./RoutingApp.vue";
import {createApp} from "vue";



// 1. Define route components.
// These can be imported from other files
const FrontPage = FrontPageApp
const MainPage = MainPageApp

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const routes = [
    { path: '/', component: FrontPage },
    { path: '/MainPage', component: MainPage },
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHistory(),
    routes, // short for `routes: routes`
})

// 5. Create and mount the root instance.
createApp(App).use(router).mount('#app')
// Make sure to _use_ the router instance to make the
// whole app router-aware.

