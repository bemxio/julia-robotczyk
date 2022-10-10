import markovify
import fbchat

from typing import List
import json

class Robotczyk(fbchat.Client):
    def __init__(self, dataset: List[str], mentions: List[str], *args, **kwargs):
        self.chain = markovify.NewlineText(dataset, well_formed=False)
        self.mentions = mentions

        super().__init__(*args, **kwargs)
    
    def is_mentioned(self, message_object: fbchat.Message) -> bool:
        if message_object.replied_to is not None and message_object.replied_to.author == self.uid:
            return True
        
        for mention in self.mentions:
            if mention in message_object.text:
                return True
    
        return False
    
    def onMessage(self, message_object: fbchat.Message, thread_id: str, thread_type: fbchat.ThreadType, **kwargs):
        if message_object.author == self.uid:
            return

        if not self.is_mentioned(message_object):
            return

        text = self.chain.make_sentence(tries=1000)
        message = fbchat.Message(text=text, reply_to_id=message_object.uid)

        self.send(message, thread_id=thread_id, thread_type=thread_type)
    
if __name__ == "__main__":
    with open("credentials.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)

    with open("dataset.json", "r", encoding="utf-8") as file:
        dataset = json.load(file)
    
    client = Robotczyk(dataset, ["@Julia Robotczyk", "@Kornelia"], **credentials)
    
    try:
        client.listen()
    except KeyboardInterrupt:
        client.logout()