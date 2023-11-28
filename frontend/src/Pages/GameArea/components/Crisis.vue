<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";
import {userSignInStore} from "../../../components/UserSignInStore";

export default defineComponent({
  name: "Crisis",
  components: {CardHolder},
  setup() {
    let playerStore = playerCardsStore
    let userStore = userSignInStore


    return {playerStore, userStore}
  },
  beforeMount() {
    // subscribing to the store makes the callback function within the $subscribe function run whenever the userStore updates
    // see more here: https://pinia.vuejs.org/core-concepts/state.html#Subscribing-to-the-state
    // we did not pass {detached:true} so this subssctiption automatically ends when we unmount
    this.userStore.$subscribe(() => {
      if(this.userStore.isSignedIn) this.playerStore.getCrisis()
      else this.playerStore.crisis = "back-white"
    })
  },
  methods:{
    newCrisis: function (){
      this.playerStore.newCrisis()
    }
  },
})
</script>

<template>

  <div class="crisis-component-div">
    <CardHolder :card-name="playerStore.crisis" class="crisiscard" :enable-play="false" />
  </div>
</template>

<style scoped>

.crisis-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}
.crisiscard{
  position: relative;
  margin-left: .5%;
  margin-right: .5%;
  width: 70%;
  height: 80%;
  display: inline-block;
}

</style>