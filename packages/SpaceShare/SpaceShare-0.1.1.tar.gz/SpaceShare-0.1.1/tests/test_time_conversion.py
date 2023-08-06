from SpaceShare.optimize_rideshares import get_time_of_year
import pandas as pd
import pytest

def test_get_time_of_year():
    """
    This function tests that the get_time_of_year function correctly converts the datetimes into hour values. 
    """

    # generate a pandas datetime object to test on 
    time = pd.to_datetime('2023-07-13 15:28:00.00',format='%Y-%m-%d %H:%M:%S.%f')
 
    #calculate the number of seconds of the year to the given date using the function
    func_time = get_time_of_year(time)

    # hard coded check value 
    check_time = 4671.466666666666

    # assert correctness to within a minute
    assert check_time == pytest.approx(func_time, abs = 1.0/3600)

    ## Check new years eve 
    time = pd.to_datetime('2013-12-31 23:30:05.00', format = '%Y-%m-%d %H:%M:%S.%f')
    func_time = get_time_of_year(time)
    check_time = 365*24 + 23 + 30/60 + 5/3600.

    assert check_time == pytest.approx(func_time, abs = 1.0/3600)

