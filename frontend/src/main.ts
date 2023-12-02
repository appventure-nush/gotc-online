//we import the pages' respective vue apps from their respective folders in the pages folder
import FrontPageApp from "./Pages/FrontPage/FrontPageApp.vue";
import MainPageApp from "./Pages/MainPage/MainPageApp.vue";
import GameAreaApp from "./Pages/GameArea/GameAreaApp.vue";
import HelpAreaApp from "./Pages/HelpArea/HelpAreaApp.vue";


//import vue-router's things here
import { createRouter, createWebHistory } from 'vue-router'



// We import the RoutingApp page that contains the router-view (and any other ui elements) that will be mounted to
// index.html's app div
// Therfore whatever app we assign to be displayed by the router view will be displayed to the user
// through the RoutingApp mounted on the index.html's app div.
// yes, that's ike 3 layers of nesting but its rather alright (and the way to do things) once you think about it.
import RoutingApp from "./RoutingApp.vue";

// We import createApp from vue to create the RoutingApp from its vue component so that we can display the app created
// from RoutingApp's vue component on index.html's app div.
import {createApp} from "vue";
import {globalPiniaInstance} from "./global";




// 1. Define route components.
// These can be imported from other files
// which is what we do in this case
const FrontPage = FrontPageApp
const MainPage = MainPageApp
const GameArea = GameAreaApp
const HelpArea = HelpAreaApp

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later. (I haven't gotten to that part of the vue-router tutorial)
const routes = [
    { path: '/', component: FrontPage },
    { path: '/MainPage', component: MainPage },
    { path: '/GameArea', component: GameArea},
    { path: '/HelpArea', component: HelpArea}
]

// 3. Create the router instance and pass the `routes` option
// You can pass in additional options here, but let's
// keep it simple for now.
const router = createRouter({
    // 4. Provide the history implementation to use.
    history: createWebHistory(
        import.meta.env.VITE_BASEPATH
    ),
    routes, // short for `routes: routes`
})

// 5. Create and mount the root instance.
createApp(RoutingApp)
    .use(globalPiniaInstance)
    .use(router)
    .mount('#app')
// Make sure to _use_ the router instance to make the
// whole app router-aware.
// also use the Global Pinia Instance to have a global Pinia Store

