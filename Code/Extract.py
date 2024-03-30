# import necessary modules
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import *
import json
import os

# initialize Flask app
app = Flask(__name__)

# set the name of the session cookie
app.config['SESSION_COOKIE_NAME'] = "Spotify Cookie"
app.secret_key = 'enter your secret key'
TOKEN_INFO = 'token info'


@app.route('/')
def login():
    auth_url = create_spotidy_oauth().get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotidy_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('get_user_data', _external=True))


@app.route('/getuserdata')
def get_user_data():
    try:
        token_info = get_token()
        print(token_info)
    except:
        print('not logged in')
        return redirect('/')
    sp = spotipy.Spotify(auth=token_info['access_token'])
    # data = sp.current_user_top_tracks()
    data2 = sp.featured_playlists()["playlists"]["items"]
    # [0]["id"]
    # data3=sp.playlist(playlist_id="37i9dQZF1DX0XUfTFmNBRM")
    playlist_list = []
    playlist_data = []
    for i in range(0, len(data2)):
        playlist_list.append(data2[i]["id"])

    for p_id in playlist_list:
        tmp_data = json.dumps(sp.playlist_tracks(p_id)["items"])
        path=r"C:\Users\tapis\PycharmProjects\Spotify_project\API_DATA"
        #path = r"/app/Spotify_project/API_DATA"
        with open(f'{path}/{p_id}.json', 'w') as file1:
            # Writing data to a file
            file1.write(tmp_data)

    # data3=sp.playlist_tracks("37i9dQZF1DX0XUfTFmNBRM")["items"][0]["track"]["popularity"]
    # ["artists"]["name"]

    data3 = sp.playlist_tracks("37i9dQZF1DX0XUfTFmNBRM")["items"][0]["track"]["artists"][0]["name"]

    # data3=sp.playlist_tracks("37i9dQZF1DX0XUfTFmNBRM")["items"][0]["track"]["name"]
    print(str(data3))
    return data3


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        redirect(url_for('login'), _external=False)

    now = int(time.time())
    is_expired = token_info['expires_at'] - now < 60
    if is_expired:
        spotify_oauth = create_spotidy_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])

    return token_info


def create_spotidy_oauth():
    return SpotifyOAuth(
        client_id='enter client id here',
        client_secret='enter client secret here',
        redirect_uri=url_for('redirect_page', _external=True),
        scope='user-library-read user-top-read')


if __name__ == "__main__":
    # Please do not set debug=True in production
    app.run(host="0.0.0.0", port=5000, debug=False)