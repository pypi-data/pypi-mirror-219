import pandas as pd


def read_google_sheet(sheet_id):
    """
    Reads in a Google Sheet as a CSV file using pandas. 
    Ensure that the sharing setting for the sheet allows anyone with the link to access it.

    Args:
        sheet_id (str, optional): The ID of the Google Sheet, extracted from the webpage as '/d/{sheet_id}/gviz/tq?tqx=out:csv'. 
            If None, it uses a default ID. Defaults to None.

    Returns:
        pandas.DataFrame: A DataFrame containing the information from the Google Sheet. The "Timestamp" 
            column is removed, and "date_time_of_airport_arrival" and "date_time_of_hotel_departure" 
            columns are converted into datetime objects.

    Raises:
        pandas.errors.ParserError: If parsing the CSV file fails.
        urllib.error.HTTPError: If the sheet ID is invalid, or the sheet doesn't allow public access.

    Note:
        The default sheet ID used when none is provided is '1riOck-CL8RjVkt_dgcgWhd0DWhUWMifpyb6VLngTrHs'.
    """
    prefix = "https://docs.google.com/spreadsheets/d/"
    
    DF = pd.read_csv(prefix+ sheet_id+ "/gviz/tq?tqx=out:csv")
    return clean_dataframe(DF)

def clean_dataframe(DF):
    """
    Cleans the input DataFrame by dropping the 'Timestamp' column and converting the 'date_time_of_airport_arrival'
    and 'date_time_of_hotel_departure' columns from strings to datetime objects.

    Args:
        DF (pandas.DataFrame): The DataFrame to clean.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
    DF = DF.drop(columns= "Timestamp")

    #convert day-time string into date_time object
    DF["date_time_of_airport_arrival"]  = [pd.to_datetime(tt) for tt in DF["date_time_of_airport_arrival"] ]
    DF["date_time_of_hotel_departure"]  = [pd.to_datetime(tt) for tt in DF["date_time_of_hotel_departure"] ]

    return DF
