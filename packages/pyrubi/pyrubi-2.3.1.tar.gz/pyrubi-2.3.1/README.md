<h1>Pyrubi 2.3.1</h1>

> Pyrubi is a powerful and easy library for building self Bots in Rubika

<p align='center'>
    <img src='https://iili.io/HIjPRS9.jpg' alt='Pyrubi Library 2.3.1' width='356' class="image">
</p>

<p align='center'>
    <a href='https://github.com/AliGanji1/pyrubi'>GitHub</a>
    •
    <a href='https://rubika.ir/pyrubika'>Documents</a>
</p>

[![Downloads](https://static.pepy.tech/badge/pyrubi)](https://pepy.tech/project/pyrubi)

**The Pyrubi library is compatible with version 6 of the Rubik's API**

<hr>

## Install or Update:

``` bash
pip install -U pyrubi
```

<hr>

## Example:

``` python
from pyrubi import Bot

bot = Bot("sessionName")

for update in bot.on_message():
    if update.text() == 'hello':
        bot.send_text(update.chat_id(), f"**Hello** ``{update.author_title()}``. __This message is from the Pyrubi library.__", update.message_id())
```

<hr>

## Features:
    
- **Fast** : *The requests are very fast.*

- **Easy** : *All methods and features are designed as easy and optimal as possible*

- **Powerful** : *While the library is simple, it has high speed and features that make your work easier and faster*


<hr>

## Social Media:
### <a href='https://rubika.ir/pyrubika'>Rubika</a>

<hr>

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=AliGanji1/Pyrubi&type=Date)](https://star-history.com/#AliGanji1/Pyrubi&Date)