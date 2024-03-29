/*
THIS CODE IS NOW DEPRECATED
Since this project is going to use the Vue 3 framework from now on, this code has been converted to its vue equivilant
and is now deprecated.
 */

import '../style.css'
import typescriptLogo from '../typescript.svg'
import { setupCounter } from './counter'
let BACKEND_URL = import.meta.env.VITE_BACKEND_URL
import {setupBackendMathForm} from "./backendmathform";
import {setupUserForm} from "./userform"

document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
  <div>
    <a href="https://vitejs.dev" target="_blank">
      <img src="./vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://www.typescriptlang.org/" target="_blank">
      <img src="${typescriptLogo}" class="logo vanilla" alt="TypeScript logo" />
    </a>
    <h1>Vite + TypeScript</h1>
    <div class="card">
      <button id="counter" type="button">Did you run the backend?</button>
    </div>
    <p class="read-the-docs">
      Click on the Vite and TypeScript logos to learn more
    </p>
    <p class="oran-berry-disc">
      Image below is fetched from backend
    </p>
    <a href="${BACKEND_URL}/get_image" target="_blank">
      <img src="${BACKEND_URL}/get_image" class="logo vanilla" alt="Test Image From backend. (if you see this text it's possible that you did not turn on backend)" />
    </a>
    <div id="backend_calculation" class="backend-calculation"></div>   
    <div id="userform" class="userform"></div>  
   <p class="oran-berry-disc" id="foo">
      no sign in happened
    </p>
  </div>
`

setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)
setupBackendMathForm(document.querySelector<HTMLDivElement>('#backend_calculation')!)
setupUserForm(document.querySelector<HTMLDivElement>('#userform')!)
//listens for sign in event emitted by userform on document
document.addEventListener(
    "SignInEvent",
    function(e: { detail: string; }) {
        console.log("Sign in happened")
        document.querySelector<HTMLDivElement>('#foo')!.innerHTML = "Sign in happened with username " + e.detail
    }.bind(this)
)
//listens for sign out event emitted by userform on document
document.addEventListener(
    "SignOutEvent",
    function() {
        console.log("Sign out happened")
        document.querySelector<HTMLDivElement>('#foo')!.innerHTML = "Sign out happened "
    }.bind(this)
)
