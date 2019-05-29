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
        var geolocationButton = document.getElementById("geolocation-button");
        geolocationButton.setAttribute("disabled", "");
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
    var container = document.getElementById("results-container");
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    var spinner = document.getElementById("spinner");
    spinner.classList.remove("d-none");

    var requestBody = JSON.stringify(requestObject);
    var xhr = new XMLHttpRequest();
    xhr.addEventListener("load", requestListener);
    xhr.open("POST", API_URL);
    xhr.send(requestBody);
}

function requestListener() {
    var container = document.getElementById("results-container");
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }

    var response = JSON.parse(this.responseText);
    if (response.length > 0) {
        var h2 = document.createElement("h2");
        h2.classList.add("h4");
        h2.classList.add("font-weight-normal");
        h2.appendChild(document.createTextNode("Results"));
        container.appendChild(h2);
        var ul = document.createElement("ul");
        for (var i = 0; i < response.length; i++) {
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.setAttribute("href", response[i].url);
            a.appendChild(document.createTextNode(response[i].osm_name));
            li.appendChild(a);
            ul.appendChild(li);
        }
        container.appendChild(ul);
    } else {
        var div = document.createElement("div");
        div.classList.add("alert");
        div.classList.add("alert-primary");
        div.setAttribute("role", "alert");
        div.appendChild(document.createTextNode("No results were found for this location."));
        container.appendChild(div);
    }

    var spinner = document.getElementById("spinner");
    spinner.classList.add("d-none");
}

document.addEventListener("DOMContentLoaded", function(event) {
    setup();
});
