import './style.css'
import typescriptLogo from './typescript.svg'
import { setupCounter } from './counter.js'
import serverURL from './backend_address.txt'
import {setupBackendMathForm} from "./backendmathform";

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
      <button id="counter" type="button"></button>
    </div>
    <p class="read-the-docs">
      Click on the Vite and TypeScript logos to learn more
    </p>
    <p class="oran-berry-disc">
      Image below is fetched from backend
    </p>
    <a href="${serverURL}/get_image" target="_blank">
      <img src="${serverURL}/get_image" class="logo vanilla" alt="Test Image From backend. (if you see this text it's possible that you did not turn on backend)" />
    </a>
    <div id="backend_calculation" class="backend-calculation"></div>    
  </div>
`

setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)
setupBackendMathForm(document.querySelector<HTMLDivElement>('#backend_calculation')!)
