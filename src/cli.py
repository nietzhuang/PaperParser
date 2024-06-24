import six
import configparser
import re

from pyfiglet import figlet_format
from pyconfigstore import ConfigStore
from PyInquirer import (Token, ValidationError, Validator, print_json, prompt,
                        style_from_dict)
from prompt_toolkit import document

try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None

config = configparser.ConfigParser()

style = style_from_dict({
  })


def ask(type, name, message, validate=None, choices=[]):
    questions = [
        {
            'type': type,
            'name': name,
            'message': message,
            'validate': validate,
        },
    ]
    if choices:
        questions[0].update({
            'choices': choices,
        })
    answers = prompt(questions, style=style)
    return answers

def run():
    from main import PaperParser as PParser

    def askCookie():
        cookie = ask(type='input',
                     name='cookie',
                     message='Enter PHPSESSID cookie (Only needed to provide once):')
        config['DEFAULT']['cookie'] = cookie['cookie']

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        return cookie['cookie']

    # log("SteamGifts Bot", color="blue", figlet=True)
    # log("Welcome to SteamGifts Bot!", "green")
    # log("Created by: github.com/stilManiac", "white")

    config.read('config.ini')
    if not config['DEFAULT'].get('cookie'):
        cookie = askCookie()
    else:
        re_enter_cookie = ask(type='confirm',
                            name='reenter',
                            message='Do you want to enter new cookie?')['reenter']
        if re_enter_cookie:
            cookie = askCookie()
        else:
            cookie = config['DEFAULT'].get('cookie')

    conf_list = ask(type='list',
                 name='conf_list',
                 message='Select Conference:',
                 choices=[
                     'ISSCC',
                     'MICRO',
                     'ISCA',
                     'DATE',
                     'DAC',
                     'ASP-DAC',
                     'HPCA'
                 ])['conf_list']

    P = PParser(cookie, conf_list)
    P.start()


if __name__ == '__main__':
    run()


