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
        background_user: '#6202EE',
        message_color: '#000000',
        icons_color: '#DADADA',
        text_main: '#1F1E21',
        text_second: '#6F6A75',
        smile_color: '#969696',
        back_button: '#757575',
        search: '#e0e0e0',
        sidebar_select: 'D7B7FD'
      },
      dark: {
        basic: '#D7B7FD',
        basic_text: '#D7B7FD',
        text_second: '#ffffff',
        background_main: '#141414',
        background_white: '#363636',
        background_user: '#1e1e1e',
        primary: '#6202EE',
        black: '#ffffff'
      }
    }
  }
})
