
const BundleTracker = require('webpack-bundle-tracker')

if (process.env.NODE_ENV === 'production') {
  module.exports = {
    'transpileDependencies': [
      'vuetify'
    ],
    outputDir: './dist/',
    publicPath: 'https://d-mess.net/',
    assetsDir: 'static',
    pages: {
      'index': {
        entry: './src/UserUI/main.js',
        template: 'public/index.html',
        title: 'Home',
        chunks: [ 'chunk-vendors', 'chunk-common', 'index' ]
      },
      'admin': {
        entry: './src/AdminUI/main.js',
        template: 'public/admin.html',
        title: 'Admin',
        chunks: [ 'chunk-vendors', 'chunk-common', 'admin' ]
      },
      'auth': {
        entry: './src/Login/main.js',
        template: 'public/auth.html',
        title: 'Auth',
        chunks: [ 'chunk-vendors', 'chunk-common', 'auth' ]
      }
    }
  }
} else {
  module.exports = {
    'transpileDependencies': [
      'vuetify'
    ],
    outputDir: './dist/',
    publicPath: 'https://0.0.0.0:8080/',
    assetsDir: 'static',
    pages: {
      'index': {
        entry: './src/UserUI/main.js',
        template: 'public/index.html',
        title: 'Home',
        chunks: [ 'chunk-vendors', 'chunk-common', 'index' ]
      },
      'admin': {
        entry: './src/AdminUI/main.js',
        template: 'public/admin.html',
        title: 'Admin',
        chunks: [ 'chunk-vendors', 'chunk-common', 'admin' ]
      },
      'auth': {
        entry: './src/Login/main.js',
        template: 'public/auth.html',
        title: 'Auth',
        chunks: [ 'chunk-vendors', 'chunk-common', 'auth' ]
      }
    },
    chainWebpack: config => {
      config.optimization
        .splitChunks(false)

      config
        .plugin('BundleTracker')
        .use(BundleTracker, [{ filename: '../frontend/webpack-stats.json' }])

      config.resolve.alias
        .set('__STATIC__', 'static')

      config.devServer
        .public('0.0.0.0:8080/')
        .host('127.0.0.1')
        .port(8080)
        .hotOnly(true)
        .watchOptions({ poll: 1000 })
        .https(true)
        .headers({ 'Access-Control-Allow-Origin': ['\*'] })
    }
  }
}
