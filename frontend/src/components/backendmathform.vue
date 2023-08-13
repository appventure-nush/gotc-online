<script lang="ts">

import { defineComponent } from "vue"

let BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent({
  data() {
    return {
      math_input: 0 as Number,
      result: "waiting for input" as String,
    }
  }
  ,
  methods:{

    submit_math(_event : Event){
      this.setResult("waiting for result...")
      // send a post request to the calculate part of the backend
      // body of post request is a json
      // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
      fetch(`${BACKEND_URL}/calculate`, {
        method: "POST",
        body: JSON.stringify({
          userId: 1,
          title: "Fix my bugs",
          completed: false,
          value : this.math_input
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
          // this results in a response promise that promises some sort of response
          // will be received from where the post was sent to

          // this converts the response promise into a string promise apparently
          // (resulting string should be the html text send by the flask)
          .then((response) => {
            if(!response.ok) return Promise.reject(response)
            else return response.text()
          })

          // promised string response is sent to set result
          .then((text) => {
            this.setResult(text)
          })
          .catch(error => {
            this.setResult(error)
          });
    },
    setResult(value : string){
      // update result variable and result element
      // (vue can automatically update element when variable is updated im too lazy to find out how to use vue)
      // plain vite seems to work anyway so I ain't complaining
      this.result  = value
      //element.querySelector<HTMLParagraphElement>("#calculation_result")!.innerHTML = result
    },

  },
})

</script>

<template>
  <input type="number" id = "cnum" v-model.number="math_input" />
  <button type="submit" id = "butt" @click="submit_math">backend math</button>
  <p style="border: white; border-width: 5px" id = "calculation_result">{{ result }}</p>
</template>

<style scoped>


</style>