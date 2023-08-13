<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
import backendmathform from "./components/backendmathform.vue";
import userform from "./components/userform.vue";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
</script>

<template>
  <div>
    <a href="https://vitejs.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>

  <HelloWorld msg="PLEASE USE VITE + VUE FROM NOW ON"/>

  <p class="oran-berry-disc">
    Image below is fetched from backend
  </p>
  <a :href="BACKEND_URL + '/get_image'" target="_blank">
    <img :src="BACKEND_URL + '/get_image'" class="logo vanilla" alt="Test Image From backend. (if you see this text it's possible that you did not turn on backend)" />
  </a>

  <div class="backend-calculation"><backendmathform/></div>
  <div class="userform"><userform/></div>
</template>

<style scoped>

@import "style.css";

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
