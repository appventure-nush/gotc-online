<script lang="ts">
import {defineComponent} from 'vue'
import StackedCardHolder from "./StackedCardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";

export default defineComponent({
  name: "Defences",
  components: {StackedCardHolder},
  setup(){
    let playerStore = playerCardsStore
    return { playerStore }
  },
  computed:{
    civilDefenceList: function() {
      let cdl = this.playerStore.field.filter((card) => card.substring(0,5)==="civil")
      return cdl.length > 0 ? cdl : ["civil-placeholder"]
    },
    digitalDefenceList: function() {
      let ddl = this.playerStore.field.filter((card) => card.substring(0,7)==="digital")
      return ddl.length > 0 ? ddl : ["digital-placeholder"]
    },
    economicDefenceList: function() {
      let edl = this.playerStore.field.filter((card) => card.substring(0,8)==="economic")
      return edl.length > 0 ? edl : ["economic-placeholder"]
    },
    militaryDefenceList: function() {
      let mdl = this.playerStore.field.filter((card) => card.substring(0,8)==="military")
      return mdl.length > 0 ? mdl : ["military-placeholder"]
    },
    psychologicalDefenceList: function() {
      let pdl = this.playerStore.field.filter((card) => card.substring(0,13)==="psychological")
      return pdl.length > 0 ? pdl : ["psychological-placeholder"]
    },
    socialDefenceList: function() {
      let sdl = this.playerStore.field.filter((card) => card.substring(0,6)==="social")
      return sdl.length > 0 ? sdl : ["social-placeholder"]
    },
  }
})
</script>

<template>
  <div class="defences-component-div" >
    <!--
    played cards such as the crisis cards, community support and defence cards should be stored server side
    as they need to be displayed on opponent's end too
    later make it such that after every move we get the cards played from the backend and display it here
    when that's the case we can filter the defence card type according to the defence type as stated before the "-"
    -->
    <stacked-card-holder class="sch" :cards="civilDefenceList" :enable-play="false"/>
    <stacked-card-holder class="sch" :cards="digitalDefenceList" :enable-play="false"/>
    <stacked-card-holder class="sch" :cards="economicDefenceList" :enable-play="false"/>
    <stacked-card-holder class="sch" :cards="militaryDefenceList" :enable-play="false"/>
    <stacked-card-holder class="sch" :cards="psychologicalDefenceList" :enable-play="false"/>
    <stacked-card-holder class="sch" :cards="socialDefenceList" :enable-play="false"/>
  </div>
</template>

<style scoped>

.defences-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.sch{
  position: relative;
  height: 80%;
  aspect-ratio: 2/3;
  display: inline-block;
}


</style>