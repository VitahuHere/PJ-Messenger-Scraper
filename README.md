# Facebook Messenger Chat Automatisation
Send messages and pictures to Messenger website using Selenium

## Initial checks
- Check if Python 3 is installed
- Check if modern Google Chrome is installed

## Installing dependencies
```
pip install -r requirements.txt
```

## Notice
For security reasons, credentials are base64 encoded.\
Additionally, you can use .env file to store credentials. \
In this project python-decouple is used to load .env file.\

## Usage
Facebook Messenger Chat has 1 class\
``` Facebook(email: base64 encoded str, password: base64 encoded str) ```

### Sending picture
send_image() method
```python
chat = fbchat.Facebook()
chat.send_image('path_to_file': str, conversation_thread: str | int)
```
- conversation thread - numbers after messenger.com/t/
> 123456789 **or** 123456789/
- path to file - path to picture on your PC 
> C:\Users\PC\Desktop\picture.png

### Sending text message
send_message() method
```python
chat = fbchat.Chat()
chat.send_message('conversation thread', 'message')
```
- conversation thread - numbers after messenger.com/t/
> 123456789 **or** 123456789/
- message - string to be sent as 1 message
> Hello World!

### Chaining methods
```python
fbchat.Chat(email, pass)
.send_message('conversation thread', 'message')
.send_image('path_to_file', 'conversation_thread')
```

### Session
Even though credentials are required at initialization, 
Facebook() with reuse session cookies from previous session,
and skip login process.

# PJAIT/PJATK schedule scraper

## Example usage
```python
scraper = PJScraper(
    student_id=base64.b64encode(config("PJ_ID").encode("utf-8")).decode("utf-8"),
    password=base64.b64encode(config("PJ_PASS").encode("utf-8")).decode("utf-8"),
).get_classes_schedule(0)
```

## Methods
### get_classes_schedule()

accepts 1 argument - day of the week as number \
0 - Monday \
1 - Tuesday \
2 - Wednesday \
... \
6 - Sunday \

returns a dict of classes for given day
```python
{
    "MUL ćwiczenia A215": {
        "start": "10:15",
        "end": "11:45",
    },
    "ASD wykład A1": {
        "start": "12:15",
        "end": "13:45",
    },
}
```
