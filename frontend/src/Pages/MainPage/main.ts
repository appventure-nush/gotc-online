import { createApp } from 'vue'
import '../../style.css'
import App from './MainPageApp.vue'

export function startMainPage() {
    createApp(App).mount('#app')
}