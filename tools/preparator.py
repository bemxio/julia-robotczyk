import json
import os

def fix_mojibake(text: str) -> str:
    # facebook does a fucky wucky when encoding the text in the data, so this function is supposed fix that
    # see https://stackoverflow.com/questions/50008296/facebook-json-badly-encoded for more details
    return text.encode("latin1").decode("utf-8")

# constants
AUTHOR = "Julia Krawczyk" # the person's name to take messages from
MESSAGE_FILES = ["messages/" + filename for filename in os.listdir("messages")] # files in which the messages are contained
OUTPUT_PATH = "dataset.json" # the path where the dataset will be saved

# main code
messages = []

for path in MESSAGE_FILES:
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    messages.extend([
        fix_mojibake(message["content"]) for message in data["messages"] 
        if "content" in message and message["sender_name"] == AUTHOR
    ])

print(len(messages))

with open("dataset.json", "w", encoding="utf-8") as file:
    json.dump(messages, file, indent=4)