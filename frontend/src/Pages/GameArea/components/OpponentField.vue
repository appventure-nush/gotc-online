<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {opponentFieldStore} from "./OpponentFieldStore";
import StackedCardHolder from "./StackedCardHolder.vue";

export default defineComponent({
  name: "OpponentField",
  components: {StackedCardHolder, CardHolder},
  setup(){
    let opponentStore = opponentFieldStore
    return { opponentStore }
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
                           :block-play="civilDefenceList.length < 1"
      />
      <stacked-card-holder class="sch"
                           :cards="digitalDefenceList.length > 0 ? digitalDefenceList : ['digital-placeholder']"
                           rename-play="Discard"
                           :block-play="digitalDefenceList.length < 1"
      />
      <stacked-card-holder class="sch"
                           :cards="economicDefenceList.length > 0 ? economicDefenceList : ['economic-placeholder']"
                           rename-play="Discard"
                           :block-play="economicDefenceList.length < 1"
      />
      <stacked-card-holder class="sch"
                           :cards="militaryDefenceList.length > 0 ? militaryDefenceList : ['military-placeholder']"
                           rename-play="Discard"
                           :block-play="militaryDefenceList.length < 1"
      />
      <stacked-card-holder class="sch"
                           :cards="psychologicalDefenceList.length > 0 ? psychologicalDefenceList : ['psychological-placeholder']"
                           rename-play="Discard"
                           :block-play="psychologicalDefenceList.length < 1"
      />
      <stacked-card-holder class="sch"
                           :cards="socialDefenceList.length > 0 ? socialDefenceList : ['social-placeholder']"
                           rename-play="Discard"
                           :block-play="socialDefenceList.length < 1"
      />
    </div>
    <div class="opponent-comunity-support">
      <stacked-card-holder class="community-support-stack"
                           :cards="communitySupportList > 0 ? communitySupportList : ['communitysupport-placeholder']"
                           rename-play="Discard"
                           :block-play="communitySupportList.length < 1"
      />
    </div>
    <div class="opponent-discard">
      <stacked-card-holder class="opponent-discard-stack"
                           :cards="opponentStore.discard"
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