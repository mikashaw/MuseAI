from flask import render_template, Blueprint, url_for, request, flash, redirect, session, abort
from.models import User 
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token 
from pip._vendor import cachecontrol 
import google.auth.transport.requests
import requests
import os
import pathlib

auth = Blueprint('auth', __name__)

GOOGLE_CLIENT_ID = "51767622150-u9h07fhuj58eeloubdgd15ac9sf7rfrs.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secrets_file.json")
flow = Flow.from_client_secrets_file(client_secrets_file=client_secrets_file,
scopes = ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"],
redirect_uri= "http://127.0.0.1:5000/callback"
)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['google-button'] == 'Sign in with Google':
            authorization_url, state = flow.authorization_url()
            session["state"] = state 
            return redirect(authorization_url)

    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email = email).first()

    if user:
        if check_password_hash(user.password, password):
            flash('Logged in successfully!', category = 'success')
            login_user(user, remember = True)
            return redirect(url_for('views.home'))
        else:
            flash('You failed.', category = 'error')
    else:
        flash('Email does not exist.', category = 'error')

    #write some code that checks user login info
    return render_template("login.html", user=current_user)

@auth.route('/callback')
def callback():
    flow.fetch_token(authorization_response = request.url)

    if not session["state"] == request.args["state"]:
        abort(500)

    credentials = flow.credentials 
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request = token_request,
        audience= GOOGLE_CLIENT_ID
    )

    session['google_id'] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return render_template("homepage.html", name = session["name"], session = session)

@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@auth.route('/homebase', methods =['GET', 'POST'])
def homebase():
    return render_template('homebase.html', name = session["name"], session = session)

@auth.route('/generate_audio', methods = ['GET', 'POST'])
def generate_audio():
    return render_template('generate_audio.html', name = session["name"], session = session)
    




