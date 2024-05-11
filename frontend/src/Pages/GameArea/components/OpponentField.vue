<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {opponentFieldStore} from "./OpponentFieldStore";
import { playerCardsStore } from './PlayerCardsStore';
import StackedCardHolder from "./StackedCardHolder.vue";

export default defineComponent({
  name: "OpponentField",
  components: {StackedCardHolder, CardHolder},
  setup(){
    let playerCards = playerCardsStore
    let opponentStore = opponentFieldStore
    return { playerCards, opponentStore }
  },
  computed:{
    civilDefenceList: function() {
      return this.opponentStore.field.filter((card) => card.substring(0, 5) === "civil")
    },
    digitalDefenceList: function() {
      return this.opponentStore.field.filter((card) => card.substring(0, 7) === "digital")
    },
    economicDefenceList: function() {
      return this.opponentStore.field.filter((card) => card.substring(0, 8) === "economic")
    },
    militaryDefenceList: function() {
      return this.opponentStore.field.filter((card) => card.substring(0, 8) === "military")
    },
    psychologicalDefenceList: function() {
      return this.opponentStore.field.filter((card) => card.substring(0, 13) === "psychological")
    },
    socialDefenceList: function() {
      return this.opponentStore.field.filter((card) => card.substring(0, 6) === "social")
    },
    communitySupportList: function () {
      return this.opponentStore.field.filter((card) => card.substring(0, 16) === "communitysupport")
    },
    clickfunction : function () { // yes, this is a triple nested function
      return (which: string) => {return (key: number) => {return () => {
        if (this.playerCards.showOptionDefence) {
          // if only 1 card
          if (this.opponentStore.field.length - this.communitySupportList.length == 1) {
            this.playerCards.playHand(this.playerCards.index, [which, key])
            this.playerCards.showOptionDefence = false
          } else {
            this.playerCards.selectionDefence = [which, key]
            this.playerCards.showOptionDefence = false
            this.playerCards.showOptionDefence2 = true
          }
        } else if (this.playerCards.showOptionDefence2) {
          // make sure no duplicates first
          if (which == this.playerCards.selectionDefence[0] && key == this.playerCards.selectionDefence[1]) {
            this.playerCards.moveNotifier = "Do not select the same card again."
          } else {
            this.playerCards.showOptionDefence2 = false
            this.playerCards.playHand(this.playerCards.index, this.playerCards.selectionDefence, [which, key])
            this.playerCards.selectionDefence = []
          }
        } else if (this.playerCards.showOptionField) {
          this.playerCards.showOptionField = false
          this.playerCards.playHand(this.playerCards.index, [which, key])
        }
      }}}
    }
  }
})
</script>

<template>
  <div class="oppfield-component-div">
    <div class="opponent-crisis">
      <p class="cards-left">{{opponentStore.cardsLeft}} Cards Left</p>
      <CardHolder :card-name="opponentStore.crisis" class="crisiscard" :enable-play="false" />
    </div>
    <div class="opponent-defence">
      <stacked-card-holder class="sch"
                           :cards="civilDefenceList.length > 0 ? civilDefenceList : ['civil-placeholder']"
                           rename-play="Discard"
                           :enable-play="civilDefenceList.length > 0 &&
                             (playerCards.showOptionDefence2 || playerCards.showOptionDefence || playerCards.showOptionField)
                             && playerCards.canClickEndTurn"
                           :play-button-func="clickfunction('civil')"
      />
      <stacked-card-holder class="sch"
                           :cards="digitalDefenceList.length > 0 ? digitalDefenceList : ['digital-placeholder']"
                           rename-play="Discard"
                           :enable-play="digitalDefenceList.length > 0 &&
                             (playerCards.showOptionDefence2 || playerCards.showOptionDefence || playerCards.showOptionField)
                             && playerCards.canClickEndTurn"
                           :play-button-func="clickfunction('digital')"
      />
      <stacked-card-holder class="sch"
                           :cards="economicDefenceList.length > 0 ? economicDefenceList : ['economic-placeholder']"
                           rename-play="Discard"
                           :enable-play="economicDefenceList.length > 0 &&
                             (playerCards.showOptionDefence2 || playerCards.showOptionDefence || playerCards.showOptionField)
                             && playerCards.canClickEndTurn"
                           :play-button-func="clickfunction('economic')"
      />
      <stacked-card-holder class="sch"
                           :cards="militaryDefenceList.length > 0 ? militaryDefenceList : ['military-placeholder']"
                           rename-play="Discard"
                           :enable-play="militaryDefenceList.length > 0 &&
                             (playerCards.showOptionDefence2 || playerCards.showOptionDefence || playerCards.showOptionField)
                             && playerCards.canClickEndTurn"
                           :play-button-func="clickfunction('military')"
      />
      <stacked-card-holder class="sch"
                           :cards="psychologicalDefenceList.length > 0 ? psychologicalDefenceList : ['psychological-placeholder']"
                           rename-play="Discard"
                           :enable-play="psychologicalDefenceList.length > 0 &&
                             (playerCards.showOptionDefence2 || playerCards.showOptionDefence || playerCards.showOptionField)
                             && playerCards.canClickEndTurn"
                           :play-button-func="clickfunction('psychological')"
      />
      <stacked-card-holder class="sch"
                           :cards="socialDefenceList.length > 0 ? socialDefenceList : ['social-placeholder']"
                           rename-play="Discard"
                           :enable-play="socialDefenceList.length > 0 &&
                             (playerCards.showOptionDefence2 || playerCards.showOptionDefence || playerCards.showOptionField)
                             && playerCards.canClickEndTurn"
                           :play-button-func="clickfunction('social')"
      />
    </div>
    <div class="opponent-comunity-support">
      <stacked-card-holder class="community-support-stack"
                           :cards="communitySupportList.length > 0 ? communitySupportList : ['communitysupport-placeholder']"
                           rename-play="Discard"
                           :enable-play="communitySupportList.length > 0 && playerCards.showOptionField && playerCards.canClickEndTurn"
                           :play-button-func="clickfunction('communitysupport')"
      />
    </div>
    <div class="opponent-discard">
      <stacked-card-holder class="opponent-discard-stack"
                           :cards="opponentStore.discard.length > 0 ? opponentStore.discard: ['discard-placeholder']"
                           :enable-play = "false"
      />
    </div>
  </div>
</template>

<style scoped>

.oppfield-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.opponent-crisis{
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  width: 10%;
  background-color: transparent;
  display: inline-flex;
  justify-content: space-evenly;
  align-items: center;
}
.opponent-crisis>.crisiscard{
  position: absolute;
  height: 60%;
  aspect-ratio: 2/3;
  bottom: 10%;
  display: block;
}
.opponent-crisis>.cards-left{
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
  padding: .25em 0;
}

.opponent-defence{
  position: absolute;
  top: 0;
  left: 10%;
  height: 100%;
  width: 70%;
  background-color: transparent;
  display: inline-flex;
  justify-content: space-evenly;
  align-items: center;
}
.opponent-defence>.sch{
  position: relative;
  height: 80%;
  aspect-ratio: 2/3;
  display: inline-block;
}

.opponent-comunity-support{
  position: absolute;
  top: 0;
  right: 11%;
  height: 100%;
  width: 10%;
  background-color: transparent;
  display: inline-flex;
  justify-content: space-evenly;
  align-items: center;
}
.opponent-comunity-support>.community-support-stack{
  position: relative;
  height: 80%;
  aspect-ratio: 2/3;
  display: inline-block;
}

.opponent-discard{
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  width: 10%;
  background-color: transparent;
  display: inline-flex;
  justify-content: space-evenly;
  align-items: center;
}
.opponent-discard>.opponent-discard-stack{
  position: relative;
  height: 80%;
  aspect-ratio: 2/3;
  display: inline-block;
}



</style>