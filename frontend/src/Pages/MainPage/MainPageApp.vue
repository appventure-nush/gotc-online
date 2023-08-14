<script setup lang="ts">

import Topbarbuttonbar from "./components/topbarbuttonbar.vue";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

</script>

<template>
  <div class="all_container">
    <div class="topbar">
      <p class="gotc-online-pseudologo">GOTC<br>ONLINE</p>
      <topbarbuttonbar/>
      <button>Sign In</button>
    </div>
  </div>
</template>

<style scoped>



.topbar .gotc-online-pseudologo{
  text-align: center;
  color: #c1f773ff;
  font-size: 2.5vh;
  font-weight: 600;
}

/* :deep means that this css will also be aplied to child vue components used in this vue component */
:deep button {
  border-radius: 10pt;
  background-color: #d9c779ff; /* Green background */
  border: 5px solid #cd931bff; /* Green border */
  color: black; /* White text */
  padding: 0.5vh 0.5vw; /* Some padding */
  cursor: pointer; /* Pointer/hand icon */
  float: left; /* Float the buttons side by side */

  width: 120pt ;
  text-align: center;

  font-size: 3vh;

  transition: border-color 0.3s;
}

:deep button:hover{
  border-color: firebrick;
}



.all_container{
  background-image: url("../../assets/mainpage_bg.png");
  background-size: 100vw 100vh;
  height: 100vh;
  width: 100vw;

  font-family: "Exo 2",serif;
}

.topbar{
  height: 8vh;
  background-color: #964e44ff;
  top: 0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-left: 10vw;
  padding-right: 10vw;
}


</style>