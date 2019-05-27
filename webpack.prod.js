const child_process = require("child_process");
const webpack = require("webpack");
const merge = require("webpack-merge");
const common = require("./webpack.common.js");
const TerserJSPlugin = require("terser-webpack-plugin");
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

module.exports = function() {
    return new Promise(function(resolve, reject) {
        var process = child_process.spawn(
            "aws",
            [
                "cloudformation",
                "describe-stacks",
                "--stack-name",
                "registrars",
                "--query",
                "Stacks[].Outputs[?OutputKey==`RegistrarsApi`]",
                "--output",
                "json"
            ],
            {
                stdio: ["pipe", "pipe", "inherit"],
            }
        );
        var output = "";
        process.stdout.on("data", function(data) {
            output += data.toString();
        });
        process.on("close", function(code) {
            if (code === 0) {
                const API_URL = JSON.parse(output)[0][0].OutputValue;
                if (API_URL) {
                    resolve(merge(common, {
                        mode: "production",
                        devtool: "source-map",
                        plugins: [
                            new webpack.DefinePlugin({
                                API_URL: JSON.stringify(API_URL),
                            }),
                        ],
                        optimization: {
                            minimizer: [
                                new TerserJSPlugin({}),
                                new OptimizeCSSAssetsPlugin({}),
                            ],
                        },
                    }));
                } else {
                    reject("Couldn't parse output of " +
                           "`aws cloudformation describe`: " +
                           output);
                }
            } else {
                reject("Failed to read API Gateway URL from CloudFormation");
            }
        });
        process.on("error", function(err) {
            reject("Failed to run AWS CLI: " + err);
        });
    });
};
