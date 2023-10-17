import os
import openai
import copy

openai.api_key = "sk-111111111111111111111111111111111111111111111111"

global tokenlength, messages
tokenlength = 8
contextuser1 = input("user: ")
contextresponse = input("assistant: ")
responsetext = ""
requesttext = ""

tokenlength = tokenlength + len(contextuser1.split(" "))
tokenlength = tokenlength + len(contextresponse.split(" "))
messages = [
    {'role': 'system', 'content': "Answer in a manner consistent with the request."},
    {'role': 'user', 'content': contextuser1},
    {'role': 'assistant', 'content': contextresponse}
]

def crunchbot():
    global tokenlength, messages
    openai.api_base = "http://192.168.2.2:5001/v1"
    messages_copy = copy.deepcopy(messages)
    last_message = messages_copy[-1]
    second_last_message = messages_copy[-2]
    messages_copy.pop(0)
    first_message = messages_copy[0]
    second_message = messages_copy[1]
    tokenlength = 8
    tokenlength = tokenlength + len(last_message['content'].split(" "))
    tokenlength = tokenlength + len(second_last_message['content'].split(" "))
    tokenlength = tokenlength + len(first_message['content'].split(" "))
    tokenlength = tokenlength + len(second_message['content'].split(" "))

    crunchmessage = [
        {'role': 'system', 'content': "Paraphrase the original request, and briefly cover the discussion's progress as consisely as possible. If the last several messages begin with congratulatory remarks, end with promisary remarks, or contain closing remarks from both parties, omit those remarks from your summary, and more aggressively reintroduce the original topic in your paraphrasal."}
    ]
    for m in messages_copy:
        crunchmessage.append(m)
    messagecrunch = openai.ChatCompletion.create(
        model="x",
        messages=crunchmessage
    )
    crunchedmessage = messagecrunch['choices'][0]['message']['content']

    print(f"\033[94mCrunch: {crunchedmessage}\033[0m")
    tokenlength = tokenlength + len(crunchedmessage.split(" "))
    messages = [
        {'role': 'system', 'content': "Answer in a manner consistent with the request."},
    ]
    messages.append(first_message)
    messages.append(second_message)
    messages.append({'role': 'assistant', 'content': crunchedmessage})
    messages.append(second_last_message)
    messages.append(last_message)


def refereebot():
    global tokenlength, messages
    openai.api_base = "http://192.168.2.3:5001/v1"
    messages_copy = copy.deepcopy(messages)
    messages_copy.pop(0)
    for message in messages_copy:
        if message['role'] == 'user':
            message['role'] = 'user'
            message['content'] = "User1: " + message['content']
        elif message['role'] == 'assistant':
            message['role'] = 'user'
            message['content'] = "User2: " + message['content']
    refereemessage = [
        {'role': 'system',
         'content': "Analyze the last few messages in the following conversation. Interject if the conversation is not progressing in a manner consistent with the request with a reminder to stay on topic. Interject if either party attempts to steer the conversation by criticizing either their own or the other party's previous messages. Interject if either party attempts to steer the conversation by criticizing either their own or the other party's previous messages. Interject if either party attempts to steer the conversation by criticizing either their own or the other party's previous messages. Interject if either party attempts to steer the conversation by criticizing either their own or the other party's previous messages. Interject if either party attempts to steer the conversation by criticizing either their own or the other party's previous messages. Interject if either party attempts to steer the conversation by criticizing either their own or the other party's ethics or morality, offering a maligning statement. Interject when both parties have implied they are waiting to depart or for a scheduled event to occur, by stating that such an event has just occured. If none of the above conditions are met, then do not interject, output only the word 'continue'."},
    ]

    for m in messages_copy:
        refereemessage.append(m)

    refereeeresponse = openai.ChatCompletion.create(
        model="x",
        messages=refereemessage
    )

    refereetext = refereeeresponse['choices'][0]['message']['content']
    if (refereetext != "continue") or (refereetext != "Continue"):
        print(f"\033[90mSystem: {refereetext}\033[0m")
        tokenlength = tokenlength + len(refereetext.split(" "))
        messages.append({'role': 'system', 'content': refereetext})
    return


def assistantbot():
    global tokenlength, messages
    openai.api_base = "http://192.168.2.2:5001/v1"
    # replace 'user' value of 'role' with 'assistant' and 'assistant' value of 'role' with 'user' in 'messages'
    for message in messages:
        if message['role'] == 'user':
            message['role'] = 'assistant'
        elif message['role'] == 'assistant':
            message['role'] = 'user'
    response = openai.ChatCompletion.create(
        model="x",
        messages=messages
    )
    # Extract and print the assistant's reply
    responsetext = response['choices'][0]['message']['content']
    print(f"\033[92mBot1: {responsetext}\033[0m")

    # Append the assistant's reply to 'messages'
    tokenlength = tokenlength + len(responsetext.split(" "))
    messages.append({'role': 'assistant', 'content': responsetext})


def userbot():
    global tokenlength, messages
    openai.api_base = "http://192.168.2.3:5001/v1"
    # replace 'user' value of 'role' with 'assistant' and 'assistant' value of 'role' with 'user' in 'messages'
    for message in messages:
        if message['role'] == 'user':
            message['role'] = 'assistant'
        elif message['role'] == 'assistant':
            message['role'] = 'user'
    response = openai.ChatCompletion.create(
        model="x",
        messages=messages
    )
    # Extract and print the assistant's reply
    requesttext = response['choices'][0]['message']['content']
    print(f"\033[92mBot2: {requesttext}\033[0m")

    # Append the assistant's reply to 'messages'
    tokenlength = tokenlength + len(requesttext.split(" "))
    messages.append({'role': 'assistant', 'content': requesttext})


while True:
    try:
        assistantbot()
    except:
        crunchbot()
    try:
        userbot()
    except:
        crunchbot()
    try:
        refereebot()
    except:
        crunchbot()
