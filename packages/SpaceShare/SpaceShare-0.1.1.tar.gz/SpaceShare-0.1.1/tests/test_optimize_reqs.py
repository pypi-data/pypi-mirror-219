from SpaceShare import optimize_rideshares as opt
from SpaceShare.reader import clean_dataframe
import pandas as pd
import numpy as np

def test_columns(sheet_name = "spaceshare_example_sheet.csv"):
    df = clean_dataframe(pd.read_csv(sheet_name))
    for kind in ["arrival","departure"]:
        opt.optimize(df,kind)
    assert "arrival_group" in df.columns, "arrival_group column not found"
    assert "departure_group" in df.columns, "departure_group column not found"

def test_group_limits(sheet_name = "spaceshare_example_sheet.csv"):
    df = clean_dataframe(pd.read_csv(sheet_name))
    for kind in ["arrival","departure"]:
        opt.optimize(df,kind)
        groups = np.unique(df[kind+"_group"])
        for group in groups:
            assert len(df[df[kind+"_group"]==group]) <= 3, "Group size exceeded 3"
            if(kind == "arrival"):
                times = df[df[kind+"_group"]==group]["date_time_of_airport_arrival"]
            else:
                times = df[df[kind+"_group"]==group]["date_time_of_hotel_departure"]
            for i in range(len(times)):
                for j in range(i,len(times)):
                    assert pd.Timedelta(times.iloc[i]-times.iloc[j]).total_seconds()/3600 <= 0.5, "Time difference exceeded 0.5 hours"
    
    
test_columns()
test_group_limits()