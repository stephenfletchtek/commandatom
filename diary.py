#!/usr/bin/env python3

from collections import OrderedDict
import datetime
import os
import sys

from peewee import *

db = SqliteDatabase('diary.db')


class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

def initialise():
    """Create the database and table if they don't exist."""
    db.connect()
    db.create_tables([Entry],safe=True)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_loop():
    """Show the menu"""
    choice = None

    while choice !='q':
        clear()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            clear()
            menu[choice]()


def add_entry():
    """Add an entry."""
    print('Make your entry and press ctrl+d when finished.')
    data = sys.stdin.read().strip()

    if data:
        if input('Save entry? [Y/n]   ').lower != 'n':
            Entry.create(content=data)
            print('Entry saved!')

def view_entries(search_query=None):
    """View previous entries."""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %d %B, %Y %H:%M')
        clear()
        print(timestamp)
        print('='*len(timestamp))
        print(entry.content)
        print('\n\n'+'='*len(timestamp))
        print('N) Next entry')
        print('d) delete entry')
        print('q quit back to main menu')

        next_action = input('Action [N/d/q]   ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)

def search_entries():
    """Search entries."""
    view_entries(input('Search query: '))


def delete_entry(entry):
    """Delete an entry."""
    if input('Are you sure? [y/N]   ').lower().strip() == 'y':
        entry.delete_instance()
        print('Entry deleted')


menu = OrderedDict([
        ('a', add_entry),
        ('v', view_entries),
        ('s', search_entries)
])

if __name__ == '__main__':
    initialise()
    menu_loop()
