<script lang="ts">
import {defineComponent} from 'vue'
import { expandButtonStore } from "./ExpandButtonStore";


export default defineComponent({
  name: "CardHolder",
  props: {
    cardName : {
      type : String,
      required: true,
      validator(value : string){
        return [
          "back-black",
          "back-white",
          "civil-1",
          "civil-2",
          "civil-3",
          "communitysupport",
          "crisis-1",
          "crisis-2",
          "crisis-3",
          "crisis-4",
          "crisis-5",
          "crisis-6",
          "digital-1",
          "digital-2",
          "digital-3",
          "economic-1",
          "economic-2",
          "economic-3",
          "economic-4",
          "economic-5",
          "event-1",
          "event-10",
          "event-11",
          "event-12",
          "event-2",
          "event-3",
          "event-4",
          "event-5",
          "event-6",
          "event-7",
          "event-8",
          "event-9",
          "instructions-1",
          "instructions-2",
          "instructions-3",
          "instructions-4",
          "military-1",
          "military-2",
          "military-3",
          "military-4",
          "psychological-1",
          "psychological-2",
          "psychological-3",
          "social-1",
          "social-2",
          "social-3",
        ].includes(value)
      }
    },
    enableDetails : {
      type : Boolean,
      default : true
    },
    enablePlay : {
      type : Boolean,
      default : true
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
  setup(){
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
    const expButtonStore = expandButtonStore
    return{ BACKEND_URL, expButtonStore }
  },
  data(){
    return{
      cardHover : false as boolean,
    }
  },
  computed:{
    cardImgSrc : function (){
      return this.BACKEND_URL+'/get_card?cardname='+this.cardName
    },

    overlayOpacity : function () {
      return this.cardHover? 1 : 0
    }
  },
  methods:{
    expandButton(){
      this.expButtonStore.expand = true
      this.expButtonStore.imageSrc = this.cardImgSrc
      //console.log(expandButtonStore().expand)
    }
  }
})
</script>

<template>

  <div class="cardholder">
    <img :src="cardImgSrc" :alt="cardName" />
    <div v-if="enableOverlay" class="card-overlay" v-on:mouseover="cardHover=true" v-on:mouseout="cardHover=false">
      <button v-if="enableDetails" class="card-button details" @click="expandButton()" >Details</button>
      <button v-if="enablePlay" class="card-button play" @click="playButtonFunc!()" >{{ renamePlay }}</button>
    </div>

  </div>

</template>

<style scoped>

.cardholder {
  display: flex;
  height: 100%;
  width: 100%;
  position: absolute;
}
.cardholder>img{
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  object-fit: fill;
}

.card-overlay {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background-color: rgba(0,0,0,0.5);
  opacity: v-bind(overlayOpacity);
  transition: all .2s;
}

.card-button {
  position: absolute;
  height: 20%;
  width: 80%;
  left: 10%;
  display: block;
  text-align: center;
  padding: 0;
}
.details{
  top: 20%;
}
.play{
  top: 60%;
}



</style>