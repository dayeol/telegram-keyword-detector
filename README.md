## Introduction

This Telegram Bot eavesdrops any chats and detects some keywords.
You can subscribe or unsubscribe from the detection alert, and also add/remove the keywords.

## Installation

This bot depends on telepot. 

```
sudo pip install telepot
```

You should set your API Token in the ".telegram\_bot\_secret" file.

## Execution

Execute this at your server
```
python telebot.py 
```

## Usage

/subscribe 		: Subscribe the chat room in which you're typing this command. If you subscribe, the bot will send an alert whenever it detects any keywords.

/unsubscribe	: Unsubscribe from the bot alert

/list					: List the keywords

/add <keyword> : Add keyword

/remove <keyword> : Remove the keyword
