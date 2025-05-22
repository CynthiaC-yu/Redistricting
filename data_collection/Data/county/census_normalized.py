import csv

'''
Normalized the ethinicity columns for the census data.

What we did mathematically:
For each zip code, we did following calculation for its data:
race and ethinitity column (e.g. white) / total population of the zip code
'''

place = 'county'
if place == 'city':
    TOTAL_POP = 564266 # CITY
elif place == 'county':
    TOTAL_POP = 1074242 # COUNTY
census_file     = f'census_race_ethnicity_{place}.csv'
population_file = f'zip_population_{place}.csv'
output_file     = f'census_normalized_{place}.csv'

ethnicity_cols = [
    'American Indian and Alaska Native',
    'Asian',
    'Black or African American',
    'Hispanic or Latino',
    'Native Hawaiian and Other Pacific Islander',
    'Not Hispanic or Latino',
    'Some Other Race',
    'Two or More Races',
    'White'
]

pop_map = {}
with open(population_file, newline='') as pop_f:
    reader = csv.DictReader(pop_f)
    for row in reader:
        zipc = row['zip_code']
        try:
            pop_map[zipc] = float(row['population'])
        except ValueError:
            pop_map[zipc] = 0.0

with open(census_file, newline='') as cen_f, \
     open(output_file, 'w', newline='') as out_f:

    reader = csv.DictReader(cen_f)
    fieldnames = ['zip_code', 'population'] + ethnicity_cols
    writer = csv.DictWriter(out_f, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        zipc = row['zip_code']
        pop  = pop_map.get(zipc, 0.0)

        out_row = {
            'zip_code': zipc,
            'population': pop / TOTAL_POP
        }

        if pop > 0:
            for col in ethnicity_cols:
                try:
                    count = float(row.get(col, 0))
                    out_row[col] = count / pop
                except ValueError:
                    out_row[col] = ''
        else:
            for col in ethnicity_cols:
                out_row[col] = ''

        writer.writerow(out_row)

print(f"Normalized data saved to {output_file}")
