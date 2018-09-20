# slack_analytics

A Flask server serving a Vue JS single page app and an API that provides slack analytics

## How to dev
It is advised to run both frontend and backend separately

Frontend: `npm install; npm run start`

Backend: `FLASK_APP=run.py FLASK_DEBUG=1 flask run`

## Build & deploy
`npm run build` -> the frontend web app
Then the flask server can serve the files

You'll also need to feed SLACK_CLIENT and SLACK_SECRET in a config.ini file
(see run.py)
