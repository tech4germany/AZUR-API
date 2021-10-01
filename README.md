Code Repository for the API used in the AZUR project from the 2021 [Tech4Germany](tech.4germany.org) fellowship. The functionalities of this API are also being made accessible through a UI, available [here](https://github.com/daudprobst/AZUR-Frontend).

# AZUR

In the German Bundestag, various resources are allocated to parties according to their strengths in the plenum using one of three [proportionality calculation](https://en.wikipedia.org/wiki/Party-list_proportional_representation) methods - the Saint-Lague/Schepers, d'Hondt, and Hare-Niemeyer methods. This includes, for example, the number of seats on committees, speaking time on the floor, and even things like floor space on open-door days. AZUR is an internally used calculator that applies these methods - this project is its third iteration, after one created in the 1970s and one created in 2000.

# AZUR-API

This repository contains the backend API, which is to be hosted separately from the frontend so it can be accessed from other sources. Detailed API docs are to follow - in short, it requires a JSON POST with a vote distribution, the number of seats (or minutes, or square meters, or...) to distribute, and the method to use, and returns the result of that calculation as a JSON with up to three keys: the seat distribution, the assignment sequence (if the method returns one), and a table of distributions from 1 to the requested amount of seats.

# Getting Started

To run the API locally, clone this project, install requirements.txt in a new python environment, set the flask app with `export FLASK_APP app` (or your OS equivalent of setting an environment variable) and run it with `flask run`.
