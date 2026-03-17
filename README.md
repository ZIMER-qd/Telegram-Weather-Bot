# Telegram-Weather-Bot
### Description:
A Telegram bot that displays the weather for any location.
### Supports:
- Current weather;
- Detailed and short forecast;
- Multi-day forecast;
- Daily weather notification at a user-specified time;
- Saving your specified location.
### Functions:
- /start - Welcome and brief information;
- /help - Command help;
- /weather - Check the weather at a specified location;
- /myloc - Show weather at a saved location;
- /setloc - Set or change a location;
- setime - Set a daily weather notification.
### Requirements:
- Python 3.11+
- aiogram
- SQLAlchemy
- APScheduler
- pydantic-settings
### Installation:
#### 1. Clone the repository:  
git clone https://github.com/ZIMER-qd/Telegram-Weather-Bot.git
cd Telegram-Weather-Bot  
#### 2. Create a virtual environment and activate it:  
python -m venv .venv  
source .venv/bin/activate - Linux / Mac  
.venv\Scripts\activate - Windows  
#### 3. Install dependencies:  
pip install -r requirements.txt  
#### 4. Configure the .env file with the bot token:  
BOT_TOKEN=token  
#### 5. Run the bot:  
python run.py
