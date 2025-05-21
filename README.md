# Redistricting

## Data Collection
I will briefly introduce the programs included in this folder.

### ZCTAs
A ZCTA (ZIP Code Tabulation Area) is the Census Bureau’s best‐fit area for a five-digit ZIP Code. You can think of it as a polygon drawn around the majority of addresses sharing the same ZIP. Unlike USPS ZIPs (which are routes, not areas), ZCTAs are static geographic units the Census uses to tabulate and publish population or demographic data at ZIP-like level.

Since all ZCTAs are valid USPS ZIPs, and they are more standardized, we will use ZCTAs as units of the data we collect for this project.

We fetched the St. Louis county and city's ZCTAs from Dexter — Data EXTractER. You may access the data with following link:

- https://mcdc.missouri.edu/cgi-bin/broker?_PROGRAM=utils.uex2dex.sas&path=/pub/data/corrlst&dset=us_stzcta5_county

**Note:** Throughout this document, “ZIP code” and “ZCTA” are used interchangeably; however, all references should be understood as **ZCTAs**.

### Data Processing Rules:
- **Transit Scores**  
  All transit-related metrics have been min–max rescaled to the \[0, 1\] interval.

- **Census Data**  
  Ethnicity counts were normalized by ZCTA population.  
  Mathematically, for each ZCTA and each group (e.g. White), we compute:
   $$
   \mathrm{NormalizedValue}_{\mathrm{ZCTA},\,\mathrm{group}}
   \;=\;
   \frac{\mathrm{Count}_{\mathrm{ZCTA},\,\mathrm{group}}}
      {\mathrm{Population}_{\mathrm{ZCTA}}}
   $$


### zip2census.py
Source of Info:
- https://data.census.gov/

This script will convert a list of zip codes to the cooresponidng ethinicity and race information from census data. Following is the categories we include:

- American Indian and Alaska Native
- Asian
- Black or African American
- Hispanic or Latino
- Native Hawaiian and Other Pacific Islander
- Not Hispanic or Latino
- Some Other Race
- Two or More Races
- White

Input: a list of zip codes
Output: a CSV file called **census_race_ethinicity.csv**
*I manually renamed the files and saved each for St. Louis City and St. Louis County.*  
- For St. Louis City: **census_race_ethinicity_city.csv**  
- For St. Louis County: **census_race_ethinicity_county.csv**

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


