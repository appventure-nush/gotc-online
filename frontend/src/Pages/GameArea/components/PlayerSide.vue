<script lang="ts">
import {defineComponent} from 'vue'
import Hand from "./Hand.vue";
import Pile from "./Pile.vue";
import Crisis from "./Crisis.vue";
import UtilBar from "./UtilBar.vue";
import Defences from "./Defences.vue";
import CommunitySupports from "./CommunitySupports.vue";
import {playerCardsStore} from "./PlayerCardsStore";

export default defineComponent({
  name: "PlayerSide",
  components: {CommunitySupports, Defences, UtilBar, Crisis, Hand, Pile},
  computed:{
    handBGColor() {
      return ((playerCardsStore.showOptionHand || playerCardsStore.showDialogHand) && !playerCardsStore.vetoShowOpponentHand) ? "#588B8B" : "#F28F3B"
    }
  }
})
</script>

<template>
  <div>
    <Hand class="hand"/>
    <div class="separator s3"/>
    <Pile class="pile"/>
    <Crisis class="crisis"/>
    <div class="separator s1"/>
    <Defences class="defences"/>
    <div class="separator s2"/>
    <CommunitySupports class="community-supports"/>
    <UtilBar class="utilbar"/>
  </div>
</template>

<style scoped>

*{
 font-size: 2vh;
}

.separator{
  position: absolute;
  background-color: grey;
  height: 45%;
  width: .1%;
}
.s1{
  background: linear-gradient(0deg, #FFD5C2 0%, #FFD5C2 5%, white 5%, white 95%, #FFD5C2 95%, #FFD5C2 100%);
  top: 10%;
  left: 12.5%;
}
.s2{
  background: linear-gradient(0deg, #FFD5C2 0%, #FFD5C2 5%, white 5%, white 95%, #FFD5C2 95%, #FFD5C2 100%);
  top: 10%;
  right: 12.5%;
}
.s3{
  background: linear-gradient(0deg, #F28F3B 0%, #F28F3B 5%, #FFD5C2 5%, #FFD5C2 95%, #F28F3B 95%, #F28F3B 100%);
  bottom: 0;
  right: 20%;
}


.hand{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 45%;
  width: 80%;
  background-color: v-bind(handBGColor);
}

.pile{
  position: absolute;
  bottom: 0;
  right: 0;
  height: 45%;
  width: 20%;
  background-color: #F28F3B;
}

.crisis{
  position: absolute;
  bottom: 45%;
  left: 0;
  height: 45%;
  width: 12.5%;
  background-color: #FFD5C2;
}

.defences{
  position: absolute;
  bottom: 45%;
  left: 12.6%;
  height: 45%;
  width: 74.8%;
  background-color: #FFD5C2;
}

.community-supports{
  position: absolute;
  bottom: 45%;
  right: 0;
  height: 45%;
  width: 12.5%;
  background-color: #FFD5C2;
}

.utilbar{
  position: absolute;
  top: 0;
  left: 0;
  height: 10%;
  width: 100%;
  background: grey;
  font-size: 2vh;
}



</style>