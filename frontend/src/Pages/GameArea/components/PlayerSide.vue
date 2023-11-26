<script lang="ts">
import {defineComponent} from 'vue'
import Hand from "./Hand.vue";
import Pile from "./Pile.vue";
import Crisis from "./Crisis.vue";
import UtilBar from "./UtilBar.vue";
import Defences from "./Defences.vue";
import CommunitySupports from "./CommunitySupports.vue";

export default defineComponent({
  name: "PlayerSide",
  components: {CommunitySupports, Defences, UtilBar, Crisis, Hand, Pile}
})
</script>

<template>
  <div>
    <Hand class="hand"/>
    <Pile class="pile"/>
    <Crisis class="crisis"/>
    <Defences class="defences"/>
    <CommunitySupports class="community-supports"/>
    <UtilBar class="utilbar"/>
  </div>
</template>

<style scoped>

.hand{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 45%;
  width: 75%;
  background-color: rgba(70,130,180,0.6);
}

.pile{
  position: absolute;
  bottom: 0;
  right: 0;
  height: 45%;
  width: 25%;
  background-color: rgba(70, 180, 130, 0.6);
}

.crisis{
  position: absolute;
  bottom: 45%;
  left: 0;
  height: 45%;
  width: 10%;
  background-color: rgba(180, 165, 70, 0.6);
}

.defences{
  position: absolute;
  bottom: 45%;
  left: 10%;
  height: 45%;
  width: 70%;
  background-color: rgba(119, 70, 180, 0.6);
}

.community-supports{
  position: absolute;
  bottom: 45%;
  right: 0;
  height: 45%;
  width: 20%;
  background-color: rgba(70, 180, 180, 0.6);
}

.utilbar{
  position: absolute;
  top: 0;
  left: 0;
  height: 10%;
  width: 100%;
  background: linear-gradient(to bottom,darkgray,grey);;
}



</style>