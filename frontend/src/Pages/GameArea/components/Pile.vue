<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";
import {userSignInStore} from "../../../components/UserSignInStore";

export default defineComponent({
  name: "Pile",
  components: {CardHolder},
  setup(){
    const playerCards = playerCardsStore
    return { playerCards }
  },
  data(){
    return{
      drawHover : false as boolean,
      discHover : false as boolean,
    }
  },
  computed:{
    drawRemainderOpacity : function () {
      return this.drawHover ? 1 : 0
    }
  },
  methods:{
    drawDeck(){
      if(userSignInStore.username !== "") playerCardsStore.drawDeck()
    }
  }
})
</script>

<template>

  <div class="pile-component-div">

    <div class="pile-component-card-wrapper" v-on:mouseover="drawHover=true" v-on:mouseout="drawHover=false">
      <CardHolder card-name="back-black" class="pile-component-card" rename-play="Draw" :enable-details="false" :play-button-func="drawDeck"/>
      <p class="draw-remainder">{{ playerCards.cardsLeft }} Left</p>
    </div>

    <div class="pile-component-card-wrapper" v-on:mouseover="discHover=true" v-on:mouseout="discHover=false">
      <CardHolder :card-name="playerCards.discardDeck[playerCards.discardDeck.length-1]" class="pile-component-card" :enable-play="false" :enable-details="false" />
    </div>


  </div>

</template>

<style scoped>

.pile-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.pile-component-card-wrapper{
  position: relative;
  width: 30%;
  height: 80%;
  display: inline-block;
}

.draw-remainder {
  position: absolute;
  height: 20%;
  width: 80%;
  left: 10%;
  text-align: center;
  padding: 0;
  top: 20%;
  display: block;
  opacity: v-bind(drawRemainderOpacity);
  transition: all .2s;
  pointer-events: none;
  background-color: rgba(0,0,0,0.7);
  line-height: 200%;
}

</style>