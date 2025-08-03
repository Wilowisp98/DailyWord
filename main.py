from src.daily_word import *
from src.groq_client import *

from env import GROQ_API_KEY, DICTIONARY_URL, GROQ_MODEL, generate_system_prompt

def main():
    daily_word = DailyWord(url=DICTIONARY_URL)
    
    word_data = daily_word.word_data
    
    if not word_data or not word_data.get('word'):
        print("Failed to retrieve the word of the day.")
        return
    
    system_prompt = generate_system_prompt(word_data)
    groq_client = GroqClient(api_key=GROQ_API_KEY, system_prompt=system_prompt, model=GROQ_MODEL)
    
    print("\nBem-vindo ao DailyWord!")
    print(f"A palavra de hoje é: {word_data.get('word', '')}")
    print("Tenta adivinhar o significado desta palavra.")
    
    while True:
        user_input = input("\nFaz uma pergunta (ou 'sair/exit/quit' para terminar): ")
        if user_input.lower() in ['sair', 'exit', 'quit']:
            break
        
        response = groq_client.ask_question(user_input)
        print(f"\n{response}")
        
        if 'acertaste na moeda' in response.lower():
            break

if __name__ == "__main__":
    main()