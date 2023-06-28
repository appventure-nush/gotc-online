import './style.css'
import typescriptLogo from './typescript.svg'
import { setupCounter } from './counter.js'
let BACKEND_URL = import.meta.env.VITE_BACKEND_URL
import {setupBackendMathForm} from "./backendmathform";
import {setupUserForm} from "./userform";

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
      <p>
        Enter in username below (test version for accounts)
      </p>
      <p id="username-info">
        Username is: 
      </p>
      <input id="username" type="text">
      <button id="submit-username" type="button">Submit username</button>
      <br>
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
  </div>
`

setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)
setupBackendMathForm(document.querySelector<HTMLDivElement>('#backend_calculation')!)
setupUserForm(document.querySelector<HTMLDivElement>('#userform')!)
