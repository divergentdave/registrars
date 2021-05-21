const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: "./webapp/src/index.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "webapp/dist"),
    },
    plugins: [
        new MiniCssExtractPlugin({}),
        new HtmlWebpackPlugin({
            title: "Registrar of Titles Property Map Lookup",
            template: "./webapp/src/index.ejs",
        }),
    ],
    module: {
        rules: [
            {
                test: /.scss$/,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                    },
                    {
                        loader: "css-loader",
                    },
                    {
                        loader: "postcss-loader",
                        options: {
                            postcssOptions: {
                                plugins: [
                                    "autoprefixer",
                                ],
                            },
                        },
                    },
                    {
                        loader: "sass-loader",
                    },
                ],
                sideEffects: true
            },
            {
                test: /webapp\/src\/index.js$/,
                sideEffects: true
            }
        ],
    },
};
