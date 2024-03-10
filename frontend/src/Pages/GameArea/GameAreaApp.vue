<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./components/CardHolder.vue";
import BigCardHolder from "./components/BigCardHolder.vue";
import PlayerSide from "./components/PlayerSide.vue";
import OpponentSide from "./components/OpponentSide.vue"

export default defineComponent({
  name: "GameAreaApp",
  components: {OpponentSide, PlayerSide, BigCardHolder, CardHolder},
  include:{
    CardHolder,
  }
})
</script>

<!--
  This GameApp App/Page is the page that will be shown when going to [url]/gamearea as specified in the vue router in main.ts
-->

<template>

  <div class="gamearea">

    <OpponentSide class="opponent-side"/>
    <player-side class="player-side"/>

    <big-card-holder/>

  </div>



</template>

<style scoped>

.gamearea{
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background-color: maroon;

  font-family: "Exo 2", serif;
}

.opponent-side{
  position: absolute;
  top: 0;
  left: 0;
  height: 40%;
  width: 100%;
}

.player-side{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 60%;
  width: 100%;
}



</style>