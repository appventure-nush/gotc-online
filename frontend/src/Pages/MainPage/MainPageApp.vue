<script lang="ts">

import {defineComponent} from "vue";
import userform from "../../components/userform.vue";
import topbarbuttonbar from "./components/topbarbuttonbar.vue";
import {mainPageStore} from "./MainPageStore";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export default defineComponent({
  components: {
    userform, topbarbuttonbar
  },
  data(){
    return{
      isLandscape : screen.height<=screen.width
    }
  },
  computed: {
    showSignInDialog() {
      return mainPageStore.signInPrompDisplay
    },
    isMobile() {
      return Math.min(screen.width, screen.height) <= 500
    },
    showWarningBox(){
      return this.isMobile || !this.isLandscape
    }
  },
})

</script>

<template>
  <div class="all_container">
    <div class="topbar">
      <p class="gotc-online-pseudologo">GOTC<br>ONLINE</p>
      <topbarbuttonbar/>
      <div class="userform-div"><userform/></div>
    </div>
    <div v-if="showWarningBox" class="bottom-reminders">
      <p v-if="!isLandscape">Please rotate your device such that it is in landscape mode.</p><br v-if="!isLandscape">
      <p v-if="isMobile">You seem to be playing on a mobile device. You may need to zoom out on your browser for text to be properly sized.</p>
    </div>
  </div>
</template>

<style scoped>

.userform-div{
  display: v-bind(showSignInDialog);
  top: 10%;
  position: absolute;
  right: 5%;
  flex-direction: column;
  background: #80808080;
  justify-content: center;
  align-items: center;
  padding: 1em;
  row-gap: .5em;
}

.topbar .gotc-online-pseudologo{
  text-align: center;
  color: white;
  font-size: 2.5vh;
  font-weight: 600;
  font-style: italic;
  width: 12rem;
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
  background-color: #C8553D;
  top: 0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-left: 10vw;
  padding-right: 10vw;
}

.bottom-reminders{
  position: absolute;
  bottom: 5%;
  right: 5%;
  left: 5%;
  background: #FFD5C2;
  color: black;
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: column;
  padding: .5em;
  gap: 1vh;
}
.bottom-reminders > p{
  margin: 0;
  display: flex;
  justify-content: center;
  font-size: 3.5vh;
  line-height: .9;
}

</style>