# coat-bot

Telegram bot that tracks weather and
notifies you every day about appropriate
clothes for that given day.

## Installation

Assuming you have a Linux machine with
Python 3, pip and Git, the installation
process is as follows:

1. Clone this repository to your local machine:  
`$ git clone https://github.com/gnudeb/coat-bot.git`  
`$ cd coat-bot`
2. Create new virtual environment and enable it:  
`$ python3 -m venv coat-bot-venv`  
`$ source coat-bot-venv/bin/activate`  
Your command line should now have a prefix
indicating that you are in a virtual environment:
`(coat-bot-venv) $ _`
3. Install Python dependencies:  
`$ pip3 install -r requirements.txt`
4. Add a json file with your Telegram bot token
in the project root directory named `private.json`:  
```json
{
    "TELEGRAM_TOKEN": "<your token here>"
}
```
5. Run bot:  
`$ python3 manage.py runserver`
