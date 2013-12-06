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
import json

class WordDatabase(object):
    """Class for connecting to the word database."""

    def __init__(self, email, password, spreadsheet_key):
        """Create an instance of the word database."""
        super(WordDatabase, self).__init__()
        self.spreadsheet_key = spreadsheet_key
        self.email = email
        self.password = password
        self.client = None

    def login_to_spreadsheet(self):
        """Login to the spreadsheet using the stored credentials."""
        if self.client is None:
            self.client = gdata.spreadsheet.service.SpreadsheetsService()

        # Catch the error and turn it boolean
        try:
            self.client.ClientLogin(self.email, self.password)
            ret = True
        except gdata.service.BadAuthentication:
            ret = False
        finally:
            return ret

    def get_worksheet_id(self, worksheet_id):
        """Get the unique id of a the worksheet by index."""
        ws_feed = self.client.GetWorksheetsFeed(self.spreadsheet_key)
        wksht_id_parts = ws_feed.entry[worksheet_id].id.text.split('/')
        return wksht_id_parts[len(wksht_id_parts) - 1]

    def get_packs(self):
        """Get a tuple consisting of pack ids and names."""
        wksht_id = self.get_worksheet_id(1)
        query = gdata.spreadsheet.service.CellQuery()
        query.min_col = '1'
        query.max_col = '2'
        query.min_row = '4'
        cell_feed = self.client.GetCellsFeed(self.spreadsheet_key,
                                             wksht_id,
                                             query=query)
        data = [entry.content.text for entry in cell_feed.entry]
        return zip(data[0::2], data[1::2])

    def determine_start_id(self):
        """Get the next unique ID in sequence."""
        wksht_id = self.get_worksheet_id(0)
        query = gdata.spreadsheet.service.CellQuery()
        query.min_col = '1'
        query.max_col = '1'
        query.min_row = '2'
        cell_feed = self.client.GetCellsFeed(self.spreadsheet_key,
                                             wksht_id,
                                             query=query)

        # Determine the max id and add one to it
        start_id = max([int(entry.content.text) for entry in cell_feed.entry])
        start_id += 1

        return start_id

    def format_cardstring(self, cards):
        """Format the list of cards into a string ready for app consumption"""
        cardString = ''
        # Add new lines between each, instead of commas
        for card in cards:
            cardString += str(card) + '\n'
        cardString.rstrip()
        # Replace ' with " if it's one of the keys
        cardString = cardString.replace("{'", '{"')
        cardString = cardString.replace("'}", '"}')
        cardString = cardString.replace("': ", '": ')
        cardString = cardString.replace(": '", ': "')
        cardString = cardString.replace("', ", '", ')
        cardString = cardString.replace(", '", ', "')
        # Replace #s for TMs
        cardString = cardString.replace('#', '™')
        return cardString

    def get_pack(self, name):
        """Output the designated pack."""
        wksht_id = self.get_worksheet_id(0)
        query = gdata.spreadsheet.service.CellQuery()
        query.min_col = '2'
        query.max_col = '2'
        query.min_row = '2'
        cell_feed = self.client.GetCellsFeed(self.spreadsheet_key,
                                             wksht_id,
                                             query=query)
        cell_rows = set()
        for entry in cell_feed.entry:
            if entry.content.text == name:
                cell_rows.add(int(entry.cell.row))
        query.min_row = str(min(cell_rows))
        query.max_row = str(max(cell_rows))
        query.min_col = '1'
        query.max_col = '10'
        cell_feed = self.client.GetCellsFeed(self.spreadsheet_key,
                                             wksht_id,
                                             query=query)
        count = 1
        cards = list()
        cur_card = dict()
        bad_words = list()
        for entry in cell_feed.entry:
            if count % 10 == 0:
                cur_card['badwords'] = ",".join(bad_words).upper()
                if entry.content.text == 'Final' or entry.content.text == 'Shipped':
                    cards.append(cur_card)
                else:
                    print('Warning: "{0}" is not ready'.format(cur_card['title']))
                cur_card = dict()
                bad_words = list()
            elif count % 10 == 1:
                cur_card['_id'] = entry.content.text.strip()
            elif count % 10 == 3:
                cur_card['title'] = entry.content.text.strip().title()
            elif count % 10 >= 4 and count % 10 <= 8:
                bad_words.append(entry.content.text.strip())
            count += 1
        formatted_cards = self.format_cardstring(cards)
        return formatted_cards
