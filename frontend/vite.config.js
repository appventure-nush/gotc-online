import { defineConfig } from 'vite'
export default defineConfig({
    transpileDependencies: true,
    base: process.env.NODE_ENV === 'production'
        ? '/stuff/'
        : '/'

})
