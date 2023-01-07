## Overview

This projects aims to predict customer churn with PySpark based on the dataset provided by Udacity. 

The two main goals of this project are as follows:

1) Exploring the relationgship between the variables in the user log and their churning behavior.
   
2) Provide a model that can predict the churning behavior of the users.
   
## Business Understanding

Okay, imagine yourself as a data scientist working for a music streaming company, called Sparkify. The company has a lot of users and they want to know which users are going to churn. So the stakeholders reached you and asked you to build a model that can predict the churning behavior of the users. What you have is the user log data and the churn label.

Sounds easy at first glance but I can assure you that  your first design choice appeared just at exact moment you heard about this new assignment.

The choice you have to make here is whether you are going to try to predict the the timing of the churn behaviour or to predict which users are most likely to churn. If these two sounds same to you, from the business perspective they refer more or less to the same thing, but from a datascientist's perspective they are two different problems.

In first case, you have your log data and you are trying to predict a really minor cases of churning labelled as cancellation confirmation. This means working with millions of rows and building your model on millions of rows. So it's really a big data task.

In the second case, you have your log data but this time you convert your rows to aggregated user level data. This means you have to group your data by user id and then you have user profiles. This translates to your work as you going to work with less of rows and build your model on this smaller dataset. This is still a big data work in one sense because you still need that computational power to make the aggregations but not big data task in the other sense because you are not building a machine learning model on millions of rows.

So my choice was to go for the second path. Because of two reasons:

1) I don't see groundbreaking value in predicting the exact timing of the churn behaviour. I think it's more important to know which users are most likely to churn. So I can take action on them before they churn.
2) It costs less. Because you'll need cloud of your choice to work with your data either case. If you go for the first route, you'll have to spend more time and money on the cloud. If you go for the second route, you'll have to spend money only for the time that you spend on data processing task. So it's cheaper.

So having clarified this, what would be the next step? 

You guessed it right, you have to explore the data!

## Data Understanding

I did it and made a beautiful table for you so that we spend less time here.
The catch it, the label is not given to you. It's stored in the pages column with the 'cancellation_confirmation' value. And you have to work your way to get it first.

 `table here`

As you can see above, the label column does not exist when you first acquired the data. This is user-logs data and the churn behavious is captured in the page column. Page column covers each page visits, and when a user visits the cancellation confirmation page, it means that the user has churned. So you have to work your way to get the label column which we are going to do in a bit.

Another thing to notice here is the unit of observation is events here. What I mean by this is that each row represents an event. So if a user visits certain page n times, you have n rows for that user. Basically a row for each event. I will break this structure and will convert our unit of analysis to user level. This means that I will group the data by user id and will aggregate the data. This will give us a user profile. 

When I looked at those columns, I realized some crucial information are missing. Yes, the artist name and the song name are there. But they are in the text format and they are not telling us anything useful. We can't use them directly as features. One can attempt to code them as categories but it's almost for sure that they'll toss into cardinality issue. So we have to do some feature engineering here and that feature engineering requires an external data source.

For this reason, I started looking for some music API's to receive extra information about artists and/or songs. My three choices were:

1) Spotify API
2) Apple Music API
3) MusicBrainz API

All of them comes with their advantages and disadvantages. Spotify API has the richest features already provided for you. All you have to do is call the API with your request and get the features. They have features like tempo, danceability, energy, valence, etc. But the problem is that bulk requests are not permitted and they have a special section for bulk requests which is not available for individuals. Apple Music API is free but it has limited features. Plus, just like spotify, the bulk requests is not possible. MusicBrainz API is free and it has a lot of features and allows bulk requests. But the problem is that it's not a music streaming API. It's a music database API. So you have to do some extra work to get the features you want.

Since I wanted to tire myself and learn new things on the way, I decided to go with musicbrainz API to get my features. 

A brief attempt to learn MusicBrainz API showed me that it has genres features submitted by the community members. Basically, anyone can recommend a genre for a song or an artist. Also, for the artists, it has country of origin, years of the activity, as well as a type indicator telling that if the artist is a person, choir, group etc.

Another design choice to be made here is that which type of request that is going to be made to the API. You can submit song names to the API and receive info back. Or you can make your search using the artist name. If you submit song names, your list will be much bigger than the artist list. But the problem is that you can't be sure that the song name you have is the same as the song name in the database. The same concern exists for the artist name, however, the there are less unique artist names than the song names. So you'll be submitting a shorter list to the API and your chance of getting a match is higher. For this reason I decided to go with the artist name.

## Data Preparation

So, having established an understanding about the data at hand. Now it's time to implement it. The diagrom below shows the steps that I took to prepare the data and finalize the project. Of course I'll not provide full code here, but for each file in the diagram I'll provide the code for most important parts alongside with the explanation.

`diagram here`

Before explaining the what each script does with example code snippets, I want to mention that I used the following libraries in my project:

`libraries here`


***get_artist_info.py***

Basically this script is where you enter the project. As the diagram above suggests, there are two data sources associated with it. First, mini_sparkify_event_data.json which is the user log data. We'll get our artist names from here. And second, musicbrainz API is where we'll get our features from each artist name.
There are 3 user written function inside this python script. 
partition: Since Musicbrainz API only allows to submit 25 entities in one call, you can't pass your all artist names inside. You have to partition your artist_names list into partitions where each of them consists of 25 song at max.
get_artists_from_json: This function reads the artist names from the json file and saves it as a partitioned list. It calls partition function inside
get_artist_info: The function makes the API call and saves the response in a dataframe. This is where I made my first mistake. I could have written a better function to store my data in a pandas dataframe by taking the nestedness of the json response into account. I didn't do that and I paid the price by having to write another script which covers this nested json issue. The reason I dind't re-write the function here is, I already made the call with this function and received my whole data. So I didn't want to make the same call again which wouldn't be kind to musicbrainz devs.

get_genres.py: This is the script where spent the most time. The reason is that the json response from the API is nested. So I had to write a function to flatten the json response. Basically, I wasn't able to flatten the nested json with pandas because while saving the nested part as a column, it doesn't recognized as a list by python. So I searched for the answer and finally found a solution on stackowerflow where they explained the problem and suggested using literaleval to save that column as a list first. So Basically after applying this solution my pain disappeared. The result of the script is a pandas dataframe where for each artist name has an associated genre with it. I picked the genre that is recommended by musicbrainz community most. And it's pivoted so that genres become columns so that we can use them as features.

clustering.ipynb: So far we have created the genres.csv for 20% of the artists that we have in original data. The reason is a mixture of two things. The artist name is not exactly matching the artist name in Musicbrainz database. In this notebook I did 3 things:
1. Run Principal component analysis on genres columns to reduce the dimensionality of the genres. And used K-means clustering to cluster the artists into 3 clusters using the elbow method.
2. Join genres.csv to our original dataframe. For non-matching artists the way is to merge is to assign 0s to each genre column.
3. Create the label column. The label column is the churn column. If a user has visited the cancellation confirmation page, it means that the user has churned. So I created a label column where 1 means churn and 0 means not churn.


