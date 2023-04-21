from flask import render_template, redirect, url_for, session, flash, request, jsonify, send_from_directory, Blueprint
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests
from config import client_id, client_secret, organization_domain

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    flow = Flow.from_client_config({
        'web': {
            'client_id': client_id,
            'client_secret': client_secret,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [url_for('auth.oauth2callback', _external=True)]
        }},
        ['email', 'openid']
    )

    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
    print(f'Redirect URI: {flow.redirect_uri}')
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state

    return redirect(authorization_url)

@auth.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_config({
        'web': {
            'client_id': client_id,
            'client_secret': client_secret,
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'redirect_uris': [url_for('auth.oauth2callback', _external=True)]
        }},
        scopes=['openid', 'email'],
        state=state
    )

    flow.redirect_uri = url_for('auth.oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    id_info = id_token.verify_oauth2_token(credentials.id_token, google_requests.Request(), client_id)

    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    if id_info['hd'] != organization_domain:
        flash("Unauthorized email domain", "error")
        return redirect(url_for('routes.index'))

        session['email'] = id_info['email']
    flash('Login successful.', 'success')
    session['email'] = id_info['email']
    return redirect(url_for('routes.index'))


@auth.route('/logout')
def logout():
    session.pop('email', None)
    flash('Logout successful.', 'success')
    return redirect(url_for('routes.index'))
