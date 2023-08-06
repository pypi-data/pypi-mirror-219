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

# LOGIN
response = mutual.Auth.login("username", "email")
print(response)

# CHAT
mutual.api_key = "your_api_key"
for message in mutual.Chat.create("Hello", "seansbot", "Sean"):
    print(message['content'], end='', flush=True)

# CHAT DEMO
for message in mutual.Chat.create_demo("Hello"):
    print(message['content'], end='', flush=True)

# BOT Instance

# uses bot name
alexbot = mutual.create_bot("alexbot") # THIS WILL CREATE A NEW BOT EACH TIME AND RETURN A BOT INSTANCE
for message in alexbot.chat("Hey there", "Sean"):
    print(message['content'], end='', flush=True)

# can create bot instance passing in these values
alexbot = mutual.create_bot("alexbot", bot_org="Mutual", prompt_id="default") 

# uses bot id
alexbot = mutual.generate_bot("alexbot-id") # THIS WILL LOOK UP FOR A EXISTING BOT AND GENERATE AN INSTANCE OF THAT BOT 
for message in alexbot.chat("Hey there", "Sean"):
    print(message['content'], end='', flush=True)

# update using bot instance
alexbot.update_bot(bot_org='mutual', bot_name='new_bot_name', prompt_id='new_prompt')

# view bot instance data
print(alexbot.api_key) # prints the api_key
print(alexbot.bot_id) # prints the bot id
print(alexbot.bot_name) # prints the bot name
print(alexbot.prompt_id) # prints the prompt id

# BOT
# using functions
print(mutual.Bot.get_bots())
print(mutual.Bot.get_bot("1"))
print(mutual.Bot.create_bot("alex", "mutual")) #bot_name, bot_org.
print(mutual.Bot.create_bot("alex2", "mutual", prompt_id='default')) #bot_name, bot_org, prompt_id -> optional
print(mutual.Bot.update_bot("2", bot_name="alex2"))
print(mutual.Bot.update_bot("2", bot_name="alex2", bot_org="mutual"))
print(mutual.Bot.update_bot("2", bot_org="mutual"))

# you can also set the bot_id like this so you dont need to pass it in chat
mutual.bot_id = "bot_id"

# to print the bot_id
print(mutual.bot_id)


# PROMPT

print(mutual.Prompt.get_prompts())
print(mutual.Prompt.get_prompt("1"))
print(mutual.Prompt.create_prompt("new_prompt", identity_prompt="",
                                    backstory_prompt="", world_prompt="",
                                    action_prompt="", internal_thought="",
                                    external_thought="", internal_thought_memory="",
                                    external_thought_memory="", summarization_prompt="")) # cannot be blank

# optionals for updating
# identity_prompt,
# backstory_prompt,
# world_prompt,
# action_prompt,
# internal_thought,
# external_thought,
# internal_thought_memory,
# external_thought_memory,
# summarization_prompt
print(mutual.Prompt.update_prompt("alex_prompts", identity_prompt="alex2")) #prompt_id is first

# DEV
response = mutual.Dev.clear("bot_id") # clears memories

# you can import the functions directly like so
from mutual import Bot, Auth, Chat, Dev, Prompt
```

python setup.py sdist

twine upload dist/* 