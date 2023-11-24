<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";

export default defineComponent({
  name: "Hand",
  components: {CardHolder},
  setup(){
    //this imports the playerCardsStore, allowing us to use the variables stored within
    const playerCards = playerCardsStore
    return { playerCards }
  },
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
    <CardHolder v-for="(card,index) in playerCards.handList" :card-name="card" :key="card+index" class="handcard"/>
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
  width: 9%;
  height: 80%;
  display: inline-block;
}

</style>