# __init__.py
from . import Auth, Bot, Chat, Prompt, Dev

api_key = None
bot_id = None


def create_bot(bot_name, bot_org="Mutual", prompt_id="default"):
    # create new bot instance
    global api_key
    global bot_id

    response = Bot.create_bot(bot_name, bot_org, prompt_id)
    if not response['bot_id']:
        print('Failed in creating a bot.')
        raise Exception(f"Something went wrong. Error Message: {response['details']}")
    
    new_bot_instance = Bot.Bot(api_key, response['bot_id'], response['bot_name'], 
                               response['prompt_id'] or "default")
    
    print(f"Successfully Created a new Bot named {bot_name} with an id: {response['bot_id']}")

    bot_id = response['bot_id']
    return new_bot_instance


def generate_bot(bot_id_arg):
    # generate new bot instance
    global api_key
    global bot_id

    response = Bot.get_bot(bot_id_arg)
    if not response['bot_id']:
        print(f'Bot with id: {bot_id_arg} does not exist please create one.')
        raise Exception(f"Something went wrong. Error Message: {response['details']}")
    
    new_bot_instance = Bot.Bot(api_key, response['bot_id'], response['bot_name'], 
                               response['prompt_id'] or "default")
    
    print(f"Successfully Generated Bot named {response['bot_name']} with an id: {bot_id_arg}")

    bot_id = bot_id_arg
    return new_bot_instance