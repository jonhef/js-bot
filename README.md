# jonhef's secretary bot

## How to run

1. Put your google credentials in `config/credentials.json`
2. Put your data in `config/.env.example` and rename it to `config/.env`
3. Make virtual environment and activate it
```
# MacOS / Linux
python3 -m venv .venv
source .venv/bin/activate
# Windows
python -m venv .venv
.venv\Scripts\activate
```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Run the bot
```
python -m internal.main
```

## How to use

1. Write a message to your bot(it must be your second account)
2. Use!