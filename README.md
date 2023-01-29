# Distributed Computer Systems - Crypto Broker

Project created for a class in the Faculty of Technical Sciences. 

## Table of Contents
* [General](#general)
* [Technologies](#technologies)
* [How to Run](#how-to-run?)
* [Team Members](#team-members)

## General

The goal of the project was to make two dockerised flask applications that will communicate with each other and in the end deploy it. Frontend is simple html, css and javascript. The frontend communicates with the UI service that takes the request and propagates the data to Engine service from which it gets the response and sends it to frontend. Unfortunately the only crypto thing here is the external API from which we get the currency values and conversion rates since this app is essentially a little banking sistem. 

## Technologies
* Python
* Flask (Waitress WSGI)
* Docker
* HTML, CSS, JS

## How to run?
1. Use git to pull the whole repository `git clone https://github.com/AleksaBajat/DRS-Team-Project.git`
2. Open terminal inside the root folder and run `docker compose up --build`

## Team members
    Dragan Stančević
    Jovan Peškanov
    Djordje Jelicki
    Aleksa Bajat
