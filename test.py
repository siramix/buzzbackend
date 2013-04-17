import gdata.spreadsheet.service
import gdata.service
#import getpass
import string


def _PrintFeed(feed):
    for i, entry in enumerate(feed.entry):
        if isinstance(feed, gdata.spreadsheet.SpreadsheetsCellsFeed):
            print i
            print entry
            print '%s %s\n' % (entry.title.text, entry.content.text)
        elif isinstance(feed, gdata.spreadsheet.SpreadsheetsListFeed):
            print '%s %s %s' % (i, entry.title.text, entry.content.text)
            # Print this row's value for each column (the custom dictionary is
            # built using the gsx: elements in the entry.)
            print 'Contents:'
            for key in entry.custom:
                print '  %s: %s' % (key, entry.custom[key].text)
            print '\n',
        else:
            print '%s %s\n' % (i, entry.title.text)


def login_to_spreadsheet():
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.email = raw_input('Email: ')
    client.password = getpass.getpass('Password: ')
    client.source = "BuzzBackend"
    client.ProgrammaticLogin()
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
    return max([int(entry.content.text) for entry in cell_feed.entry])+1


def ship_pack(name):
    client = login_to_spreadsheet()
    spreadsheet_key = '0Ar6_A4FPzJBPdFlZTEN5REJJYVMtejI1RGkwYW1FX2c'
    wksht_id = get_worksheet_id(client, 0)
    query = gdata.spreadsheet.service.CellQuery()
    query.min_col = '2'
    query.max_col = '11'
    query.min_row = '2'
    cell_feed = client.GetCellsFeed(spreadsheet_key, wksht_id, query=query)
    included_cells = list()
    count = 0
    for entry in cell_feed.entry:
        if count == 9:
            break
        print '%d : %s' % (count, entry.content.text)
        count += 1


def ship_pack_ui():
    packs = get_packs()
    pack_dictionary = dict(packs)
    print('Which pack would you like to ship?')
    for index, pack in packs:
        print('  %s: %s' % (index, pack))
    ship_index = raw_input('Which pack would you like to ship? ')
    ship_name = pack_dictionary[ship_index]
    ship_pack(ship_name)

def main():
    client = gdata.spreadsheet.service.SpreadsheetsService()
    client.email = raw_input('Email: ')
    client.password = getpass.getpass('Password: ')
    client.source = "BuzzBackend"
    client.ProgrammaticLogin()
    spreadsheet_key = '0Ar6_A4FPzJBPdFlZTEN5REJJYVMtejI1RGkwYW1FX2c'
    ws_feed = client.GetWorksheetsFeed(spreadsheet_key)
    wksht_id_parts = ws_feed.entry[string.atoi('0')].id.text.split('/')
    wksht_id = wksht_id_parts[len(wksht_id_parts) - 1]
    _PrintFeed(ws_feed)
    #list_feed = client.GetListFeed(spreadsheet_key, wksht_id)
    #_PrintFeed(list_feed)
    #print(len(list_feed.entry))
    query = gdata.spreadsheet.service.CellQuery()
    query.min_col = '2'
    query.max_col = '2'
    cell_feed = client.GetCellsFeed(spreadsheet_key, wksht_id, query=query)
    for i, entry in enumerate(cell_feed.entry):
        print '%s %s\n' % (entry.title.text, entry.content.text)

if __name__ == '__main__':
    print determine_start_id()
    print ship_pack_ui()
