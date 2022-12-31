# import musicbrainzngs
import musicbrainzngs
import pandas as pd
import json
import time

musicbrainzngs.set_useragent("UdacityDSChallenge", "0.1", "tugberkcapraz@gmail.com")

# partition a list into chunks of size n
def partition(lst, n):
    '''This function takes a list and a number n and returns a list of lists
    where each list is of size n
    
    param lst: a list
    param n: an integer
    return: a list of lists
    
    Rationale:
    This function is used to partition the list of artists into chunks of 25.
    This is because the MusicBrainz API only allows 25 artists per call.
    In order to get the artist info for all the artists, we need to make multiple calls.
    This partitioning function is useful and necessary for that purpose.
    '''
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


# get the artists from the json file
def get_artists_from_json(json_file):
    '''This function takes a json file and returns a list of artists from the json file
    param json_file: a json file
    return: a list of artists
    
    Rationale:
    This function is used to get the artists from the json file.
    It reads the json file line by line and appends the artist to a list.
    Then it removes the duplicates and partitions the list into chunks of 25 
    by using the partition function.

    '''
    # initialize an empty list
    artists = []
    # open the json file and read it line by line
    with open(json_file) as f:
        for line in f:
            try:
                artists.append(json.loads(line)['artist'])
            except:
                pass
    # remove duplicates
    artists = list(set(artists))
    # partition the list into chunks of 25
    partitioned_artists = list(partition(artists, 25))

    return partitioned_artists


def get_artist_info(artists):
    '''This function takes a list of artists and 
    returns a dataframe of artist information from MusicBrainz
    
    param artists: a list of artists
    return: a dataframe of artist information
    
    Rationale:
    This function is used to get the artist information from MusicBrainz.
    It uses the musicbrainzngs package to get the artist information.
    It then converts the artist information to a dataframe and returns it.
    
    The genres are, I believe, are decisive features for churn.'''

    # set the user agent
    musicbrainzngs.set_useragent("UdacityDSNDChallenge", "0.1", "tugberkcapraz@gmail.com")
    # get the artist info
    artist_info = musicbrainzngs.search_artists(query=artists)
    # convert the artist info to a dataframe
    artist_info_df = pd.DataFrame(artist_info['artist-list'])
    # lowercase the artist names
    artist_info_df['name'] = artist_info_df['name'].str.lower()
    #lowercase the artists list
    artists = [artist.lower() for artist in artists]
    # filter the dataframe to only include the artists in the artists list
    final_df = artist_info_df[artist_info_df['name'].isin(artists)]
    
    return final_df

# start timer
start_time = time.time()

# read in the json file
artists = get_artists_from_json('./data/mini_sparkify_event_data.json')
print("read in the json file. Proceeding with the API call.")

# for testing purposes, we will use 250 artists
#artists = artists[:10]
#print("for testing purposes, we are using 250 artists")

# loop over the nested list of artists and get the artist info.
artist_info = pd.DataFrame()
for artist in artists:
    # append the artist info to the dataframe using concat
    artist_info = pd.concat([artist_info, get_artist_info(artist)], axis=0)
print("looped over the nested list of artists and got the artist info.")

# write the artist info to a csv file
artist_info.to_csv('./data/artist_info_sample.csv', index=False)
print("wrote the artist info to a csv file")

# end timer
end_time = time.time()
print("time elapsed: ", end_time - start_time)
