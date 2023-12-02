<script lang="ts">
import {defineComponent} from 'vue'
import {expandButtonStore} from "./ExpandButtonStore";

export default defineComponent({
  name: "BigCardHolder",
  setup(){
    //import the store so we may use the variables within
    const ebs = expandButtonStore
    return {ebs}
  },
  methods:{
    cancelBig(){
      // dismisses the enlarged card
      this.ebs.expand = false
      console.log(expandButtonStore.expand)
    }
  }

})
</script>

<!--
  This component will show when the user requests "details" on a card.

  The trigger for it to show is the expand variable in the ExpandButton Store
  It shows whatever image it's linked to in the ExpandButton Store's image src variable
  To dismiss it the X button sets the expand variable to false
-->

<template>

  <div class="bigcardholder" v-if="ebs.expand">
    <img :src="ebs.imageSrc" :alt="ebs.imageSrc"/>
    <button @click="cancelBig()" >X</button>
  </div>
</template>

<style scoped>

.bigcardholder>img{
  position: absolute;
  height: 100%;
  width: 90%;
  top: 0;
  left: 0;
  object-fit: fill;
  display: block;
}
.bigcardholder>button{
  position: absolute;
  height: 3em;
  width: 10%;
  top: 0;
  right: 0;
  display: block;
}

.bigcardholder{
  position: absolute;
  height: 80vh;
  width: 40vw;
  top: 10vh;
  left: 30vw;
  display: inline-block;
  align-items: center;
  background-color: transparent;
}


</style>