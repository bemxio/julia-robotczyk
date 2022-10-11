import markovify
import fbchat
import spacy

from typing import List
import json

class Robotczyk(fbchat.Client):
    def __init__(self, dataset: List[str], mentions: List[str], *args, **kwargs):    
        self.nlp = spacy.load("pl_core_news_sm")

        self.mentions = mentions
        self.dataset = dataset

        super().__init__(*args, **kwargs)
    
    # helper functions (mostly for mentions)
    def is_mentioned(self, message_object: fbchat.Message) -> bool:
        if message_object.replied_to is not None and message_object.replied_to.author == self.uid:
            return True
        
        content = message_object.text.lower()

        for mention in self.mentions:
            if mention in content:
                return True
    
        return False

    def cleanify(self, content: str) -> str:
        clean = content.lower()
        
        for mention in self.mentions:
            if not mention in clean:
                continue
            
            clean = clean.replace(mention, "")
        
        return clean
    
    def keyword(self, content: str) -> str:
        if not content:
            return ""
        
        doc = self.nlp(content)
        subjects = [token.text for token in doc if token.dep_ in ("nsubj", "nsubj:pass")]

        if subjects:
            return subjects[0]
        else:
            return next((token.text for token in doc if token.dep_ == "ROOT"), "")
        
    # event listeners
    def onMessage(self, message_object: fbchat.Message, thread_id: str, thread_type: fbchat.ThreadType, **kwargs):
        if message_object.author == self.uid:
            return

        if not self.is_mentioned(message_object):
            return

        content = self.cleanify(message_object.text)
        keyword = self.keyword(content)

        dataset = [text for text in self.dataset if keyword in text.lower()]

        chain = markovify.NewlineText(
            dataset, 
            state_size=3,
            well_formed=False
        )

        text = chain.make_sentence(tries=100000) or "..."
        message = fbchat.Message(text=text, reply_to_id=message_object.uid)

        self.send(message, thread_id=thread_id, thread_type=thread_type)
    
if __name__ == "__main__":
    with open("credentials.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)

    with open("dataset.json", "r", encoding="utf-8") as file:
        dataset = json.load(file)
    
    client = Robotczyk(dataset, ["@julia robotczyk", "@kornelia krawiec", "@kornelia"], **credentials)
    
    try:
        client.listen()
    except KeyboardInterrupt:
        client.logout()