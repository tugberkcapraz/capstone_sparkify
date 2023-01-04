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

Data Understanding

I did it and made a beautiful table for you so that we spend less time here.
The catch it, the label is not given to you. It's stored in the pages column with the 'cancellation_confirmation' value. And you have to work your way to get it first.
