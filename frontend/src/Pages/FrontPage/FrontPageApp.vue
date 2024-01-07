<script setup lang="ts">
/*
Here we import the (FrontPage-specific) Vue UI Components from the components folder in the Frontpage folder.
Those components could be used elsewhere but since they are probably only going to be used in the FrontPage, we put
them in Frontpage's very own components folder for tidiness
 */
import HelloWorld from './components/HelloWorld.vue'
import backendmathform from "./components/backendmathform.vue";
/*
Meanwhile this userform login/out Vue component is placed in the src's main/public components folder since it is
probably versatile enough to be used across multiple pages.
 */
import userform from "../../components/userform.vue";
import socketconnection from "./components/socketconnection.vue";

// import the backend url from the .env (for development server), .env.production (for production server),
// or .env.production.local (for private production server whose IP address should ideally not be committed to Git
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

/*
import { socket } from "../../socket"
// in case of reload
socket.disconnect()
*/

</script>

<template>
  <!--
  This FrontPageApp.vue file is the first page shown to the user (as of now) as dictated by the vue-router
  in RoutingApp.vue.
  Its main purpose is to define what the FontPageApp's main layout is using html components and
  custom-made Vue UI components.
  The functionality of those Vue UI components is dictated through their respective vue files.

  The vue-router in RoutingApp.vue and main.ts decides which vue component is mounted (displayed to the user) based on the
  defined url routes.
  More info can be found in the RoutingApp.vue file
  -->
  <div class="app">
    <div>
      <a href="https://vitejs.dev" target="_blank">
        <img src="/vite.svg" class="logo" alt="Vite logo" />
      </a>
      <a href="https://vuejs.org/" target="_blank">
        <img src="../../assets/vue.svg" class="logo vue" alt="Vue logo" />
      </a>
    </div>

    <HelloWorld msg="PLEASE USE VITE + VUE FROM NOW ON"/>

    <socketconnection></socketconnection>

    <p class="oran-berry-disc">
      Image below is fetched from backend
    </p>
    <a :href="BACKEND_URL + '/get_image'" target="_blank">
      <img :src="BACKEND_URL + '/get_image'" class="logo vanilla" alt="Test Image From backend. (if you see this text it's possible that you did not turn on backend)" />
    </a>

    <div class="backend-calculation"><backendmathform/></div>
    <div class="userform"><userform/></div>

    <router-link to="/MainPage"><button style="margin: 10pt">Go to MainPage</button></router-link>
  </div>
</template>

<style scoped>

/*
Here we specify the style of the components in the FontPageApp vue component.
 */

.app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>
