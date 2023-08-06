from SpaceShare.reader import read_google_sheet

df = read_google_sheet("1M6akYJ46z-qMZ_DDHyJvXr2U4rlqvZ8epe6PCa5tpHQ")

default_keys = ['Name', 'Email', 'date_time_of_hotel_departure',
                    'date_time_of_airport_arrival', 'Gender', 'Gender_to_share_room_with',
                    'Phone_number']

#confirm expected number of columns
assert len(df.keys()) == 7,f'extra, possibly empty columns exist in the google sheet'

#assert that keys are in expected default 
for k in df.keys():
    assert k in default_keys,f' "{k}" is not a column expected from the google sheet. Expected columns are {default_keys}'

