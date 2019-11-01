"""
py_chat_bot

A basic Python chat bot built using chatterbox 

"""

import time
from pathlib import Path
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.conversation import Statement
import logging 
import random

nori = ChatBot('Nori',
               storage_adapter='chatterbot.storage.SQLStorageAdapter',
               logic_adapters=[
                   'chatterbot.logic.BestMatch'
               ],
               database_uri='sqlite:///database.db')
list_trainer = ListTrainer(nori)
corpus_trainer = ChatterBotCorpusTrainer(nori)
logger = logging.getLogger() 
logger.setLevel(logging.CRITICAL)


def main():
    """
    main function in py_chatter_bot

    """

    print("\n\nCreating and training NoriChat...")
    create()
    print('Nori is ready to chat!')
    chat()


def create():
    """
    function that trains the chatbot

    """

    use_custom = input("\nUse custom corpus? y/n\n")
    if use_custom == "y":
        print("\nPlease type the list corpus filename below")
        print("Must be a list format txt file located in /assets\n")
        time.sleep(.4)
        corpus_filename = input("Filename:>  ") + ".txt"
        data_folder = Path("assets/")
        file_to_open = data_folder / corpus_filename
        conv = open(file_to_open, 'r').readlines()
        # conv =  open('../assets/basic_1.txt', 'r').readlines()
        list_trainer.train(conv)
    else:
        corpus_trainer.train(
            "chatterbot.corpus.english"
            )


def get_feedback():

    text = input()

    if 'y' in text.lower():
        return True
    elif 'n' in text.lower():
        return False
    else:
        print('Please type either "Y" or "N"')
        return get_feedback()


def chat():
    """
    chat with the chatbot using an inf loop

    """

    print("Begin chatting with Nori! ")
    print('\nPress ctrl-c or ctrl-d on the keyboard to exit\n')
    time.sleep(.5)
    # The following loop will execute each time the user enters input
    while True:
        try:
            user_input = input("You: ")
            input_statement = Statement(user_input)
            response = nori.get_response(
                input_statement
            )

            # get feedback every few questions
            r_int = random.randint(0, 10)
            if r_int < 9:
                print("Nori: {}".format(response))
            else:
                print('\n Is "{}" a coherent response to "{}"? y/n\n'.format(
                    response.text,
                    input_statement.text
                ))
                if get_feedback() is False:
                    print('please input the correct one')
                    correct_response = Statement(text=input())
                    nori.learn_response(correct_response, input_statement)
                    print('Responses added to bot!')
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


if __name__ == '__main__':
    main()
