# -*- coding: utf-8 -*-
from groq import Groq
from typing import Dict, List, Generator

class GroqClient:
    def __init__(self, api_key: str, system_prompt: str, model: str = 'qwen/qwen3-32b'):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.messages = [
            {
              "role": "system",
              "content": system_prompt
            }
        ]

    def ask_question(self, question: str, stream: bool = True) -> str:
        self.add_message(question, 'user')

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=1,
                max_completion_tokens=1024,
                top_p=1,
                stream=stream,
                stop=None
            )

            response = self.process_response(completion=completion)
            self.add_message(response, 'assistant')
            
            return response
        except Exception as e:
            error_msg = f"Error calling Groq API: {str(e)}"
            print(error_msg)
            return error_msg

    def add_message(self, message: str, role: str) -> None:
        self.messages.append(
            {
                "role": role,
                "content": message
            }
        )

    def process_response(self, completion: Generator) -> str:
        response = ''
        try:
            for chunk in completion:
                if chunk.choices and chunk.choices[0].delta.content:
                    response += chunk.choices[0].delta.content or ""

            if '<think>' in response:
                parts = response.split('</think>')
                if len(parts) > 1:
                    response = parts[-1].strip()

            return response
        except Exception as e:
            error_msg = f"Error processing response: {str(e)}"
            print(error_msg)
            return error_msg
            
    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.messages