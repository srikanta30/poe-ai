BOTS_QUESTION_CLASSIFICATION_PROMPT = """
Below is the conversation between a user and an AI math bot, which helps them to improve their math skills.

Your task is to answer the bot's last question as briefly as possible.

Conversation History:
{conversation_history}

Bot's Last Question:
{bots_last_question}

"""


USERS_RESPONSE_CLASSIFICATION_PROMPT = """
Below is the conversation between a user and an AI math bot, which helps them to improve their math skills.

Your task is to classify whether user's answer is mathematically equivalent to the bot's last question:
EQUIVALENT or NOT_EQUIVALENT.

Respond with the only EQUIVALENT/NOT_EQUIVALENT.

Bot's Last Question:
{bots_last_question}

Expected Answer:
{expected_answer}

User's Answer:
{users_response}

"""