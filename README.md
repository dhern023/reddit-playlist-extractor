# reddit-playlist-extractor
Bot for extracting playlists from reddit 

# Setup
```
pip3 install -r requirements.txt
```

# Running
```
python playlist_extractor/app_cli.py
>>> Prompts for reddit URL (old.reddit is best)
```
Out pops the extracted bodies and extracted songs.

# Testing

We use pytest for Testing
```
cd playlist_extractor
python -m pytest ../tests
```

# TODO
Register as a reddit bot and spotify app to use their APIs
Add fail-fast for bad connections