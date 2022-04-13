// webpack.mix.js

let mix = require('laravel-mix');

mix
  .setPublicPath('static')
  .js('assets/app.js', 'static')
  .vue();
