from modules.markov import ConversationalChain
import fbchat
import json

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
    
    # event listeners
    def onMessage(self, message_object: fbchat.Message, thread_id: str, thread_type: fbchat.ThreadType, **kwargs):
        if message_object.author == self.uid:
            return

        if not self.is_mentioned(message_object):
            return

        content = self.clean_message(message_object.text)
        response = self.chain.generate(content)

        message = fbchat.Message(text=response, reply_to_id=message_object.uid)

        self.send(message, thread_id=thread_id, thread_type=thread_type)
    
if __name__ == "__main__":
    with open("credentials.json", "r", encoding="utf-8") as file:
        credentials = json.load(file)
    
    chain = ConversationalChain(dataset_path="dataset.json")
    client = RobotczykClient(chain, **credentials)
    
    try:
        client.listen()
    except KeyboardInterrupt:
        client.logout()