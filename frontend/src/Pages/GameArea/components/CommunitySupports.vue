<script lang="ts">
import {defineComponent} from 'vue'
import StackedCardHolder from "./StackedCardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";

export default defineComponent({
  name: "CommunitySupports",
  components: {StackedCardHolder},
  setup(){
    let playerStore = playerCardsStore
    return { playerStore }
  },
  computed:{
    communitySupportList: function () {
      let csl = this.playerStore.field.filter((card) => card.substring(0,16)==="communitysupport")
      return csl.length > 0 ? csl : ["communitysupport-placeholder"]
    }
  }
})
</script>

<template>
  <div class="cs-component-div" >
    <stacked-card-holder class="community-support-stack" :cards=communitySupportList :enable-play=false />
  </div>
</template>

<style scoped>

.cs-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}
.cs-component-div>.community-support-stack{
  position: relative;
  margin-left: .5%;
  margin-right: .5%;
  width: 70%;
  height: 80%;
  display: inline-block;
}

</style>