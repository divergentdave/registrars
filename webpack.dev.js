const webpack = require("webpack");
const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");

module.exports = merge(common, {
    mode: "development",
    devtool: "inline-source-map",
    plugins: [
        new webpack.DefinePlugin({
            API_URL: JSON.stringify("http://localhost:3000/"),
        }),
    ],
    devServer: {
        static: "./webapp/dist"
    },
});
