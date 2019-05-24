const path = require("path");

module.exports = {
    mode: "development",
    entry: "./webapp/src/index.js",
    output: {
        filename: "bundle.js",
        path: path.resolve(__dirname, "webapp/dist"),
    },
    devServer: {
        contentBase: "./webapp/dist"
    },
    module: {
        rules: [
            {
                test: /.scss$/,
                use: [
                    {
                        loader: "style-loader",
                    },
                    {
                        loader: "css-loader",
                    },
                    {
                        loader: "postcss-loader",
                        options: {
                            plugins: function() {
                                return [
                                    require("autoprefixer")
                                ];
                            },
                        },
                    },
                    {
                        loader: "sass-loader",
                    },
                ],
            },
        ],
    },
};
