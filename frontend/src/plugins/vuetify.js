import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        basic: '#6202EE',
        background_pink: '#F2E7FE',
        background_search: '#EBEBEB',
        background_main: '#F2F2F2',
        background_white: '#FFFFFF',
        message_color: '#000000',
        icons_color: '#DADADA',
        text_main: '#1F1E21',
        text_second: '#6F6A75',
        smile_color: '#969696'
      }
    }
  }
})
