#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# Library:   buzzbackend
#
# Copyright 2013 Siramix Labs
#
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 ( the "License" );
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

import ConfigParser
import os.path
import getpass
import db
import aws


def get_config():
    """Read the config object from the user home directory."""
    home_dir = os.path.expanduser('~')
    config_path = os.path.join(home_dir, '.buzzbackconfig')
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    if not config.has_section('Credentials'):
        config.add_section('Credentials')
    return (config, config_path)


def get_credentials(refresh=False):
    """Get the user credentials from the keyboard or config file."""

    # Get the config object and its path
    config, config_path = get_config()

    # Get email
    if config.has_option('Credentials', 'email') and not refresh:
        email = config.get('Credentials', 'email')
    else:
        email = raw_input('Email: ')
    config.set('Credentials', 'email', email)

    # Get password
    if config.has_option('Credentials', 'password') and not refresh:
        password = config.get('Credentials', 'password')
    else:
        password = getpass.getpass('Password: ')
    config.set('Credentials', 'password', password)

    # Save configuration to disk
    with open(config_path, 'w') as config_file:
        config.write(config_file)

    return (email, password)


def ship_pack_ui(database):
    """Display the UI for shipping a given pack."""
    packs = database.get_packs()
    pack_dictionary = dict(packs)
    print('Which pack would you like to ship?')
    for index, pack in packs:
        print('  %s: %s' % (index, pack))
    ship_index = raw_input('Which pack would you like to ship?\n')
    ship_name = pack_dictionary[ship_index]
    print ('\nPlease review the card data printed below...\n')
    card_data = database.get_pack(ship_name)
    print (card_data)
    filename = raw_input('What is the filename for this pack (ex. buzzwords_i)?\n')
    aws.upload_pack(ship_name, filename, card_data)


def login_to_database():
    """Login to the database and return the db object."""
    spreadsheet_key = '0AlafstGFd0zJdFNxMGdseWdCVHNDWGpCY2NZeTktQXc'

    # Login. Loop until it works.
    email, password = get_credentials()
    database = db.WordDatabase(email, password, spreadsheet_key)
    login_state = database.login_to_spreadsheet()
    while not login_state:
        print('Incorrect Credentials. Please Try Again!')
        email, password = get_credentials(True)
        database = db.WordDatabase(email, password, spreadsheet_key)
        login_state = database.login_to_spreadsheet()

    return database


def main():
    database = login_to_database()
    ship_pack_ui(database)
    print('\nPack data has been shipped. Review it in AWS.')


if __name__ == '__main__':
    main()
