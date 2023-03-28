# Facebook Messenger Chat Automatisation
Send messages and pictures to Messenger website using Selenium

## Initial checks
- Check if Python 3 is installed
- Check if modern Google Chrome is installed

## Installing dependencies
```
pip install -r requirements.txt
```

## Usage
Facebook Messenger Chat has 1 class\
``` Facebook(email: base64 encoded str, password: base64 encoded str) ```

### Sending picture
send_image() method
```
chat = fbchat.Facebook()
chat.send_image('path_to_file': str, conversation_thread: str | int)
```
- conversation thread - numbers after messenger.com/t/
> 123456789 **or** 123456789/
- path to file - path to picture on your PC 
> C:\Users\PC\Desktop\picture.png

### Sending text message
send_message() method
```
chat = fbchat.Chat()
chat.send_message('conversation thread', 'message')
```
- conversation thread - numbers after messenger.com/t/
> 123456789 **or** 123456789/
- message - string to be sent as 1 message
> Hello World!

### Chaining methods
```
fbchat.Chat(email, pass)
.send_message('conversation thread', 'message')
.send_image('path_to_file', 'conversation_thread')
```

### Session
Even though credentials are required at initialization, 
Facebook() with reuse session cookies from previous session,
and skip login process.
```
