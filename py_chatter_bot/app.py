"""
py_chat_bot

A basic Python chat bot built using chatterbox 

"""

import time
from pathlib import Path
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot

nori = ChatBot('Nori',
              logic_adapters=[
                  'chatterbot.logic.MathematicalEvaluation',
                  'chatterbot.logic.TimeLogicAdapter'
              ],
              storage_adapter='chatterbot.storage.SQLStorageAdapter')
list_trainer = ListTrainer(nori)
corpus_trainer = ChatterBotCorpusTrainer(nori)


def main():
    """
    main function in py_chatter_bot

    """

    print("\n\nCreating and training NoriChat...\n")
    create()
    print('Nori is ready to chat!')
    chat()


def create():
    """
    function that trains the chatbot

    """
    use_custom = input("\n\nUse custom corpus? y/n\n")
    if use_custom == "y":
        print("\nPlease type the list corpus filename below\n")
        print("\nMust be a list format txt file located in /assets\n")
        time.sleep(.4)
        corpus_filename = input("Filename:>  ")
        data_folder = Path("assets/")
        file_to_open = data_folder / corpus_filename
        conv = open(file_to_open, 'r').readlines()
        # conv =  open('../assets/basic_1.txt', 'r').readlines()
        list_trainer.train(conv)
    else:
        corpus_trainer.train("chatterbot.corpus.english")


def get_feedback():

    text = input()

    if 'yes' in text.lower():
        return True
    elif 'no' in text.lower():
        return False
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


def chat():
    """
    chat with the chatbot using an inf loop

    """

    print('\nPress ctrl-c or ctrl-d on the keyboard to exit\n')
    time.sleep(.5)

    while True:
        try:
            user_input = input('You: ')
            bot_response = nori.get_response(user_input)
            print("Nori: {}".format(bot_response))

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


if __name__ == '__main__':
    main()
