<script lang="ts">
/*
 This is the script section of a vue file
 A vue file usually has 3 parts to it.
 A script section for functionality code, a template section for defining the ui using html and a style section for css
 */

//since the counter button is a component (aka a UI element that can be used repeatedly), we use vue's defineComponent
import { defineComponent } from "vue"

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

//Here in the defineComponent function to be exported, we can define the methods and data and other functionality things
// that will be exported and used when using the counter vue component in other vue apps/components.
export default defineComponent({
  //This is the data section of a component
  //Vue is framework that is "reactive"
  //This probably means that the UI can be made sensitive to code and manual value setters needn't be called any longer
  //after changing the value of a variable.
  //So basically instead of having separate variables in code and in view, they are all one unified variable where changes
  //are reflected both ways
  data(){
    return{
      //here count is the number that is displayed in the button
      //it is also the same variable used to keep track of the count
      //so adding 1 to this will automatically change the text in the button
      //unlike in non vue where a value setter will be needed to reflect changes to the user
      //if you look at the html you will see "{{ count }}"
      //this means that whatever value the variable "count" from this data parameter has will be reflected in the ui
      count : 0 as number,
      //this is just a variable not displayed directly to the user
      //but it is used in code
      //and also used to compute the visibility/interactivity of the button
      username : "" as String,
    }
  },
  mounted() {
    //whatever code you write in this mounted function will run basically on start
    //read more about vue's lifecycle hooks here: https://vuejs.org/guide/essentials/lifecycle.html#lifecycle-diagram
    document.addEventListener("SignInEvent", this.onSignInEvent)
    document.addEventListener("SignOutEvent", this.onSignOutEvent)
  },
  computed:{
    //this computed area allows for immediate and on the go pre-processing of variables
    //for example
    //here we can create a variable "disable_count" that will tell the ui what state the counting machine is in
    //(whether someone is loggged in and therfore counting is enabled, or if there isnt anyone logged in
    //and the user has to br prompted to log in before counting)
    //this disable count stores the truth value of whether the username field is blank (and therfore nobody is signed in)
    //or if the username field is not blank and someone is signed in
    //we can then bind this variable to a v-if in 2 buttons (see the template area below) to decide which button to show
    //whether it be the enabled counting button that will count and send requests to the server
    //or the disabled sign in prompting button
    //whenever username is changed, this fucntion is automatically run to update disable_count variable
    disable_count: function (){
      return this.username === ""
    }
  },
  methods:{

    advanceCounter(){
      //this advances the count variable by one
      //after the change in the count variable, vue automatically updates all ui elements that show this count variable
      //or otherwise depend on this count variable for other purposes
      this.count++

      //standard updating server code, nothing really vue-related here
      fetch(`${BACKEND_URL}/set_counter`, {
        method: "POST",
        body: JSON.stringify({
          username: this.username,
          value : this.count
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
    },

    async onSignInEvent(SIEvent : { detail: string; }){
      this.username = SIEvent.detail

      this.count =
          await fetch(`${BACKEND_URL}/get_counter`, {
            method: "POST",
            body: JSON.stringify({
              username: this.username
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
          })
              .then((response) => response.json())
              .then((data) => parseInt(data))

    },

    onSignOutEvent(){
      //upon signing out,
      //the username is set to blank
      //this will automatically update the computed variable disable_count to true
      this.username = ""
    }


  }
})
</script>

<template>
  <!--
  This is the counting button, if counting is not enabled, it will not show due to the v-if binding
  since v-if is bound to !disable_count, when the computed variable disable_count is automatically set to false,
  due to it being a computed variable based on the state of the username data variable,
  (namely we have defined this computed variable to be false when username is anything but an empty string)
  v-if of this button will be !false = true which means this element will be shown

  opposite case for the Sign in first button.
   -->
  <button v-if="!disable_count" type="button" @click="advanceCounter" :disabled="disable_count">count is {{ count }}</button>
  <button v-if="disable_count" type="button" :disabled="disable_count">Sign in first.</button>
</template>

<style scoped>

</style>