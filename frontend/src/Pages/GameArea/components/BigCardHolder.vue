<script lang="ts">
import {defineComponent} from 'vue'
import {expandButtonStore} from "./ExpandButtonStore";

export default defineComponent({
  name: "BigCardHolder",
  setup(){
    const ebs = expandButtonStore
    return {ebs}
  },
  methods:{
    cancelBig(){
      this.ebs.expand = false
      console.log(expandButtonStore.expand)
    }
  }

})
</script>

<template>
  <div class="bigcardholder" v-if="ebs.expand">
    <img :src="ebs.imageSrc" :alt="ebs.imageSrc"/>
    <button @click="cancelBig()" >X</button>
  </div>
</template>

<style scoped>

.bigcardholder {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  align-items: center;
  background-color: transparent;
}
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

</style>