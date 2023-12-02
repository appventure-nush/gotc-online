<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";

export default defineComponent({
  name: "StackedCardHolder",
  components: {CardHolder},
  props:{
    cards : {
      type: Array,
      default: ["back-black", "back-white"]
    },
    enableDetails : {
      type : Boolean,
      default : true
    },
    enablePlay : {
      type : Boolean,
      default : true
    },
    blockPlay : {
      type : Boolean,
      default : false
    },
    renamePlay : {
      type : String,
      default : "Play"
    },
    playButtonFunc : {
      type : Function,
      default() {

      }
    },
    enableOverlay : {
      type : Boolean,
      default : true
    },
  },
  data(){
    return{
      cardHover : false as boolean,
    }
  },
  computed: {
    overflowBehavior: function (){
      return (this.cardHover && this.cards.length>1) ? 'auto' : 'clip'
    }
  },
  methods: {
  }
})
</script>

<template>
  <div class="stackedcardholder-component-div" v-on:mouseover="cardHover=true" v-on:mouseout="cardHover=false" v-on:mouseenter="this.$refs.SCHDiv.scrollTop = 0" ref="SCHDiv">
    <card-holder v-for="(val,key) in cards"
                 v-bind:card-name="val" class="stackedcard"
                 v-bind:style="cardHover?'top:0':'top:'+(-90*key)+'%'"
                 :enable-details="this.enableDetails"
                 :enable-play="this.enablePlay"
                 :block-play="this.blockPlay"
                 :rename-play="this.renamePlay"
                 :play-button-func="this.playButtonFunc"
                 :enable-overlay="this.enableOverlay"
    />
  </div>
</template>

<style scoped>

.stackedcardholder-component-div{
  display: block;
  align-items: center;
  justify-content: space-evenly;
  overflow: v-bind(overflowBehavior);
  scrollbar-width: thin;
}

.stackedcard{
  position: relative;
  width: 100%;
  height: 100%;
  display: inline-block;
  transition: top .5s;
}

</style>