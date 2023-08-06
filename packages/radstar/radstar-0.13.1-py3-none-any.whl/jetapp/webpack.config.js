// ------------------------------------------------------------------------------------------------------------------ //

// Copyright © 2021-2023 Peter Mathiasson
// SPDX-License-Identifier: ISC

// ------------------------------------------------------------------------------------------------------------------ //

const fs = require('fs')
const path = require('path');
const webpack = require('webpack');

const execSync = require('child_process').execSync;

// ------------------------------------------------------------------------------------------------------------------ //

module.exports = function(env) {

    const appSettings = JSON.parse(execSync('rs jetapp settings'));

    // TODO: check that settings that are required are present in appSettings.

    const MiniCssExtractPlugin = require('mini-css-extract-plugin');
    const production = !!(env && env.production === 'true');

    const babelSettings = {
        extends: path.join(__dirname, '/.babelrc')
    };

    const config = {
        mode: production ? 'production' : 'development',
        entry: {
            jetapp: path.join(__dirname, 'sources/jetapp.js'),
        },
        output: {
            filename: '[name].js',
            path: '/tmp/jetapp_output/',
            publicPath: '/app/'
        },
        module: {
            rules: [
                {
                    test: /\.js$/,
                    use: 'babel-loader?' + JSON.stringify(babelSettings)
                },
                {
                    test: /\.(svg|png|jpg|gif)$/,
                    type: 'asset'
                },
                {
                    test: /\.(less|css)$/,
                    use: [ MiniCssExtractPlugin.loader, 'css-loader' ]
                }
            ]
        },
        stats: 'minimal',
        resolve: {
            extensions: ['.js'],
            modules: [
                './sources',
                '/node_modules'
            ],
            alias: {
                'app': '/rs/project/main/jetapp',
                'jet-locales': path.join(__dirname, 'sources/locales'),
                'jet-views': path.join(__dirname, 'sources/views'),
                'radstar': path.join(__dirname, 'sources/radstar'),
            }
        },
        plugins: [
            new MiniCssExtractPlugin({
                filename: '[name].css'
            }),
            new webpack.DefinePlugin({
                APPNAME: `'${appSettings.name}'`,
                SETTINGS: JSON.stringify(appSettings.settings),
                PRODUCTION: production
            })
        ],
        devServer: {
            contentBase: appSettings.webroots,
            proxy: {
                context: function(reqPath) {
                    for (const root of appSettings.webroots) {
                        if (fs.existsSync(path.join(root, reqPath)))
                            return false;
                    }
                    return true;
                },
                target: 'http://localhost:5001',
            },
            stats: 'errors-only'
        }
    };

    if (!production) {
        config.devtool = 'inline-source-map';
    }

    return config;

}

// ------------------------------------------------------------------------------------------------------------------ //
