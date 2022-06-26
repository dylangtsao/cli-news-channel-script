from plumbum import cli, colors
from pyfiglet import Figlet
import yaml, ruamel.yaml
import os, fnmatch
import questionary
from questionary import prompt
from datetime import datetime
import textwrap

author = ""
broadcaster = ""
script_name = ""


def print_banner(text):
    with colors['SkyBlue2']:
        print(Figlet(font="cyberlarge").renderText(text))

def load_config(filename):
    global author, broadcaster
    if not os.path.exists(filename):
        save_config(filename, {
            "author":'',
            "broadcaster": ''
        })
    with open(filename, "r") as file:
        data = yaml.safe_load(file)
    author = data['author']
    broadcaster = data['broadcaster']
   

def save_config(filename, config):
    yaml = ruamel.yaml.YAML()

    with open(filename, "w") as file:
        yaml.dump(config, file)

def init_folder(folder_name):
    try:
        os.makedirs(folder_name)
    except OSError:
        print(f"There was an error creating directory {folder_name}")
    os.chdir(folder_name)
    add_page()

def create_script():
    global author, broadcaster, script_name
    author = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("What is your name?").ask())
    broadcaster = ruamel.yaml.scalarstring.DoubleQuotedScalarString(questionary.text("Who is the script for?").ask())

    my_dict = dict(author=author, broadcaster=broadcaster)

    save_config("config.yaml", my_dict)
    script_name = f"{author}-{broadcaster.upper()}"
    init_folder(script_name)
    
def open_script():
    global broadcaster, author, script_name
    today_entry = str(datetime.today().strftime('%Y-%m-%d'))+ ".txt"
    script_name = f"{author}-{broadcaster.upper()}"
    os.chdir(script_name)
    entry_list = os.listdir()

    if not entry_list:
        add_page()
    for entry in entry_list:
        if fnmatch.fnmatch(entry, today_entry):
            add_content(today_entry)
        else:
            add_page()

def retrieve_script():
    global broadcaster, author, script_name
    script_name = f"{author}-{broadcaster.upper()}"
    os.chdir(script_name)
    script_list = os.listdir()

    question = [{
        "type": "select",
        "name": "select_entry",
        "message": "Choose an entry to retrieve",
        "choices": script_list
    },]
    entry = prompt(question)['select_entry']
    with open(entry, 'r') as e:
        print(e.read())

def add_content(title):
    with open(title, 'a') as entry:
        writing = questionary.text(f"Input Script for {broadcaster}").ask()
        prettier_writing=textwrap.fill(writing)+"\n"
        entry.write(prettier_writing)

def add_page():
    today_entry = str(datetime.today().strftime('%Y-%m-%d'))+ ".txt"
    open(today_entry, 'x')
    print(f"Script Entry Created: {today_entry}")
    add_content(today_entry)

class NScript(cli.Application):
    VERSION = "0.0"

    def main(self):
        global author, broadcaster
        load_config("config.yaml")
        print_banner("News Channel Script")

        choice = questionary.select(
            "What would you like to do?",
            choices = [
                'Input',
                'Retrieve',
                'Quit'
            ]
        ).ask()
        if choice == 'Input':
            if broadcaster == "":
                create_script()
            open_script()
        elif choice == 'Retrieve':
            retrieve_script()
        elif choice == 'Quit':
            print("Goodbye!")
    
if __name__ == "__main__":
    NScript()