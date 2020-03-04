"use strict";


// PART 1: SHOW A FORTUNE

function replaceFortune(results) {
    $("#fortune-text").html(results);
}

function showFortune(evt) {
    $.get('/fortune', replaceFortune);
}

$('#get-fortune-button').on('click', showFortune);



// PART 2: SHOW WEATHER

function replaceForecast(results) {
    $("#weather-info").html(results.forecast);
}

function showWeather(evt) {
    evt.preventDefault();

    let url = "/weather.json";
    let formData = {"zipcode": $("#zipcode-field").val()};

    $.get(url, formData, replaceForecast);
}

$("#weather-form").on('submit', showWeather);



// PART 3: ORDER MELONS

function updateMelons(results) {
    if (results.code === "OK") {
        $('#order-status').html("<p>" + results.msg + "</p>");
    }
    else {
        $('#order-status').addClass("order-error");
        $('#order-status').html("<p><b>" + results.msg + "</b></p>");
    }
}

function orderMelons(evt) {
    evt.preventDefault();

    let formInputs = {
        "melon_type": $("#melon-type-field").val(),
        "qty": $("#qty-field").val()
    };

    $.post("/order-melons.json", formInputs, updateMelons);
}

$("#order-form").on('submit', orderMelons);
