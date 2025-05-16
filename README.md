# Redistricting

## Data Collection
I will briefly introduce the programs included in this folder.

### walk_score_zip_to_score.py
Source of Info: 
- https://www.walkscore.com/
- Python library: pgeocode.Nominatim

This script can directly convert a list of ZIP codes to the corresponding walk and bike scores.

Input: an array of ZIP codes  
Output: a CSV file named **zip_walk_bike_scores.csv**

*I manually renamed the files and saved each for St. Louis City and St. Louis County.*  
- For St. Louis City: **zip_walk_bike_scores_city.csv**  
- For St. Louis County: **zip_walk_bike_scores_county.csv**

### zip_code.py
Source of Info:
- https://nominatim.openstreetmap.org/search

This script allows you to convert an input array of ZIP codes to the corresponding latitude and longitude coordinates.

Input: an array of ZIP codes  
Output: a CSV file called **zip_code_to_coords.csv**  
*The file stored in the folder right now is just for testing purposes.*

### walk_score_input_multiple_and_array.py
Source of Info:
- https://www.walkscore.com/

This script has two functions:

1. Allows the user to input several lines, so they can enter as many latitude and longitude pairs as they want.  
   - Input: floats in the terminal  
   - Output: a CSV file called **walk_bike_scores.csv**

2. Allows the user to input an array of latitude and longitude coordinates.  
   - Input: an array of coordinates  
   - Output: a CSV file called **walk_bike_scores.csv**

*The file stored in the folder right now is just for testing purposes.*

### walk_score_input_one.py
Source of Info: 
- https://www.walkscore.com/

This script allows the user to input a pair of latitude and longitude coordinates and retrieve the corresponding walk and bike scores.

Input: floats in the terminal  
Output: corresponding walk and bike scores shown in the terminal


### allTransit_zip2score.py
Source of Info: 
- https://alltransit.cnt.org/metrics/

This script allows the user to input a list of zip codes and recrieve the cooresponding AllTransit score.

Input: a list of zip codes
Output: a CSV file called **allTransit.csv**
*I manually renamed the files and saved each for St. Louis City and St. Louis County.*  
- For St. Louis City: **allTransit_city.csv**  
- For St. Louis County: **allTransit_county.csv**

  
