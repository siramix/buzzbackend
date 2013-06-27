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
import gdata.spreadsheet.service
import gdata.service
import getpass
import ConfigParser
import os.path


class WordDatabase(object):
    """Class for connecting to the word database."""

    def __init__(self):
        super(WordDatabase, self).__init__()
        self.spreadsheet_key = '0Ar6_A4FPzJBPdFlZTEN5REJJYVMtejI1RGkwYW1FX2c'
        home_dir = os.path.expanduser('~')
        self.config_path = os.path.join(home_dir, '.buzzbackconfig')
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_path)
        if not self.config.has_section('Credentials'):
            self.config.add_section('Credentials')

    def login_to_spreadsheet(self):

        if self.config.has_option('Credentials', 'email'):
            email = self.config.get('Credentials', 'email')
        else:
            email = raw_input('Email: ')
        self.config.set('Credentials', 'email', email)

        client = gdata.spreadsheet.service.SpreadsheetsService()

        if self.config.has_option('Credentials', 'password'):
            password = self.config.get('Credentials', 'password')
        else:
            password = getpass.getpass('Password: ')
        self.config.set('Credentials', 'password', password)

        client.ClientLogin(email, password)

        with open(self.config_path, 'w') as config_file:
            self.config.write(config_file)

        return client


def login_to_spreadsheet():
    client = gdata.spreadsheet.service.SpreadsheetsService()
    email = raw_input('Email: ')
    #password = getpass.getpass('Password: ')

    client.ClientLogin(email, password)
    return client


def get_worksheet_id(client, worksheet_id):
    spreadsheet_key = '0Ar6_A4FPzJBPdFlZTEN5REJJYVMtejI1RGkwYW1FX2c'
    ws_feed = client.GetWorksheetsFeed(spreadsheet_key)
    wksht_id_parts = ws_feed.entry[worksheet_id].id.text.split('/')
    return wksht_id_parts[len(wksht_id_parts) - 1]


def get_packs():
    client = login_to_spreadsheet()
    spreadsheet_key = '0Ar6_A4FPzJBPdFlZTEN5REJJYVMtejI1RGkwYW1FX2c'
    wksht_id = get_worksheet_id(client, 1)
    query = gdata.spreadsheet.service.CellQuery()
    query.min_col = '1'
    query.max_col = '2'
    query.min_row = '4'
    cell_feed = client.GetCellsFeed(spreadsheet_key, wksht_id, query=query)
    data = [entry.content.text for entry in cell_feed.entry]
    return zip(data[0::2], data[1::2])


def determine_start_id():
    client = login_to_spreadsheet()
    spreadsheet_key = '0Ar6_A4FPzJBPdFlZTEN5REJJYVMtejI1RGkwYW1FX2c'
    wksht_id = get_worksheet_id(client, 0)
    query = gdata.spreadsheet.service.CellQuery()
    query.min_col = '1'
    query.max_col = '1'
    query.min_row = '2'
    cell_feed = client.GetCellsFeed(spreadsheet_key, wksht_id, query=query)

    # Determine the max id and add one to it
    start_id = max([int(entry.content.text) for entry in cell_feed.entry]) + 1

    return start_id


def ship_pack(name):
    client = login_to_spreadsheet()
    spreadsheet_key = '0Ar6_A4FPzJBPdFlZTEN5REJJYVMtejI1RGkwYW1FX2c'
    wksht_id = get_worksheet_id(client, 0)
    query = gdata.spreadsheet.service.CellQuery()
    query.min_col = '2'
    query.max_col = '2'
    query.min_row = '2'
    cell_feed = client.GetCellsFeed(spreadsheet_key, wksht_id, query=query)
    cell_rows = set()
    for entry in cell_feed.entry:
        if entry.content.text == name:
            cell_rows.add(int(entry.cell.row))
    query.min_row = str(min(cell_rows))
    query.max_row = str(max(cell_rows))
    query.min_col = '1'
    query.max_col = '10'
    cell_feed = client.GetCellsFeed(spreadsheet_key, wksht_id, query=query)
    count = 1
    cards = list()
    cur_card = dict()
    bad_words = list()
    for entry in cell_feed.entry:
        if count % 10 == 0:
            cur_card['badwords'] = ",".join(bad_words)
            if entry.content.text == 'Final' or entry.content.text == 'Shipped':
                cards.append(cur_card)
            else:
                print('Warning: "{0}" is not ready'.format(cur_card['title']))
            cur_card = dict()
            bad_words = list()
        elif count % 10 == 1:
            cur_card['_id'] = entry.content.text
        elif count % 10 == 3:
            cur_card['title'] = entry.content.text
        elif count % 10 >= 4 and count % 10 <= 8:
            bad_words.append(entry.content.text)
        count += 1
    return cards


def ship_pack_ui():
    packs = get_packs()
    pack_dictionary = dict(packs)
    print('Which pack would you like to ship?')
    for index, pack in packs:
        print('  %s: %s' % (index, pack))
    ship_index = raw_input('Which pack would you like to ship? ')
    ship_name = pack_dictionary[ship_index]
    return ship_pack(ship_name)


if __name__ == '__main__':
    #print determine_start_id()
    #print ship_pack_ui()
    x = WordDatabase()
    x.login_to_spreadsheet()
