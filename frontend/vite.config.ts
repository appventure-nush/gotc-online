import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  base: process.env.NODE_ENV === 'production'
      ? '/stuff/'
      : '/'
  ,

  /*
  build:{
    rollupOptions:{
      input:{
        main: resolve(__dirname, "index.html"),
        MainPage: resolve(__dirname, "MainPage/index.html"),
        NotVue: resolve(__dirname, "NotVue/index_notvue.html"),
      },
    },
  },
   */
})

