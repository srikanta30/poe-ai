# CoTeach: LLM Based Math Accuracy Project

## Objective 🎯:

Create an AI algorithm that can determine whether the response to a question is mathematically equivalent to the question itself.

## Deliverables 🚚:

1. Deliver the “Accuracy Calculation Dataset.csv” with the “*LLM Equivalence Evaluation (Response)*” column and the “*Time taken to complete the request*” column completely filled with the respective values.
    1. **LLM Equivalence Evaluation (Response)**: The result from the AI (EQUIVALENT/NOT_EQUIVALENT), of whether the final question from the bot is equivalent to the user’s response, as determined by the AI.
    2. **Time taken to complete the request**: How long did it take the AI to complete the request (in seconds).
    3. [Optional] API Cost: If a commercial API is used, please add the cost of individual requests.
2. The AI algorithm that was used to generate the values.
    1. Quick note explaining/documenting, what the AI was intended to do and what was the thought process behind it.

## Requirements ✅:

- Code should be written in Python unless the concepts/libraries can be easily adapted for Python-based code.
- The entire dataset should be treated as a “*test set*” and should not be needed to train a model unless it’s absolutely critical to the proposed solution.
    - Note: The idea is to create a generic AI that’s able to work with logic and not necessarily depend only on LLMs to solve computational questions.
- The accuracy of the model should be around 95% - and as close to 100% as possible.

## Criteria 📓:

[In the order of priority]

1. Accuracy: (True Positives + True Negatives)/(All data points)
2. Commercial feasibility:
    - Fast -  the response should not take more than an average of 5s
    - Cost effective
3. The code written should be clean, modular and scalable. If an LLM is used, it should be wrapped in a way such that it’s easy to switch out that LLM for another.
4. Bonus points if the AI algorithm also handles the image links.

## How to understand the dataset 📊:

<aside>
💡 The dataset is CoTeach’s repository of dialogs that multiple students have had with its AI Math Tutor, Zoe.

</aside>

Columns that matter the most:

1. **Conversation History:**
    1. *Information Contained:* Contains the entire dialog up to the point of the last question that Zoe asked the student. This holds the context of the conversation.
    2. *Structure:* Data is stored in the form of an array individual elements of the array representing a single back and forth between the bot and the student. The last element of the array contains the message that the student sent and the bot’s last response to that message.
    3. Note: The elements of the array resemble the format of how the message would be sent to an LLM. Some user messages may even contain images → where OpenAI’s GPT-4 vision’s syntax has been followed.
2. **Student Response:**
    1. *Information Contained:* This is the final response that the student has given to the given set of Conversation History. This can be in the form of an image for some rows. **This is what needs to be evaluated for equivalence** against the last question that the Bot has asked the student.
    2. *Structure:* The data is generally, plain text except for instances when the student shared an image. In those cases, it follows GPT-4 Vision’s syntax.

The two items in red above are to be compared for equivalence. Whether **Bot’s last question == Student’s answer**

Columns that may be relevant:

1. **DialogID Hash:** This just tracks one set of dialog across multiple rows. Since every row is a response from the student, there are rows which could be the continuation of a given conversation - belonging to the same DialogID Hash.

## Important Notes 🗒️:

- There are instances when the entire context may not be available within the last question by the bot. Some context may be available earlier in the conversation history. Such instances are outside the scope for this project. These instances can be classified as “NOT_APPLICABLE”. This feature would be a bonus but is not required in the AI algorithm.
- We’re a super small, but highly driven team thriving for excellence. That said, there may be some rows where the human evaluation may be incorrect. Please feel free to highlight those rows and correct them for your accuracy calculation. Upon submission, we’ll make the edits on our end. We’d really appreciate your help.
- Please submit your work to [rachiket@coteach.io](mailto:rachiket@coteach.io)