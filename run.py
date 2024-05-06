import os
import sys
from app.engine import MathEngine

INPUT_FILE = os.getenv("INPUT_FILE")
OUTPUT_FILE = os.getenv("OUTPUT_FILE")

if __name__ == "__main__":

    if len(sys.argv) < 3:
        if INPUT_FILE is None or OUTPUT_FILE is None:
            print("Usage: python run.py input_file output_file")
            sys.exit(1)

        input_file = INPUT_FILE
        output_file = OUTPUT_FILE
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    app = MathEngine(input_file=input_file, output_file=output_file)
    app.run(calculate_api_cost=True)
    app.evaluate()

    

