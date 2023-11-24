<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./components/CardHolder.vue";
import BigCardHolder from "./components/BigCardHolder.vue";
import PlayerSide from "./components/PlayerSide.vue";
import Userform from "../../components/userform.vue";

export default defineComponent({
  name: "GameAreaApp",
  components: {PlayerSide, BigCardHolder, CardHolder, Userform},
  include:{
    CardHolder,
  },
})
</script>

<!--
  This GameApp App/Page is the page that will be shown when going to [url]/gamearea as specified in the vue router in main.ts
-->

<template>

  <div class="gamearea">
    <div class="userform-temp" >
      <userform/>
    </div>
    <router-link to="/MainPage" v-slot="{href, route, navigate}" class="back-temp">
      Back to MainPage
    </router-link>

    <player-side class="player-side"/>


    <div class="bigcard-overlay">
      <big-card-holder/>
    </div>
  </div>



</template>

<style scoped>

.userform-temp {
  position: relative; top: 0; left: 0;
  padding: 10px;
  border: 2px green solid;
  align-items: center;
  display: block;
  text-align: center;
  width: 30%;
}
.back-temp{
  position: relative;
  display: block;
  border: 2px steelblue solid;
  padding: 10px;
  width: 30%;
  text-align: center;
}

.player-side{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 60%;
  width: 100%;
}

.gamearea{
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background-color: maroon;
}

.bigcard-overlay{
  position: absolute;
  height: 80vh;
  width: 40vw;
  top: 10vh;
  left: 30vw;
  display: inline-block;
  align-items: center;
}

</style>