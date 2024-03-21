"""
    User Interface Modul
"""

import os
import src.address_book
import src.notes

# ------------
from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.history import InMemoryHistory

# Color text ON
# RED = "\033[91m"
# GREEN = "\033[92m"
# YELLOW = "\033[93m"
# RESET = "\033[0m"
# BLUE = "\033[94m"
# FLY_BLUE = "\033[38;5;117m"he
# PURPURE = "\033[35m"

# Color text OFF
RED = ""
GREEN = ""
YELLOW = ""
RESET = ""
BLUE = ""
FLY_BLUE = ""
PURPURE = ""

def help_info():
    print(f'    {PURPURE}List of comand:{RESET}\n'
            f'-{YELLOW} "record contact" {BLUE} - Interacting with contacts.{RESET}\n'
            f'-{YELLOW} "record note" {BLUE} - Interacting with notes.{RESET}\n'
            f'-{YELLOW} "help" {BLUE} - Help{RESET}\n'
            f'-{YELLOW} "exit"  {BLUE} - Exit from program.\n{RESET}')

def help_record_contact():
    print(f"   {PURPURE}List of commands for 'record contacts':{RESET}\n"
            f"-{YELLOW} 'add' {BLUE} - add contact to phone book{RESET}\n"
            f"-{YELLOW} 'all' {BLUE} - show all records{RESET}\n"
            f"-{YELLOW} 'add tel' {BLUE} - add phone number to record with Name{RESET}\n"
            f"-{YELLOW} 'delete' {BLUE} - delete record from list{RESET}\n"
            f"-{YELLOW} 'find' {BLUE} - search for records by part of a name or phone number{RESET}\n"
            f"-{YELLOW} 'help' {BLUE} - help{RESET}\n"
            f"-{YELLOW} 'main menu' of 'back' {BLUE} - Return to main menu{RESET}\n"
            f"-{YELLOW} exit  {BLUE} - exit from program\n{RESET}")


def help_record_note():
    print(f"   {PURPURE}List of comand for 'record note':{RESET}\n"
            f"-{YELLOW} 'add content' {BLUE} - Add a note.{RESET}\n"
            f"-{YELLOW} 'edit content' {BLUE} - Edit note text.{RESET}\n"
            f"-{YELLOW} 'edit tag' {BLUE} - Edit tag.{RESET}\n"
            f"-{YELLOW} 'remove tag' {BLUE} - Delete tag.{RESET}\n"
            f"-{YELLOW} 'remove note' {BLUE} - Delete note.{RESET}\n"
            f"-{YELLOW} 'find by content' {BLUE} - Search within note text.{RESET}\n"
            f"-{YELLOW} 'find by tag' {BLUE} - Search within tag.{RESET}\n"
            f"-{YELLOW} 'sort by tag' {BLUE} - Sort by tags.{RESET}\n"
            f"-{YELLOW} 'show all' or 'all' {BLUE} - Show all notes and their keys.{RESET}\n"
            f"-{YELLOW} 'help' {BLUE} - help.{RESET}\n"
            f"-{YELLOW} 'main menu' of 'back' {BLUE} - Return to main menu{RESET}\n"
            f"-{YELLOW} exit  {BLUE} - exit from program\n{RESET}")

class MyCompleter(Completer):
    def __init__(self, commands):
        self.commands = commands

    def get_completions(self, document, complete_event):
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        for command in self.commands:
            if command.startswith(word_before_cursor):
                yield Completion(command, start_position=-len(word_before_cursor))

def start_bot():
    print(f'{YELLOW}Hello! I`m your personal assistant! To finish working please enter {RED}"exit"{YELLOW}. To view all commands please enter "help"{RESET}')

    base_path = os.path.dirname(__file__)
    filename_address_book = os.path.join(base_path, "..", "files", "save_contacts.bin")
    filename_note_book = os.path.join(base_path, "..", "files", "save_notes.bin")

    try:
        book = src.address_book.read_from_file(filename_address_book)
        book.find_birthday_people()
    except Exception:
        book = src.address_book.AddressBook()

    try:
        note = src.notes.NoteBook.load_pickle(filename_note_book)
    except Exception:
        note = src.notes.NoteBook()
    
    PROGRAM_STATUS = True

    while PROGRAM_STATUS:
        
        history = InMemoryHistory()
        completer = MyCompleter(['record contact','record note','help','exit'])
        
        try:
            data = prompt(">",
                                completer=completer,
                                history=history,
                                complete_while_typing=True)
            data.lower()

            if data == "record contact":
                while True:
                    history = InMemoryHistory()
                    completer = MyCompleter(['add', 'add tel', 'delete',
                                'find','all','back','main menu','help', 'exit'])


                    try:
                        input_data = prompt("Enter command: ",
                                    completer=completer,
                                    history=history,
                                    complete_while_typing=True)
                        input_data.lower()
                        
                        if input_data == "exit":
                            book.save_to_file(filename_address_book)
                            PROGRAM_STATUS = False
                            break
                        elif input_data == 'main menu' or input_data == 'back':
                            book.save_to_file(filename_address_book)
                            print(f"{YELLOW} You have returned to the main menu.")
                            break
                        elif input_data == "help":
                            help_record_contact()
                        elif input_data == "add":
                            name = input(f"{GREEN}Enter name: {RESET}")
                            if (name):
                                record = src.address_book.Record(name)
                                phone = input(f"{GREEN}Enter phone number (or press 'Enter' to continue): {RESET}")
                                if phone:
                                    record.add_phone(phone)
                                birthday = input(
                                    f"{GREEN}Enter date of birth [DD-MM-YYYY](or press 'Enter' to continue): {RESET}")
                                if birthday:
                                    record.add_birthday(birthday)
                                email = input(f"{GREEN}Enter email (or press 'Enter' to continue): {RESET}")
                                if email:
                                    record.add_email(email)
                                address = input(f"{GREEN}Enter address (or press 'Enter' to continue): {RESET}")
                                if address:
                                    record.add_address(address)
                                book.add_record(record)
                                book.save_to_file(filename_address_book)
                        elif input_data == "add tel":
                            name = input(f"{GREEN}Enter name: {RESET}")
                            if (name):
                                rec = book.find(name)
                                if rec:
                                    phone = input(f"{GREEN}Enter phone number: {RESET}")
                                    rec.add_phone(phone)
                                else:
                                    print(f"{RED}The name {name} was not found in the address book")
                            book.save_to_file(filename_address_book)
                        elif input_data == "delete":
                            name = input(f"{GREEN}Enter name: {RESET}")
                            if (name):
                                nam = book.delete(name)
                                if nam:
                                    print(f"{nam} deleted from address book")
                                else:
                                    print(f"{RED}The name {name} was not found in the address book")
                            book.save_to_file(filename_address_book)
                        elif input_data == "find":
                            find_contact = input(f"{GREEN}Enter text for searching (part of name or phone number): {RESET}")
                            book.get_find(find_contact)

                        elif input_data == "all":
                            n = -1
                            if len(book.data.items()) > 10:
                                n = 10
                            book.get_all(n)
                        else:
                            print(
                                f'{RED}Command "{data}" not found. The following command will "help" you know what the commands are.')
                    except:
                        print('Something went wrong, restart the program')

            elif data == 'record note':
                while True:
                    history = InMemoryHistory()
                    completer = MyCompleter(['add', 'add content', 'edit tag','edit content', 'remove tag',
                                            'remove note', 'find by content', 'find by tag', 'sort by tag',
                                            'show all','all','help','back','main menu', 'exit'])
                    
                    try:
                        input_data = prompt("Enter command: ",
                                    completer=completer,
                                    history=history,
                                    complete_while_typing=True)
                        input_data.lower()
                        if input_data == "exit":
                            note.save_pickle(filename_note_book)
                            PROGRAM_STATUS = False
                            break
                        elif input_data == 'main menu' or input_data == 'back':
                            print(f"{YELLOW} You have returned to the main menu.")
                            note.save_pickle(filename_note_book)
                            break
                        elif input_data == 'help':
                            help_record_note()
                        elif input_data == 'add content':
                            # Создание новой заметки и добавление её в NoteBook
                            new_tag = input(f"{GREEN}Enter tags: {RESET}")
                            new_content = str(input(f"{GREEN}Enter content: {RESET}"))
                            note.add_note(src.notes.Note(new_content, [new_tag]))
                            note.save_pickle(filename_note_book)
                        elif input_data == 'edit tag':
                            # Код для редактирования тегов заметки
                            tag_to_edit = input(f"{GREEN}Enter the tag to search for: {RESET}")
                            new_tag = input(f"{GREEN}Enter new teg: {RESET}")
                            note.edit_tag_by_old_value(tag_to_edit, new_tag)
                            note.save_pickle(filename_note_book)
                            print(f"{YELLOW}Post tag changed to '{new_tag}'{RESET}")
                        elif input_data == 'edit content':
                            # Код для редактирования содержимого заметки
                            input_tag = input(f"{GREEN}Enter the tag to search for: {RESET}")
                            input_new_content = input(f"{GREEN}Enter new content: {RESET}")
                            note.edit_content_by_tag(input_tag, input_new_content)
                            note.save_pickle(filename_note_book)
                            print(f"{YELLOW}content changed successfully{RESET}")
                        elif input_data == 'remove tag':
                            # Код для удаления тегов заметки
                            delete_teg = input(f"{GREEN}Enter name tag dor delete: {RESET}")
                            found_notes = note.find_by_tag(delete_teg)
                            if found_notes:
                                note.edit_tag_by_old_value(delete_teg, [])
                                note.save_pickle(filename_note_book)
                                print(f"{YELLOW}You delete tag '{delete_teg}'{RESET}")
                            else:
                                print(f"{RED} No such tag")
                        elif input_data == 'remove note':
                            # Код для удаления заметки
                            delete_id = input(f"{GREEN}Enter ID notes: {RESET}")
                            if delete_id in note.data:
                                note.remove_note(note.data[delete_id])
                                note.save_pickle(filename_note_book)
                                print(f"{YELLOW}Note with ID {delete_id} deleted.{RESET}")
                            else:
                                print(f"{RED} No such ID")
                        elif input_data == 'find by content':
                            # Код для поиска заметок по содержимому
                            find_by_content = input(f"{GREEN}Enter the words that are in the text: {RESET}")
                            found_notes = note.find_by_content(find_by_content)
                            print(f"{YELLOW}{found_notes}")
                        elif input_data == 'find by tag':
                            # Код для поиска заметок по тегам
                            find_by_tag = input(f"{GREEN}Enter the tag: {RESET}")
                            found_notes = note.find_by_tag(find_by_tag)
                            print(f"{YELLOW}{found_notes}")
                        elif input_data == 'sort by tag':
                            # Код для сортировки заметок по тегам
                            sorted_notes_contents = note.sort_by_tag()
                            # for content in sorted_notes_contents:
                            print(f"{YELLOW}{sorted_notes_contents}")
                        elif input_data == 'show all' or input_data == 'all':
                            # Код для отображения всех заметок
                            print(note.show_all())
                        else:
                            print(
                                f'{RED}Command "{input_data}" not found. The following command will "help" you know what the commands are.')
                    except:
                        print('Something went wrong, restart the program')
            
            elif data == "help":
                help_info()

            elif data == "exit":
                book.save_to_file(filename_address_book)
                note.save_pickle(filename_note_book)
                PROGRAM_STATUS = False

            else:
                print(f"{RED}Command not found. The following command will 'help' you know what the commands are.{RESET}")
        except KeyboardInterrupt:
            # Обработка прерывания пользователем (Ctrl+C и т. д.)
            continue

if __name__ == "__main__":
    start_bot()

    