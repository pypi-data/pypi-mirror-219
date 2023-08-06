'use strict';

const { merge } = require('webpack-merge');
const commonConfig = require('./webpack.config.common');
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

const webpackConfig = {
  mode: 'production',
  resolve: {
    alias: {
      vue: 'vue/dist/vue.esm.js',
    },
  },
  optimization: {
    minimize: true,
    minimizer: [
      new CssMinimizerPlugin({
        minimizerOptions: {
          preset: ['default', { discardComments: { removeAll: true } }],
        },
      }),
      new TerserPlugin({
        extractComments: false,
      }),
    ],
  },
};

module.exports = merge(commonConfig, webpackConfig);
