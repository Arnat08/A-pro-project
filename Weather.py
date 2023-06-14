import requests
from flask import Flask, request, render_template, session, redirect, url_for, jsonify
from pprint import pprint
from config import open_weather_token

def weather():
    api_url = 'https://weatherapi-com.p.rapidapi.com/current.json'
    headers = {'X-RapidAPI-Key': 'e6219e657cmsh92edde1afaa90f1p18a47ejsn1d3554ded7f9'}
    params = {'q': 'Almaty'}
    responce = requests.get(api_url, headers=headers, params=params)
    if responce.ok:
        weather_data = responce.json()
        return jsonify(weather_data)
    else:
        return jsonify({'massage': 'Sorry, could not retrieve weather_data.'}), 404
