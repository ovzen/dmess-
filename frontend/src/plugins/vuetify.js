import '@mdi/font/css/materialdesignicons.css'
import Vue from 'vue'
import Vuetify from 'vuetify/lib'

Vue.use(Vuetify)

export default new Vuetify({
  theme: {
    themes: {
      light: {
        basic: '#6202EE',
        basic_text: '#6202EE',
        background_pink: '#F2E7FE',
        background_search: '#EBEBEB',
        background_main: '#F2F2F2',
        background_white: '#FFFFFF',
        background_grey: '#808080',
        message_color: '#000000',
        icons_color: '#DADADA',
        text_main: '#1F1E21',
        text_second: '#6F6A75',
        smile_color: '#969696'
      },
      dark: {
        basic_text: '#6202EE',
        text_second: '#ffffff',
        background_main: '#141414',
        background_white: '#363636',
        primary: '#6202EE'
      }
    }
  }
})
