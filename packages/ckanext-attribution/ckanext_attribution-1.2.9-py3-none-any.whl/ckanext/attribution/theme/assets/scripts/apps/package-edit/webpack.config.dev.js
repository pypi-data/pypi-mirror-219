'use strict';

const { merge } = require('webpack-merge');
const commonConfig = require('./webpack.config.common');

const webpackConfig = {
  mode: 'development',
};

module.exports = merge(commonConfig, webpackConfig);
