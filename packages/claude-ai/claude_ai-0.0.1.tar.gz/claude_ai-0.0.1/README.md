# Claude AI Python Wrapper User Guide

This library provides a simple way to interact with the Claude AI API. You can use it to get organizations, get conversations, send messages, and upload files.

## Installation

First, you need to install this library. You can do this via pip:

```bash
pip install claude_ai
```

## Usage

First, you need to import the `ClaudeAPIWrapper` class from `claude_ai.claude`. Then, you can create a `ClaudeAPIWrapper` object using your session key.

```python
from claude_ai.claude import ClaudeAPIWrapper

session_key = "your session key"
api = ClaudeAPIWrapper(session_key)
```

You can find the session key in the Cookie of any request on the claude.ai website. It usually starts with "sessionKey=sk-ant-sid". Just copy the entire Cookie and paste it as your session key.

### How to get the Cookie

1. Open your browser and visit the claude.ai website.
2. Log in with your credentials.
3. Open the developer tools of your browser (F12 key in most browsers).
4. Go to the Network tab.
5. Refresh the page.
6. Click on any request on the left, then find the 'Cookies' section in the headers.
7. Copy the entire Cookie.

Then, you can use this object to get your organizations:

```python
organizations = api.get_organizations()
print(organizations)

organization_uuid = organizations[0]["uuid"]
```

You can also get your conversations:

```python
conversations = api.get_chat_conversations(organization_uuid)
print(conversations)

conversation_uuid = conversations[0]["uuid"]
```

You can use the `create_chat_conversation` function to create a new conversation. You need to provide your `organization_uuid`, which is the unique identifier of your organization. Then, this function will return a dictionary containing the new conversation's information.

```python
new_conversation = api.create_chat_conversation(organization_uuid)
print(new_conversation)

conversation_uuid = new_conversation["uuid"]
```

Then, you can send messages. If you need to upload a file, you can use the `/u` command followed by the file path:

```python
attachments = []
while True:
  message = input("You>>> ")
  # If it's /u, then it's uploading a file, get the file path
  if message.startswith("/u"):
    file_path = message[3:]
    # Remove spaces from the file path
    file_path = file_path.strip()
    response = api.convert_document(file_path, organization_uuid)
    print(response)
    if response is not None:
      attachments.append(response)
      continue
  response = api.send_message(organization_uuid, conversation_uuid, message,
                              attachments)
  attachments = []
  print('Claude>>> ', end='')
  for message in response:
    print(message, end='', flush=True)
  print()
```

In this example, you will enter your message from the command line. If your message starts with `/u`, then the library will try to upload the file you specified. Then, it will add the response of the uploaded file to the attachments list. Then, it will send a new message containing your message and all attachments. Finally, it will print out the response.

## Note

Make sure you set your session key correctly, otherwise you may not be able to interact with the Claude AI API.