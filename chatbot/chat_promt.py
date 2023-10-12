import requests
import os
from dotenv import load_dotenv

load_dotenv()
CHAT_GPT_API_KEY = os.environ.get('CHAT_GPT_API_KEY')


class ChatGPTClient:
    def __init__(self, api_key=CHAT_GPT_API_KEY):
        self.api_key = api_key
        self.url = "https://api.openai.com/v1/chat/completions"

    def ask_question(self, question):
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
        }

        response = requests.post(self.url, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return None


# example:
# gpt_client = ChatGPTClient()

# question = "Who is the prime minister of India?"
# answer = gpt_client.ask_question(question)
# print(answer)
