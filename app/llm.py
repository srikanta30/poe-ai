import os
from dotenv import load_dotenv

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from langchain_community.callbacks import get_openai_callback

from app.prompts import (
    BOTS_QUESTION_CLASSIFICATION_PROMPT,
    USERS_RESPONSE_CLASSIFICATION_PROMPT
)
from app.utils import format_dialog, get_last_bot_question

load_dotenv()

LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

class LLM:

    def __init__(self) -> None:
        self.llm = ChatOpenAI(api_key=LLM_API_KEY,model=LLM_MODEL_NAME)

    def call(self, conversation_history: str, users_response: str, calculate_api_cost: bool = False):
        bots_last_question = get_last_bot_question(conversation_history)
        conversation_history = format_dialog(conversation_history)

        bots_question_clasification_prompt_template = BOTS_QUESTION_CLASSIFICATION_PROMPT
        users_response_clasification_prompt_template = USERS_RESPONSE_CLASSIFICATION_PROMPT

        bots_question_clasification_prompt = PromptTemplate(
            template=bots_question_clasification_prompt_template,
            input_variables=[
                "bots_last_question"
                "conversation_history",
            ],
        )

        users_response_clasification_prompt = PromptTemplate(
            template=users_response_clasification_prompt_template,
            input_variables=[
                "expected_answer"
                "users_response",
            ],
        )

        bots_question_clasification_chain = LLMChain(llm=self.llm, prompt=bots_question_clasification_prompt, output_key="expected_answer")
        users_response_clasification_chain = LLMChain(llm=self.llm, prompt=users_response_clasification_prompt, output_key="content")

        input = {"bots_last_question": bots_last_question, "conversation_history": conversation_history, "users_response": users_response}

        llm_chain = SequentialChain(
            chains = [bots_question_clasification_chain, users_response_clasification_chain],
            input_variables = ["bots_last_question","conversation_history","users_response"],
            output_variables = ["content", "expected_answer"]
            )

        if calculate_api_cost:
            with get_openai_callback() as cb:
                reponse = llm_chain.invoke(input=input)
                print("Bot's Last Question: ", bots_last_question)
                print("Expected Answer: ", reponse["expected_answer"])
                print("Users Response: ", users_response)
            return [reponse["content"], cb.total_cost]
        else:
            reponse = llm_chain.invoke(input=input)
            return reponse["content"]