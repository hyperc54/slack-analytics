from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from slackclient import SlackClient
from backend.slack.request_handler import GraphRequestHandler
import configparser

app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
CORS(app)

rh = GraphRequestHandler()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/load/<token_start>/<chan_name>/<int:nb_days>/<code>')
def get_graphs_data(token_start, chan_name, nb_days, code):
    response = rh.handle_request(code, token_start, chan_name, nb_days)
    return jsonify(response)

@app.route('/api/load/available_channels')
def get_available_channels():
    return None

@app.route('/api/auth/<code>')
def get_user_token(code):
    sc = SlackClient("")

    # Read config
    config = configparser.ConfigParser()
    config.read('config.ini')
    CLIENT_ID = config['SLACK_API']['CLIENT_ID']
    CLIENT_SECRET = config['SLACK_API']['CLIENT_SECRET']

    # Request the auth tokens from Slack
    auth_response = sc.api_call(
        "oauth.access",
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code
    )

    token = auth_response['access_token']

    rh.register_new_client(code, token)

    return jsonify(auth_response)