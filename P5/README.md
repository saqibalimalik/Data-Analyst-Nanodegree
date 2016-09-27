## Make Effective Data Visualization: Titanic Data
by SAQIB ALI

### Introduction

I created 4 different charts/graphs to tell the story of Titanic data analysis. Charts represent the survivals based on Gender, Age, Class they are travelling.


### Design

#### Data Analysis and Improvements

I got the data from the data options link provided by the Porject insturctions section. I picked Titanic data because I already did a project "Investigate a Dataset" using this data. So I am already familiar with this data set. The data provided was already cleaned, which didn't need any clean or transformation. 
After looking at the data and getting feedback from different people, I decided create separate csvs for the rates.

The most important feature to analyse in dataset is obiviously the Survival Rate. After looking at data, curosity starts about which gender, age or other factors had affect on Survival rate. If you rember the movie, you already get some idea that women and children were given priority to aboard the safety boats first. We also see some rich people tried to bribe the crew to aboard the boats first. So we kind of get alot of hypothesis about this data.

#### Data Visualization Design

After doing some research, I realised dimple.js is easier and quicker to implement. So I chose dimple.js for creating visualiztion from the data.

I tried to create some scatter plots or line charts, but other than age there was no other continuous variable to be used. So my choices were limited to only categorical representations using bar charts. In all charts I chose light blue for women and pink for men. 

Chart 1: For this chart I chose to use side by side bar vertical bar chart to see the survival rate per gender in each class. I used the 3 classes on x axis and number of survivals on y axis. It shows lower survival rates for lower classes but higher survival rate for first class passengers. Also in each class, survival rate for women is higher than men.

Chart 2. I chose to use a bar chart because I wanted to show survival rate by Age Group. I tried different sizes of bins for Age Category axis, but size 15 seemed to look cleaner and better. We see children under age 15 had highest survival rate.


### Feedback

After intial charts, I gathered 4 reviews from my wife, a collegue, udacity reviewer and a friend. Below is summary of their reviews. 

#### Review #1

> Like the blue and pinkish colors. Charts are too wide to fit page. Also charts don't tell what they explain. Please add some labels or description.

#### Review #2

> Charts look good. Instead of using ages, make category of ages so that your histogram and the final chart looks cleaner. Ofcourse add labels. Legends should be moved inside the cart aread for 2nd chart. 

#### Review #3

> Histogram is not pretty at all. The final chart conveys no information at all. It should be either expanded in size to see y-axis ticks, or use larger bins to make it better. Pie chart is bit too large and legend is too far away. You do not need legend for histogram.

#### Review #4
> Pie charts are misleading visualization tool. The counts should be replaced with rates. 

### Post-feedback Design

Following imporvements were made

- Removed Pie Chart
- Added Heading at top of the page
- Moved legend inside the chart area.
- Decrease the size of svg to smaller value.
- Removed Chart 4
- Used Excel to create survival rates
- Used Excel to create age bins of size 15 with 60+ and N/A.
- Used the Age Group in 2nd Chart.
- Ofcourse added labels.

### Resources

- [dimple.js Documentation](http://dimplejs.org/)

### Data

- `titanic.csv`: original downloaded dataset with one more Column AgeCategory for dimple.js implementation.