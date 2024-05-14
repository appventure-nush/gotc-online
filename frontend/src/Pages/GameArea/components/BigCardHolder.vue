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
  aspect-ratio: 6/8.5;
  top: 0;
  left: 0;
  object-fit: fill;
  display: block;
}
.bigcardholder>button{
  position: absolute;
  height: 2em;
  aspect-ratio: 1;
  top: 0;
  right: 0;
  display: block;
  border: white solid 3px;
  background-color: black;
  font-weight: bold;
  font-size: 1.5em;
  padding: 0;
}

.bigcardholder{
  position: absolute;
  height: 80vh;
  width: 62vh;
  max-width: 53vw;
  max-height: 60vw;
  top: 10vh;
  left: 35vw;
  display: inline-block;
  background-color: transparent;
}


</style>