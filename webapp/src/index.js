import "./main.scss";

function setup() {
    var geolocationButton = document.getElementById("geolocation-button");
    geolocationButton.addEventListener("click", geolocate);
    var searchButton = document.getElementById("search-button");
    searchButton.addEventListener("click", search);
}

function geolocate() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(geolocationCallback);
    } else {
        console.log("unsupported");
    }
}

function geolocationCallback(position) {
    queryServer({
        "longitude": position.coords.longitude,
        "latitude": position.coords.latitude,
    });
}

function search() {
    var query = document.getElementById("geocode-input").value;
    queryServer({
        "query": query,
    });
}

function queryServer(requestObject) {
    var requestBody = JSON.stringify(requestObject);
    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", requestListener);
    xhr.open("POST", API_URL);
    xhr.send(requestBody);
}

function requestListener() {
    var response = JSON.parse(this.responseText);
    console.log(response);
}

document.addEventListener("DOMContentLoaded", function(event) {
    setup();
});
