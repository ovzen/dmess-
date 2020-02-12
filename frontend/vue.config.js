
const BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  'transpileDependencies': [
    'vuetify'
  ],
  outputDir: './dist/',
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
      template: 'public/index.html',
      title: 'Admin',
      chunks: [ 'chunk-vendors', 'chunk-common', 'admin' ]
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
      .public('http://127.0.0.1:8080/')
      .host('127.0.0.1')
      .port(8080)
      .hotOnly(true)
      .watchOptions({ poll: 1000 })
      .https(false)
      .headers({ 'Access-Control-Allow-Origin': ['\*'] })
  }
}
