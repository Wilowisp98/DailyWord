import requests
from bs4 import BeautifulSoup
from typing import Dict

class DailyWord:
    def __init__(self, url: str = 'https://dicionario.priberam.org/') -> None:
        self.url = url
        try:
            self.response = self.run_request()
            self.parsed_response = self.parse_html()
            self.word_data = self.extract_word_data()
        except Exception as e:
            print(f"Error initializing DailyWord: {e}")
            self.word_data = {}

    def run_request(self) -> requests.Response:
        response = requests.get(self.url)
        response.raise_for_status()
        return response

    def parse_html(self) -> BeautifulSoup:
        return BeautifulSoup(self.response.text, 'html.parser')

    def extract_word_data(self) -> Dict[str, str]:
        word = syllables = definition = etymology = ""
        
        word_element = self.parsed_response.select_one('div .varpt')
        if word_element:
            word = word_element.text.strip()

        syllable_element = self.parsed_response.select_one('.dp-divisao-silabica .titpalavra')
        if syllable_element:
            syllables = syllable_element.text.strip()

        definition_element = self.parsed_response.select_one('.dp-definicao-linha .def')
        if definition_element:
            definition = definition_element.text.strip()
            definition = definition[:-1] if definition else ""

        etymology_element = self.parsed_response.select_one('.dp-seccao-icon .def')
        if etymology_element:
            etymology = etymology_element.text.strip()
            etymology = etymology[:-1] if etymology else ""

        return {
            'word': word,
            'syllables': syllables,
            'definition': definition,
            'etymology': etymology
        }