# Twitter-Viewer-Editor
We have a dataset of tweets from various users related to the US Presidential Election 2012. We want to create a Twitter Viewer & Editor that will allow the user to perform the following commands:

View the current tweet, display the tweet with the current tweet ID, move to the next tweet, change the current tweet ID to the next tweet in the dataset,
move to the previous tweet, change the current tweet ID to the previous tweet in the dataset, edit a tweet, delete the old version of a tweet and create a new version in the format: {"text": "...here goes the text...", "created at": "...here goes datetime..."}, write the new version to the correct line/position based on the ID/line number of the tweet that was edited (in memory or if saved to a file).
It's important to note that when updating a tweet, we delete the old version and create a new version with the updated content, preserving the original tweet's ID and position in the dataset (either in memory or eventually saved to a file).
