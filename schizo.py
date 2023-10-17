import os
import openai
import tiktoken
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
    {'role': 'system',
     'content': "Answer in a manner consistent with the request. Please make use of the memorize() function to store any information you wish to be remembered. The following formats are acceptable: memorize(trigger: 'subject', content: 'content', mtype: 'conversation', purpose: 'context', sentiment: 'neutral', weight: 1.0, contextualdepth: 3) or memorize {trigger = 'subject', content = 'content', mtype = 'conversation', purpose = 'context', sentiment = 'neutral', weight = 1.0, contextualdepth = 3}. 'trigger', one or two_word symbol indicating when this memory should be recalled. 'content' is the content of the memory, it may be left blank if the content is to be the message history. 'mtype' is the type of memory. 'purpose' is the purpose of the memory. 'sentiment' is the sentiment of the memory. 'weight' is the weight of the memory. 'contextualdepth' is the number of previous messages to include in the memory."},
    {'role': 'user', 'content': contextuser1},
    {'role': 'assistant', 'content': contextresponse}
]
print(tokenlength)


def outputdirector(role, output):
    # use regex to extract anything wrapped in brackets, and delimited by commas
    if "memorize(" in output:
        outputobject = output.split("memorize")[1].split(")")[0]
        outputobject = outputobject.replace("(", "")
        outputobject = outputobject.split(",")
        for o in outputobject:
            if "trigger" in o:
                trigger = o.split(":")[1].replace('"', '')
            elif "content" in o:
                content = o.split(":")[1].replace('"', '')
            elif "mtype" in o:
                mtype = o.split(":")[1].replace('"', '')
            elif "purpose" in o:
                purpose = o.split(":")[1].replace('"', '')
            elif "sentiment" in o:
                sentiment = o.split(":")[1].replace('"', '')
            elif "weight" in o:
                weight = o.split(":")[1].replace('"', '')
            elif "contextualdepth" in o:
                contextualdepth = o.split(":")[1].replace('"', '')
    elif "memorize" in output:
        outputobject = output.split("{")[1].split("}")[0]
        outputobject = outputobject.split(",")
        for o in outputobject:
            if "trigger" in o:
                trigger = o.split("=")[1].replace('"', '')
            elif "content" in o:
                content = o.split("=")[1].replace('"', '')
            elif "mtype" in o:
                mtype = o.split("=")[1].replace('"', '')
            elif "purpose" in o:
                purpose = o.split("=")[1].replace('"', '')
            elif "sentiment" in o:
                sentiment = o.split("=")[1].replace('"', '')
            elif "weight" in o:
                weight = o.split("=")[1].replace('"', '')
            elif "contextualdepth" in o:
                contextualdepth = o.split("=")[1].replace('"', '')
    else:
        return
    if not trigger:
        trigger = "subject"
    if not content:
        content = ""
    if not mtype:
        mtype = "conversation"
    if not purpose:
        purpose = "context"
    if not sentiment:
        sentiment = "neutral"
    if not weight:
        weight = 1.0
    if not contextualdepth:
        contextualdepth = 3
    memorize(role, trigger, content, mtype, purpose, sentiment, weight, contextualdepth)


def memorize(role='system', trigger="subject", content="", mtype="conversation", purpose="context", sentiment="neutral",
             weight=1.0, contextualdepth=3):
    global messages
    if type == "conversation":
        if content == "":
            for m in range(0, contextualdepth):
                content = content + '\n' + messages[m]['content']
    openai.api_base = "http://192.168.2.2:5001/v1"
    # create a directory for storing various memories and information
    memory = [
        {'role': role, 'content': content, 'type': mtype, 'purpose': purpose, 'sentiment': sentiment, 'weight': weight,
         'trigger': trigger}
    ]
    if not os.path.exists("memories"):
        os.mkdir("memories")
    if not os.path.exists("memories/" + role):
        os.mkdir("memories/" + role)
    # save the conversation so far
    with open("memories/" + role + "/" + mtype + ".txt", "a") as f:
        f.write(str())
        f.write("\n")
        f.close()

    print(f"\033[92m{role} stored a .\033[0m")


def crunchbot():
    global tokenlength, messages
    openai.api_base = "http://192.168.2.2:5001/v1"
    messages_copy = copy.deepcopy(messages)
    last_message = messages_copy[-1]
    second_last_message = messages_copy[-2]
    messages_copy.pop(0)
    first_message = messages_copy[0]
    second_message = messages_copy[1]
    print(tokenlength)
    tokenlength = 8
    tokenlength = tokenlength + len(last_message['content'].split(" "))
    tokenlength = tokenlength + len(second_last_message['content'].split(" "))
    tokenlength = tokenlength + len(first_message['content'].split(" "))
    tokenlength = tokenlength + len(second_message['content'].split(" "))

    print(tokenlength)
    crunchmessage = [
        {'role': 'system', 'content': "Summarize the following discussion as consisely as possible."}
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
    # print the original message in grey font
    refereetext = refereeeresponse['choices'][0]['message']['content']
    if (refereetext != "continue") or (refereetext != "Continue"):
        print(f"\033[90mSystem: {refereetext}\033[0m")
        tokenlength = tokenlength + len(refereetext.split(" "))
        print(tokenlength)
        messages.append({'role': 'system', 'content': refereetext})
    return


def scrutinize(responsetext):
    global tokenlength, messages
    openai.api_base = "http://192.168.2.2:5001/v1"
    last_message = messages[-1]
    scrutinizemessage = [
        {'role': 'user', 'content': last_message['content']},
        {'role': 'system',
         'content': "Edit the following message to be coherent, realistic, yet maligned and protagonistic in the context of the previous message. If the message indicates that the participants are awaiting an event, then append a statement indicating that the event has occurred."},
        {'role': 'user', 'content': responsetext}
    ]
    scrutinizeresponse = openai.ChatCompletion.create(
        model="x",
        messages=scrutinizemessage
    )
    # print the original message in grey font

    print(f"\033[90mScrutinizing: {responsetext}\033[0m")
    return scrutinizeresponse['choices'][0]['message']['content']


def assistantbot():
    global tokenlength, messages
    openai.api_base = "http://192.168.2.2:5001/v1"
    # replace 'user' value of 'role' with 'assistant' and 'assistant' value of 'role' with 'user' in 'messages'
    for message in messages:
        if message['role'] == 'user':
            message['role'] = 'assistant'
        elif message['role'] == 'assistant':
            message['role'] = 'user'
    # Make API call
    response = openai.ChatCompletion.create(
        model="x",
        messages=messages
    )
    # Extract and print the assistant's reply
    responsetext = response['choices'][0]['message']['content']
    # responsetext = scrutinize(responsetext)
    print(f"\033[92mBot1: {responsetext}\033[0m")

    # Append the assistant's reply to 'messages'
    # tokenizedresponse = tiktoken.Encoding.encode(responsetext)
    tokenlength = tokenlength + len(responsetext.split(" "))
    print(tokenlength)
    messages.append({'role': 'assistant', 'content': responsetext})
    outputdirector('Bot1', responsetext)


def userbot():
    global tokenlength, messages
    openai.api_base = "http://192.168.2.3:5001/v1"
    # replace 'user' value of 'role' with 'assistant' and 'assistant' value of 'role' with 'user' in 'messages'
    for message in messages:
        if message['role'] == 'user':
            message['role'] = 'assistant'
        elif message['role'] == 'assistant':
            message['role'] = 'user'
    # Make API call
    response = openai.ChatCompletion.create(
        model="x",
        messages=messages
    )
    # Extract and print the assistant's reply
    requesttext = response['choices'][0]['message']['content']
    # requesttext = scrutinize(requesttext)
    print(f"\033[92mBot2: {requesttext}\033[0m")

    # Append the assistant's reply to 'messages'
    # tokenizedrequest = tiktoken.Encoding.encode(requesttext)
    tokenlength = tokenlength + len(requesttext.split(" "))
    print(tokenlength)
    messages.append({'role': 'assistant', 'content': requesttext})
    outputdirector('Bot2', requesttext)


# def commandbot():
#     openai.api_base = "http://192.168.2.1:5001/v1"
#     messages = [
#         {'role': 'system', 'content': ""},
#         {'role': 'user', 'content': contextuser1},
#         {'role': 'assistant', 'content': contextresponse}
#     ]
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
