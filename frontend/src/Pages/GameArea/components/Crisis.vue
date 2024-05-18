<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";
import {userSignInStore} from "../../../components/UserSignInStore";

export default defineComponent({
  name: "Crisis",
  components: {CardHolder},
  setup() {
    let playerStore = playerCardsStore
    let userStore = userSignInStore


    return {playerStore, userStore}
  },
  beforeMount() {
    // subscribing to the store makes the callback function within the $subscribe function run whenever the userStore updates
    // see more here: https://pinia.vuejs.org/core-concepts/state.html#Subscribing-to-the-state
    // we did not pass {detached:true} so this subscription automatically ends when we unmount
    // next time we can also check if a game's going on after checking if the user's signed in
    this.userStore.$subscribe(() => {
      if(this.userStore.isSignedIn) this.playerStore.getCrisis()
      else this.playerStore.crisis = "back-white"
    })
  },
  methods:{
    newCrisis: function (){
      this.playerStore.newCrisis()
    }
  },
})
</script>

<template>
  <div class="crisis-component-div">
    <p class="cards-left">{{playerStore.playersideusername}}: {{playerStore.cardsLeft}} Cards Left</p>
    <CardHolder :card-name="playerStore.crisis" class="crisiscard" :enable-play="false" />
  </div>
</template>

<style scoped>

.crisis-component-div{
  background-color: transparent;
  display: inline-flex;
  justify-content: space-evenly;
  align-items: center;
}

.crisis-component-div>.crisiscard{
  position: absolute;
  height: 60%;
  aspect-ratio: 2/3;
  bottom: 10%;
  display: block;
}

.crisis-component-div>.cards-left{
  position: absolute;
  width: 80%;
  margin: 0 0 2.5%;
  top: 10%;
  display: block;
  text-align: center;
  white-space: nowrap;
  background: linear-gradient(to bottom, dimgrey, darkslategrey);
  color: white;
  font-weight: 600;
  font-size: 1.25em;
  padding: .25em .25em;
  line-height: 1.2em;
  overflow-y: auto;
}

.crisiscard {
  position: relative;
  height: 80%;
  aspect-ratio: 2/3;
  display: inline-block;
  margin: auto;
}

</style>