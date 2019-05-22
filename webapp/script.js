function setup() {
    var geolocationButton = document.getElementById("geolocation-button");
    geolocationButton.addEventListener("click", function(event) {
        geolocate();
    });
}

function geolocate() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(geolocationCallback);
    } else {
        console.log("unsupported");
    }
}

function geolocationCallback(position) {
    console.log(position.coords);
    queryServer({
        "longitude": position.coords.longitude,
        "latitude": position.coords.latitude,
    });
}

function queryServer(position) {
    request_body = JSON.stringify(position);
    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", requestListener);
    xhr.open("POST", "http://127.0.0.1:3000/");
    xhr.send(request_body);
}

function requestListener() {
    var response = JSON.parse(this.responseText);
    console.log(response);
}

document.addEventListener("DOMContentLoaded", function(event) {
    setup();
});
