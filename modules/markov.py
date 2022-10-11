import markovify
import spacy

from typing import Union
import pathlib
import json

class ConversationalChain:
    def __init__(self, dataset_path: Union[pathlib.Path, str]):
        self.dataset = self._load_dataset(dataset_path)
        self.nlp = spacy.load("pl_core_news_sm")
    
    def _load_dataset(self, path: Union[pathlib.Path, str]) -> dict:
        with open(path, "r", encoding="utf-8") as file:
            dataset = json.load(file)
        
        return dataset
    
    def keyword(self, prompt: str) -> str:
        if not prompt:
            return ""
        
        doc = self.nlp(prompt)
        subjects = [token.text for token in doc if token.dep_ in ("nsubj", "nsubj:pass")]

        if subjects:
            return subjects[0]
        else:
            return next((token.text for token in doc if token.dep_ == "ROOT"), "")
        
    def generate(self, prompt: str) -> str:
        keyword = self.keyword(prompt)
        dataset = [text for text in self.dataset if keyword in text.lower()]

        if len(dataset) < 1000:
            state_size = 1
        else:
            state_size = 2

        chain = markovify.NewlineText(dataset, state_size=state_size, well_formed=False)
        
        return chain.make_sentence(tries=1000)