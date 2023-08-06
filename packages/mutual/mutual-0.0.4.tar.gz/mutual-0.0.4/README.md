# mutual

A python package to interact with the Mutuai API.

## Installation

Run `pip install mutual` in the project root directory.

## Usage

```python
import mutual

# SIGNUP
response = mutual.Auth.signup("username", "email")
print(response) # after signing up the key is automatically set

# to print the api_key from the response
api_key = response.get("api_key", None)
print(api_key)

# to get the api_key
print(mutual.api_key)
# to set the api_key
mutual.api_key = "your_api_key"

# CHAT
mutual.api_key = "your_api_key"
for message in mutual.Chat.create("Hello", "bot_id", "username"):
    print(message)

# CHAT DEMO
for message in mutual.Chat.create_demo("Hello"):
    print(message)

# BOT
print(mutual.Bot.getBots())
print(mutual.Bot.getBot("1"))
print(mutual.Bot.createBot("2", "alex", "mutual")) # bot_id, bot_name, bot_org
print(mutual.Bot.updateBot("2", bot_name="alex2"))
print(mutual.Bot.updateBot("2", bot_name="alex2", bot_org="mutual"))
print(mutual.Bot.updateBot("2", bot_org="mutual"))

# you can also set the bot_id like this so you dont need to pass it in chat
mutual.api_key = "your_api_key"
mutual.bot_id = "bot_id"

for message in mutual.Chat.create("Hello", username="username"):
    print(message)

# to print the bot_id
print(mutual.bot_id)

# you can import the functions directly like so
from mutual import Bot, Auth, Chat
```

python setup.py sdist

twine upload dist/* 