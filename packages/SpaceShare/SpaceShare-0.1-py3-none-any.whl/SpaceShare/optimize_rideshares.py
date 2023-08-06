import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from datetime import timedelta

def get_time_of_year(time):
    """
    Calculates the time as a float in hours, given a datetime object.

    Args:
        time (datetime): The datetime object to be converted.

    Returns:
        float: The time in hours, represented as a float.

    Note:
        This function assumes that the input datetime object has attributes 
        for day, hour, minute, and second. The output is not an exact month 
        representation, it's a representation of time in hours converted to 
        an approximate month scale.

    Raises:
        AttributeError: If the input datetime object doesn't have day, hour, minute, 
        and second attributes.
    """
    return timedelta(days=time.day, hours=time.hour, minutes=time.minute, seconds=time.second).total_seconds()/3600


def optimize(df, kind="arrival", max_time_difference = 0.5, max_people_per_car = 3): 
    """ 
    Optimizes shared rides for participants based on airport arrival or departures times using a hierarchical clustering algorithm. 

    Args:
        df (pandas.DataFrame): Input DataFrame which needs to be processed.
        kind (str, optional): Specifies the column to consider for optimization. 
            Must be either 'arrival' or 'departure'. Defaults to 'arrival'.
        max_time_difference (float, optional): The maximum difference in departure time between participants
            for grouping in the hierarchical clustering. Defaults to 0.5.
        max_people_per_car (int, optional): The maximum number of people that can 
            be grouped in a car. Defaults to 3.

    Returns:
        pandas.DataFrame: DataFrame with a new column indicating the ride groups.

    Raises:
        AssertionError: If the kind parameter is not 'arrival' or 'departure'.
        
    Note: 
        'arrival' and 'departure' refers to the "date_time_of_airport_arrival" 
        and "date_time_of_hotel_departure" columns of the DataFrame respectively.
    """

    assert kind in ["arrival", "departure"], "kind must be either 'arrival' or 'departure'"
    if(kind=="arrival"):
        times = df["date_time_of_airport_arrival"].apply(get_time_of_year)
    else:
        times = df["date_time_of_hotel_departure"].apply(get_time_of_year)

    # Reshape the data to the format needed for the linkage function
    data = np.array(times).reshape(-1, 1)

    # Create a dendrogram using the 'ward' method to minimize variance in each cluster
    Z = linkage(data, 'ward')

    # Set a maximum time difference (let's say 15 minutes) for each group
    clusters = fcluster(Z, max_time_difference, criterion='distance')

    counts = np.bincount(clusters)

    too_many_people = np.where(counts > max_people_per_car)[0]

    for idx in too_many_people:
        # Find the people in the cluster
        people = np.where(clusters == idx)[0]
        # Sort the people by their time
        people = people[np.argsort(times[people])]
        # Split the people into groups of 3
        new_clusters = np.array_split(people, len(people) // 3 + 1)
        for cluster_idx,new_cluster in enumerate(new_clusters[1:]):
            # Update the clusters
            clusters[new_cluster] = clusters.max() + 1
    df[f"{kind}_group"] = clusters
    return df

