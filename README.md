# Youtube Data API V3 - Data collection and visualization
In this project, I have worked with the Youtube Data API from Google. 
1. Generated an API key
2. Created a script.py file which contains the code to extract the trending videos and create a pandas file with the relevant information
3. Created analysis_script.py file which contains the code to add category names to the videos, as well as conduct the data visualizations via Seaborn

Worked with the Youtube API to get the trending videos in India, containing the following:
1. Video ID
2. Description
3. Views, Likes and Comment count
4. Tags used
5. Category ID (based which category name was added in the dataframe in the analysis_script)
6. Channel Title
7. Publishing Information and a few more details.


### Script.py
Creates a youtube service as per the API KEY.
Created a function to get the information of the videos as per paramaters specified.
Loop and run the function until a user specified amount of video information is collection.
Saved the resultant dataframe into a csv file.

### Analysis_Script.py
Creates a function to get the category ids and names as per the paramaters from the youtube API
Matches the category ids in the exported csv files and subsequently enters the matched category name
Conducted some preliminary data analysis on the dataframe, and subsequent visualization using seaborn.

Visualized statistics such as:
1. Histograms of Likes, Views and Comments
2. Categories with number of trending videos
3. Number of videos based on the hour when it was published
4. Correlation among the numeric attributes via a heatmap
5. Most recurring tags used in the videos
among others.

### Note
One can recreate this project by simply adding a file "config.py" which would have the variable (API_KEY) containing your own API KEY, to be used in the script.
Happy Coding!

### Some visualizations:
![Histogram Visual]((https://github.com/PranavP4tel/YouTube-Data-Project-1/blob/main/images/Figure_1.png))

![Categories with number of videos](https://github.com/PranavP4tel/YouTube-Data-Project-1/blob/main/images/Figure_2.png)

![Videos by Publishing Hour](https://github.com/PranavP4tel/YouTube-Data-Project-1/blob/main/images/Figure_4.png)
