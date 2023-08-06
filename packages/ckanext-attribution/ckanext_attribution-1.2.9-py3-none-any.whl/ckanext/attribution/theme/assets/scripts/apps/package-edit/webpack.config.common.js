'use strict';

const { VueLoaderPlugin } = require('vue-loader');
const NodePolyfillPlugin = require('node-polyfill-webpack-plugin');

const webpackConfig = {
  entry: ['./src/app.js'],
  resolve: {
    alias: {
      vue: 'vue/dist/vue.js',
    },
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader',
      },
      {
        test: /\.js$/,
        use: 'babel-loader',
      },
      {
        test: /\.css$/,
        use: ['vue-style-loader', 'style-loader', 'css-loader'],
      },
      {
        test: /\.csl$/,
        type: 'asset/source',
      },
    ],
  },
  plugins: [
    new VueLoaderPlugin(),
    // this fixes a bug with citation-js where 'process' is not defined
    // (https://github.com/citation-js/citation-js/issues/150)
    new NodePolyfillPlugin(),
  ],
  output: {
    library: 'package-edit',
    libraryTarget: 'umd',
    filename: '[name].package-edit.js',
    publicPath: '/assets/scripts/apps/package-edit/',
  },
};

module.exports = webpackConfig;
