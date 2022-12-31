# import libraries
import pandas as pd
from ast import literal_eval


# function the cells above
def get_genres(df):
    # drop nans from tag-list column
    df = df.dropna(subset=['tag-list'])
    df['tag-list'] = df['tag-list'].apply(literal_eval) #convert to list type
    df.reset_index(inplace=True)
    df = df.explode('tag-list')
    off = df[['name', 'tag-list']].rename(columns={'name':'artist_name'})
    off.set_index("artist_name", inplace=True)
    final = pd.json_normalize(off["tag-list"]).set_index(off.index)
    final = final.reset_index().rename(columns={'name':'genre'})
    # drop missing values
    final = final.dropna()
    # convert the count column to int
    final['count'] = final['count'].astype(int)
    # sort by count and genre.
    final = final.sort_values(by=['count', 'genre'], ascending=False)
    #final.drop(columns=['count'], inplace=True)
    final.reset_index(inplace=True)
    final.drop_duplicates(subset=['artist_name'], inplace=True)
    final.rename(columns={'artist_name':'name'}, inplace=True)
    return final


# read artists_info_sample.csv from data folder
df = pd.read_csv('./data/artist_info_sample.csv')

genres = get_genres(df)

# get dummies for genres
genres_dummies = pd.get_dummies(genres['genre'])
# merge the genres_dummies with the genres dataframe
genres = pd.concat([genres, genres_dummies], axis=1)

df.drop(columns=['id','tag-list', 'sort-name', 'country', 'area',
       'begin-area', 'life-span', 'alias-list', 'tag-list', 'isni-list',
       'disambiguation', 'end-area','ipi-list'], inplace=True)

# merge the genres_pivot dataframe with the df dataframe
merged = df.merge(genres, on='name', how='left')

# fill the missing values of merged[gender] with merged[type]
merged["gender"].fillna(merged["type"], inplace=True)

merged.drop(columns=['type', 'index', 'genre', 'count'], inplace=True)

# get dummies for gender
gender_dummies = pd.get_dummies(merged['gender'])
# merge the gender_dummies with the merged dataframe
merged = pd.concat([merged, gender_dummies], axis=1)

# save the merged dataframe to csv
merged.to_csv('./data/genres.csv', index=False)