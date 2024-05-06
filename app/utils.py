import time
from functools import wraps

def calculate_time(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  
        result = func(*args, **kwargs)  
        end_time = time.time() 
        execution_time = end_time - start_time  
        return result, execution_time

    return wrapper

def format_dialog(dialog):
    formatted_string = ""
    for entry in dialog:
        if isinstance(entry['user'], list):
            image_url = entry['user'][1]['image_url']['url']
            formatted_string += f"User: [Image] {image_url}\n"
        else:
            formatted_string += f"User: {entry['user']}\n"
        formatted_string += f"Bot: {entry['bot']}\n\n"
    return formatted_string

def get_last_bot_question(dialog):
    last_bot_question = None
    for entry in reversed(dialog):
        last_bot_question = entry['bot']
        break
    return last_bot_question