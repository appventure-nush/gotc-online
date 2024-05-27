<script lang="ts">
import {defineComponent} from 'vue'
import Userform from "../../../components/userform.vue";
import {playerCardsStore} from "./PlayerCardsStore";
import {userSignInStore} from "../../../components/UserSignInStore";
import {opponentFieldStore} from "./OpponentFieldStore";

export default defineComponent({
  name: "UtilBar",
  components:{Userform},
  setup(){
    const playerCards = playerCardsStore
    const oppStore = opponentFieldStore
    const userStore = userSignInStore
    return { playerCards, oppStore, userStore }
  },
  data(){
    return{

    }
  },
  methods: {
    displayFormattedTime(t: number) {
      if (t < 1) {
        return "0:0"+t.toFixed(2)
      } else if (t < 10) {
        return "0:0"+t.toFixed(1)
      } else {
        // format time eg: 9:09
        if ((t%60).toFixed(0) === "60") {
          return ""+(Math.floor(t/60)+1)+":00"
        }
        return ""+Math.floor(t/60)+":"+(t%60<9.5 ? "0": "")+(t%60).toFixed(0)
      }
    }
  }
})
</script>

<template>
  <div class="utilbar-component-div" >
    <div v-if="!userStore.isSignedIn" class="userform-temp">
      <userform />
      <router-link to="/" v-slot="{href, route, navigate}" class="back-temp">
        Back to MainPage
      </router-link>
    </div>
    <div v-else class="utilbar-component-div utilbar-signed-in" >
      <p v-if="oppStore.opponentsideusername==='NO GAME INITIATED'" class="playerinfo" style="font-size: 1.5em"><b>NO GAME INITIATED</b></p>
      <p v-else class="playerinfo">Playing Against: <b>{{oppStore.opponentsideusername}}</b> Time: {{displayFormattedTime(oppStore.timer)}}<br>Signed In As: <b>{{userStore.username}}</b> Time: {{displayFormattedTime(playerCards.timer)}}</p>
      <router-link to="/" v-slot="{href, route, navigate}">
        <p class="back-temp">Click to go back to MainPage.</p>
      </router-link>
      <button v-if="playerCards.showForfeitButton && !playerCards.showForfeit" @click="() => {
        playerCards.showForfeit = true
        playerCards.moveNotifier = 'Are you sure you want to forfeit?'
      }">
        Forfeit Game
      </button>
    </div>
  </div>
</template>

<style scoped>

.utilbar-component-div{
  display: flex;
  align-items: center;
  justify-content: space-evenly;
  flex-direction: row;
}

.utilbar-signed-in{
  width: 100%;
  height: fit-content;
}

.utilbar-component-div>.userform-temp{
  border: white .5vmin solid;
  background-color: #F28F3B;
  color: black;
  display: flex;
  flex-direction: column;
  position: absolute;
  height: fit-content;
  width: fit-content;
  justify-content: space-evenly;
  align-items: center;
  padding: 1vmin;
  gap: 1vh;
}

:deep(button){
  height: 80%;
  padding-top: .5%;
  padding-bottom: .5%;
}

.back-temp{
  position: relative;
  border: white 3px solid;
  color: white;
  padding: 0 .5em;
  line-height: 1.5em;
  margin: 0;
}
.back-temp:hover{
  border-color: black;
  font-style: italic;
}

.playerinfo{
  margin: auto 0;
  text-align: center;
  height: fit-content;
  max-width: 20vw;
  max-height: 2.2em;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.1;
}

.utilbar-signed-in > button{
  background: transparent;
  position: relative;
  border: white 3px solid;
  border-radius: 0;
  color: white;
  padding: 0 .5em;
  line-height: 1.5em;
  font-size: 1em;
  margin: 0;
}
.utilbar-signed-in > button:hover{
  border-color: black;
  font-style: italic;
}

</style>