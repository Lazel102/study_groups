# Study Groups

In this repo I implement an algorithm to distribute students in study groups and ensure diversity of disciplines present in each group.

## Algorithm 

The Algorithm works as follows : First the students are assigned randomly to a fixed number of groups which is specified in the script. Than we iterrate over all possible swaps and try to improve an overall diversity score which is determined by the number of disciplines present in each group. When there are no more swaps, which improve this score we stop.

## Usage 
Store the data in a csv-file called __data.csv__ with the columns : name, disciplines. Specify the group number in the __distribute.py__ file. In the variable "num_groups". Then run  ``` python distribute.py ``` .
This will produce a csv-file titled __grouped_students.csv__ with an additional column indicating the group each student is assigned to.

## Limitations
The algorithm is not guaranteed to find an optimal solution as it can get stucked in local maxima.


