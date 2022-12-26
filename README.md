# julia-robotczyk
A Facebook Messenger chatbot based on my classmate's messages.
Uses [markovify](https://github.com/jsvine/markovify) for handling Markov chains and also uses [spaCy](https://github.com/explosion/spaCy) for NLP.

## Running
Make sure you're running Python 3.7+ before doing any steps.

If you are planning to run this bot on a Raspberry Pi, the host OS **must** be 64-bit for spaCy support. 
Check [this](https://www.raspberrypi.com/news/raspberry-pi-os-64-bit/) link for more details.

1. Clone the repository into a directory of your choice.
2. Move to the directory with the files in a terminal.
3. Make a new file called `credentials.json`, and use the template below to fill it up:
```json
{
    "email": "<FACEBOOK_ACCOUNT_EMAIL_HERE>",
    "password": "<FACEBOOK_ACCOUNT_PASSWORD_HERE>"
}
```
4. Gather a dataset of some kind, then make a `dataset.json` file, containing an array of strings with messages used for the chain.
5. Run `python3 -m pip install -r requirements.txt` to install required requirements.
6. Done! To run the bot, do `python3 bot.py`.

## Contributing
As with all my projects, contributions are highly appreciated!
