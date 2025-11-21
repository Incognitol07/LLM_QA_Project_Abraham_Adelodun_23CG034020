import os
import openai
import string
from dotenv import load_dotenv

load_dotenv()

def preprocess(question):
    question = question.lower()
    question = question.translate(str.maketrans("", "", string.punctuation))
    return question


def get_answer(question):
    if not os.getenv("GITHUB_TOKEN"):
        return "Error: GITHUB_TOKEN environment variable not set."
    client = openai.OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=os.getenv("GITHUB_TOKEN"),
    )
    prompt = f"Answer the following question: {question}"
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    question = input("Enter your question: ")
    processed = preprocess(question)
    print(f"Processed question: {processed}")
    answer = get_answer(processed)
    print(f"Answer: {answer}")
