FROM ubuntu

RUN apt update
RUN apt install python3-pip -y
RUN pip install Flask
RUN pip install spotipy


WORKDIR /app/Spotify_project
RUN mkdir -p /app/Spotify_project/API_DATA

COPY Code .
EXPOSE 5000
ENV FLASK_APP=test.py

CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]

