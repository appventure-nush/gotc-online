<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";
import {userSignInStore} from "../../../components/UserSignInStore";

export default defineComponent({
  name: "Hand",
  components: {CardHolder},
  setup(){
    //this imports the playerCardsStore, allowing us to use the variables stored within
    const playerCards = playerCardsStore
    const userStore = userSignInStore
    return { playerCards, userStore }
  },
  beforeMount() {
    // subscribing to the store makes the callback function within the $subscribe function run whenever the userStore updates
    // see more here: https://pinia.vuejs.org/core-concepts/state.html#Subscribing-to-the-state
    // we did not pass {detached:true} so this subssctiption automatically ends when we unmount
    // next time we can also check if a game's going on after checking if the user's signed in
    this.userStore.$subscribe(() => {
      if(this.userStore.isSignedIn) this.playerCards.getHand()
    })
  }
})
</script>

<!--
  This is the component that displays up to 7 cards in the player's hand

  Uses v-for to horizontally stack cardholders
  The hand itself is stored in the playerCards Store's handlist
  player logic can be attached to the CardHolder's playButtonFunc later
--->

<template>
  <div class="hand-component-div">
    <CardHolder v-for="(card,index) in playerCards.handList"
                :card-name="card"
                :key="card+index"
                :play-button-func="()=>{playerCards.playHand(index)}"
                class="handcard"
    />
  </div>

</template>

<style scoped>

.hand-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.handcard{
  position: relative;
  margin-left: .5%;
  margin-right: .5%;
  width: 10%;
  height: 80%;
  display: inline-block;
}

</style>