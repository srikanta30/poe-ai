import os
import json
import ast
from dotenv import load_dotenv
import pandas as pd
from app.llm import LLM
from app.utils import calculate_time

load_dotenv()

CONFIG_JSON = os.getenv("CONFIG_JSON")

class MathEngine:
    def __init__(self, input_file: str, output_file: str) -> None:
        self.config = json.loads(CONFIG_JSON)
        self.input_file = input_file
        self.output_file = output_file
        self.llm = LLM()
    
    @calculate_time
    def classify_users_response(self, conversation_history: str, users_response: str = "", calculate_api_cost: bool = False):

        if calculate_api_cost:
            response, cost = self.llm.call(conversation_history=conversation_history, users_response=users_response, calculate_api_cost=calculate_api_cost)    
            return [response, cost]
        else:
            response = self.llm.call(conversation_history=conversation_history, users_response=users_response)
            return [response, None]

    def call(self, row, calculate_api_cost: bool = False):

        try:
            conversation_history = ast.literal_eval(row[self.config['conversation_history_key']])
        except (ValueError, SyntaxError) as e:
            print(f"Skipping row due to error in conversation history.")
            return "NOT_APPLICABLE", 0, 0
        
        users_response = row[self.config['users_response_key']]
        human_evaluation = row[self.config['human_evaluation_key']]

        result, time_taken_seconds = self.classify_users_response(conversation_history=conversation_history, users_response=users_response, calculate_api_cost=calculate_api_cost)
     
        llm_equivalence, api_cost = result

        print(f"OUTPUT => Correct: {'Yes' if llm_equivalence == human_evaluation else 'No'}, Time Taken: {time_taken_seconds}, Cost: ${api_cost}")
        return llm_equivalence, time_taken_seconds, api_cost

    def run(self, calculate_api_cost: bool = False):
        df = pd.read_csv(self.input_file)

        df = df[~df[self.config['users_response_key']].str.contains('https://zoe-images.s3.amazonaws.com/')]
        
        results = df.apply(lambda row: self.call(row=row, calculate_api_cost=calculate_api_cost), axis=1)
        
        results_df = pd.DataFrame(results.tolist(), columns=['llm_equivalent_key', 'time_taken_key', 'api_cost_key'])
        
        for key in ['llm_equivalent_key', 'time_taken_key', 'api_cost_key']:
            if key in self.config:
                if key == 'api_cost_key' and calculate_api_cost:
                    df[self.config[key]] = results_df[key]
                else:
                    df[self.config[key]] = results_df[key]
        
        df.to_csv(self.output_file, index=False) 

    def evaluate(self):

        total_df = pd.read_csv(self.output_file)

        df = total_df[total_df[self.config['llm_equivalent_key']] != 'NOT_APPLICABLE']
        df = total_df[~total_df[self.config['users_response_key']].str.contains('https://zoe-images.s3.amazonaws.com/')]

        total_rows = len(df)

        llm_responses = df[self.config['llm_equivalent_key']].str.strip()
        human_evaluations = df[self.config['human_evaluation_key']].str.strip()

        matches = df[llm_responses == human_evaluations]
        num_matches = len(matches)

        total_time_taken_sum = df[self.config['time_taken_key']].sum()
        total_api_cost_sum = df[self.config['api_cost_key']].sum()

        print(f"Total Rows: {total_rows}")
        print(f"Accuracy: {num_matches/total_rows*100}%")
        print(f"Speed: {total_time_taken_sum} secs")
        print(f"Cost: ${total_api_cost_sum}")
