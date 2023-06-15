import requests
from flask import Flask, request, render_template, session, redirect, url_for, jsonify



def show_weather():
    location = 'https://weatherapi-com.p.rapidapi.com/current.json'
    headers = {'X-RapidAPI-Key': 'e6219e657cmsh92edde1afaa90f1p18a47ejsn1d3554ded7f9'}
    params = {'q': 'Astana'}
    responce = requests.get(location, headers=headers, params=params)
    if responce.ok:
        weather = responce.json()
        return jsonify(weather)
    else:
        return f"Error"
