import random
import json
import time

from modules.markov import ConversationalChain
import fbchat

def random_chance(precent: int) -> bool:
    return random.randint(1, 100) <= precent

class RobotczykClient(fbchat.Client):
    def __init__(self, chain: ConversationalChain, *args, **kwargs):
        self.chain = chain
        self.mentions = ["@kornelia krawiec", "@kornelia"] # TODO: fetch that information on the client's initialization

        super().__init__(*args, **kwargs)
    
    # helper functions
    def is_mentioned(self, message: fbchat.Message) -> bool:
        if message.replied_to is not None and message.replied_to.author == self.uid:
            return True

        content = message.text.lower()

        for mention in self.mentions: 
            if mention in content:
                return True
    
        return False

    def clean_message(self, content: str) -> str:
        clean_content = content.lower()

        for mention in self.mentions:
            if not mention in clean_content:
                continue
            
            clean_content = clean_content.replace(mention, "")
        
        return clean_content
    
    # sender functions
    def send_dots(self, thread_id: str, thread_type: fbchat.ThreadType, reply_to_id: int) -> int:
        dots = "." * random.randint(2, 10)
        message = fbchat.Message(text=dots, reply_to_id=reply_to_id)

        return self.send(message, thread_id=thread_id, thread_type=thread_type)

    # event listeners
    def onMessage(self, message_object: fbchat.Message, thread_id: str, thread_type: fbchat.ThreadType, **kwargs):
        if message_object.author == self.uid:
            return

        if not self.is_mentioned(message_object):
            return

        content = self.clean_message(message_object.text)
        content = self.chain.generate(content)

        if random_chance(10): # chance for sending dots
            self.send_dots(thread_id, thread_type, reply_to_id=message_object.uid)
            response = fbchat.Message(text=content)
        else:
            response = fbchat.Message(text=content, reply_to_id=message_object.uid)
        
        time.sleep(1.0)

        if not random_chance(10): # chance for sending a message for a word
            return self.send(response, thread_id=thread_id, thread_type=thread_type)

        for index, word in enumerate(content.split()):
            if index == 0:
                response = fbchat.Message(text=word, reply_to_id=message_object.uid)
            else:
                response = fbchat.Message(text=word)
            
            self.send(response, thread_id=thread_id, thread_type=thread_type)
            time.sleep(0.5)
        
if __name__ == "__main__":
    with open("credentials.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)
    
    chain = ConversationalChain(dataset_path="dataset.json")
    client = RobotczykClient(chain, **credentials)
    
    try:
        client.listen()
    except KeyboardInterrupt:
        client.logout()