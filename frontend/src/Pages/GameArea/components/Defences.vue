<script lang="ts">
import {defineComponent} from 'vue'
import StackedCardHolder from "./StackedCardHolder.vue";

export default defineComponent({
  name: "Defences",
  components: {StackedCardHolder}
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
    <stacked-card-holder class="sch civil-stack" :cards="['civil-1','civil-2','civil-3']"/>
    <stacked-card-holder class="sch digital-stack" :cards="['digital-1','digital-2','digital-3']"/>
    <stacked-card-holder class="sch economic-stack" :cards="['economic-1','economic-2','economic-3','economic-4','economic-5']"/>
    <stacked-card-holder class="sch military-stack" :cards="['military-1','military-2','military-3','military-4']"/>
    <stacked-card-holder class="sch psychological-stack" :cards="['psychological-1','psychological-2','psychological-3']"/>
    <stacked-card-holder class="sch social-stack" :cards="['social-1','social-2','social-3']"/>
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
  width: 15%;
  height: 80%;
  display: inline-block;
}


</style>