from collections import UserDict
from datetime import datetime
import uuid
import re
import pickle
import os
from abc import ABC, abstractmethod


class FieldAbstract(ABC):
    pass

class NoteAbstract(ABC):
    @abstractmethod
    def edit_content(self, new_content) -> None:
        pass

    @abstractmethod
    def remove_content(self) -> None:
        pass

    @abstractmethod
    def add_tag(self, new_tag) -> None:
        pass

    @abstractmethod
    def edit_tag(self, new_tag) -> None:
        pass

    @abstractmethod
    def remove_tag(self) -> None:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

class NoteBookAbstract(ABC):
    @abstractmethod
    def add_note(self, note) -> None:
        pass

    @abstractmethod
    def find_by_content(self, search_content) -> NoteAbstract:
        pass

    @abstractmethod
    def find_by_tag(self, search_tag) -> NoteAbstract:
        pass

    @abstractmethod
    def edit_content_by_tag(self, search_tag, new_content) -> None:
        pass

    @abstractmethod
    def edit_tag_by_old_value(self, old_tag, new_tag) -> None:
        pass

    @abstractmethod
    def remove_note(self, note_it_to_del) -> None:
        pass

    @abstractmethod
    def sort_by_tag(self) -> NoteAbstract:
        pass

    @abstractmethod
    def show_all(self) -> NoteAbstract:
        pass

    @abstractmethod
    def save_pickle(self, filename) -> None:
        pass

    @abstractmethod
    def load_pickle(filename) -> None:
        pass

class Field(FieldAbstract):
    mandatory = False

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Content(Field):

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Tag(Field):

    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Note(NoteAbstract):

    def __init__(self, content, tags=[]):
        self.id = str(uuid.uuid4())[:5]
        self.content = Content(content)
        if tags:
            self.tag = [Tag(tag) for tag in tags]
        else:
            self.tag = []
        self.creationdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def edit_content(self, new_content) -> None:
        self.content.value = new_content
        tags_found = re.findall(r'#\s*([\w-]+\d*)', self.content.value)
        tags_found = [Tag(tag) for tag in tags_found]  # перетворюємо знайдені рядки на об'єкти Tag
        if tags_found:
            self.tag.extend(tags_found)

    def remove_content(self) -> None:
        self.content.value = 'Content <<<<Сlassified>>>>'  # Замість видалення помічажмо матеріл Засекречено =)

    def add_tag(self, new_tag) -> None:
        self.tag.append(Tag(new_tag))

    def edit_tag(self, new_tag) -> None:
        self.tag = [Tag(new_tag)]

    def remove_tag(self) -> None:
        self.tag = []

    def __str__(self):
        return f'Content: {self.content.value}, Note ID: {self.id}, Date Created: {self.creationdate}, Tags: {[tag.value for tag in self.tag]}'

    def __repr__(self):
        return f'Content: {self.content.value}, Note ID: {self.id}, Date Created: {self.creationdate}, Tags: {[tag.value for tag in self.tag]}'


class NoteBook(UserDict, NoteBookAbstract):

    def add_note(self, note) -> None:
        self.data[note.id] = note

    def find_by_content(self, search_content):
        found = []
        search_content = search_content.lower()
        for note in self.data:
            if search_content in self.data[note].content.value.lower():
                found.append(self.data[note])
        result = '\n'.join(str(line) for line in self.data.values())

        return f'Found notes by content:\n{result}'

    def find_by_tag(self, search_tag):
        found = []
        search_tag = search_tag.lower()
        for note in self.data:
            for tag in self.data[note].tag:
                if search_tag == tag.value.lower():
                    found.append(self.data[note])  # для тестування замінити ці коментарі в цих 2 рядках місцями)

        result = '\n'.join(str(line) for line in self.data.values())

        return f'Found by tag:\n{result}'

    def edit_content_by_tag(self, search_tag, new_content):
        search_tag = search_tag.lower()
        for note in self.data.values():
            for tag in note.tag:
                if search_tag == tag.value.lower():
                    note.edit_content(new_content)
                    return f'Content edited for note with tag {search_tag}'
        return f'No note found with tag {search_tag}'

    def edit_tag_by_old_value(self, old_tag, new_tag):
        count_changed = 0
        for note in self.data.values():
            for tag in note.tag:
                if tag.value == old_tag:
                    tag.value = new_tag
                    count_changed += 1
        if count_changed > 0:
            return f"{count_changed} tag(s) '{old_tag}' successfully changed to '{new_tag}'."
        else:
            return f"No tag '{old_tag}' found in any note."

    def remove_note(self, note_it_to_del) -> None:
        if note_it_to_del.id in self.data:
            del self.data[note_it_to_del.id]
            print(f'Note {Note(note_it_to_del).id} deleted')

    def sort_by_tag(self):
        # сортуємо по тегу. При цьому, якщо в списку декілька тегів, то в кожному списку береться "1й" по алфавіту
        # і сортується по цим "1м" значенням
        sorted_notes_by_tags = sorted(self.data.items(), key=lambda x: min(tag.value.lower() for tag in x[1].tag))
        sorted_notes_by_tags = [note for id, note in sorted_notes_by_tags]  # залишаємо об'єкти Note

        result = '\n'.join(str(note) for note in sorted_notes_by_tags)

        return f'Sorted notes by TAG:\n{result}'

    def show_all(self) -> {Note}:
        result = '\n'.join(str(value) for value in self.data.values())
        return f'All Notes:\n{result}'

    def save_pickle(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_pickle(filename):
        with open(filename, 'rb') as file:
            deserialized = pickle.load(file)
        return deserialized



