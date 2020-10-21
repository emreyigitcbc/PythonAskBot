# Ask BOT

AskBOT is a algorithmic chat bot for ***Schools***. It is very simple and soft. It gets the message, it tries to find soonest possibility and returns the answer.

 - I made this for schools! Not general usage. Anyone can edit this. And start using in their school.

I made this in my own language I translated all variables, comments, but I didn't translate `Brain.json` at all. Sorry for that, I won't translate it.

The bot, answers randomly from paired key's answers.
## Setup

It needs 2 module, `PyQt5 and NLTK`, you must install them with `pip`:

```bash
pip install PyQt5
pip install nltk
```

## Usage

You can start it with command below:
```bash
python FormChat.py
```
If you want to convert to exe, you may have issues with NLTK.

## Editing
So, how can you edit this? Actually it is very simple.
If you want new ask-answer dialog just add these in "Chat":
```json
   {
      "key": [
        "hi",
        "hello"
      ],
      "answer": [
        "Welcome!",
        "Hi, how can i help you?"
      ]
    }
```
If you want new ordered dialog just add these in "Lined":
```json
{
      "code": "last",
      "key": [
        "whats your name",
        "whar re u"
      ],
      "answer": [
        "Im askbot, what re you?",
        "Im askbot, what about you?"
      ],
      "key2": [
        "my name is",
        "my name",
        "im",
        "john"
      ],
      "answer2": [
        "Im glad to meet you {}",
        "nice name huh {}."
      ]
    }
```

You may ask what is the `code`, this is something that takes data from entry and specifies some template.

The code list:
- first : takes the first word of sentence
- last : takes the last word of sentence
- empty : does nothing
- weather : does nothing
- announcements : returns announcements template
- date : returns date
- program : returns weekly class lesson list template
- teachers : returns teacher info template
- exams : returns exams template 

There are several things more to edit but i think they are very clear to understand. You can edit them yourself.
## Contributing
I am not continuing this project but if you create pull request, I can think about it.

## License
[MIT](https://choosealicense.com/licenses/mit/)
