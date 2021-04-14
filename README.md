# Messenger Chat Automatisation
Send messages and pictures to Messenger website using Selenium

## Initial checks
- Check if msedgedriver.exe is the same version as your Microsoft Edge browser.   
  - Open your Edge browser
  - Paste ```edge://settings/help``` in search bar
  - Check first 2 digits of browser version   
If your browser version is different that 89, then download mathcing version from [Microsoft site.](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
- Check if using Python 3

## Installing
```
pip install -r requirements.txt
```

## Usage
Messenger Chat has 1 class
``` Chat() ```

### Sending picture
send_picture() method
```
chat = messenger.Chat()
chat.send_picture('conversation thread', 'path to file', 'mail', 'password')
chat.exit()
```
- conversation thread - numbers after messenger.com/t/
> 123456789 **or** 123456789/
- path to file - path to picture on your PC 
> C:\Users\PC\Desktop\picture.png
- mail - your email or login to  Facebook/Messenger
> example@mail
- password - your password to Facebook/Messenger
> Password123

### Sending text message
send_message() method
```
chat = messenger.Chat()
chat.send_message('conversation thread', 'message', 'mail', 'password')
chat.exit()
```
- conversation thread - numbers after messenger.com/t/
> 123456789 **or** 123456789/
- message - string to be sent as 1 message
> Hello World!
- mail - your email or login to  Facebook/Messenger
> example@mail
- password - your password to Facebook/Messenger
> Password123

# Please use exit() method to remove background processes
While Messenger Chat is running, it creates a lot of processes that can stay in the background.
CMD command to remove all background processes.
```
taskkill /IM msedgedriver.exe /F /T
```
