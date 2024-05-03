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
  setup(){
    //import the backend url here so that we may use it
    //setup is part of the vue lifecycle, go read up about it
    const BACKEND_URL = import.meta.env.VITE_BACKEND_URL
    //import the store so we may use the variables within
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
      // constructs the src url for te card, served by backend function
      return this.BACKEND_URL+'/get_card?cardname='+this.cardName
    },

    overlayOpacity : function () {
      // controls the opacity of the overlay buttons & div if they exist
      return this.cardHover? 1 : 0
    }
  },
  methods:{
    expandButton(){
      // enables the enlarged card view
      this.expButtonStore.expand = true
      this.expButtonStore.imageSrc = this.cardImgSrc
      //console.log(expandButtonStore().expand)
    }
  }
})
</script>

<!--
  This is the component that displays each individual card

  When hovering over the card, two buttons can appear, both can be disabled by passing values to props.
  The card also dims via the appearance of a partially transparent grey overlay, this can also be disabled by passing a prop value.
  Details button has only one use, to magnify the card when clicked.
  Play button can be customised to run a function passed into the playButtonFunc prop.
--->

<template>

  <div class="cardholder">
    <img :src="cardImgSrc" :alt="cardName" />
    <div v-if="enableOverlay" class="card-overlay" v-on:mouseover="cardHover=true" v-on:mouseout="cardHover=false">
      <button v-if="enableDetails" class="card-button details" @click="expandButton()" >Details</button>
      <button v-if="enablePlay" :disabled="blockPlay" class="card-button play" @click="playButtonFunc!()" >{{ renamePlay }}</button>
    </div>

  </div>

</template>

<style scoped>


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