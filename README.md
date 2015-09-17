# Music Explorer

- Music is cool  
- Genres aren't intuitive  
- Music has logical physical properties (tempo, key, etc.)  
- The goal: group songs and generate recommendations based on the physical attributes  

Data taken from the [Million Song Dataset](http://labrosa.ee.columbia.edu/millionsong/), associated user data, and user data from [Last.fm](http://www.last.fm/home). Code to process the data, get user listening histories, and  generate track features for clusters is in the data_formatting folder.  

User data from both the Million Song Dataset and [Last.fm](http://www.last.fm/home), code to collect this data is in the get_user_data folder.  

Code for clustering, visualizing the clustering results, making a table for quick recommendations, and sending the table to postgresql is in the main directory.  

Introductory description of this project process can be found on my [blog](http://trishaandrews.com/MSD-Intro/)
