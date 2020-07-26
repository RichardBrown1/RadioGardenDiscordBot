# Mr World Wide the Radio Garden Bot

## Info

[The list of radio stations was obtained via easingtheme's script](https://github.com/easingthemes/radio-garden-m3u/tree/feature/1-nodejs-script-to-fetch-all-channels)

### Bot.py

- Queries an SQLite3 database for internet radio URLs
- Plays internet radio URLs

#### Installation

1. Follow this [guide](https://realpython.com/how-to-make-a-discord-bot-python/) on realPython.com by Alex Ronquillo to set up the bot.

2. Put the token at the end of bot.py

3. Import the [ffmpeg builds](https://ffmpeg.zeranoe.com/builds/) into the same folder as bot.py

4. Run bot.py

### Import.py

- Made an SQLite3 database using the results from easingtheme's script. (The radioStation list is a few months old at time of writing this in July 2020)
- I have a copy of the database here for use.

## TODO

- add commands:
  - help
  - info
  - random radio station
  - stations near by
  - volume control
- improve search
- improve messages sent
- have a radio tuning sound effect when transitioning in between stations?
- error messages when it doesn't connect
- favourites / votes

## Issues  

- Missing entries of Mauritiana in the database (Country code issues, might be fixed if I update the list of radio stations)
