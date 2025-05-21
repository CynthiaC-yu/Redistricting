import csv

'''
Combine columns from different csv file together.
Just need to make sure the directory you are contains both the data file and this method file.
'''

# Paths to your input files
place = 'city'
transit_file = f'allTransit_{place}_rescaled.csv'
scores_file  = f'zip_walk_bike_scores_{place}_rescaled.csv'
output_file  = f'transit_scores_{place}.csv'

wt_map = {}
with open(transit_file, 'r', newline='') as f_transit:
    reader = csv.DictReader(f_transit)
    for row in reader:
        zipc = row['zip_code']
        wt_map[zipc] = row['wt_avg_L']

with open(scores_file, 'r', newline='') as f_scores, \
     open(output_file, 'w', newline='') as f_out:

    reader = csv.DictReader(f_scores)
    fieldnames = ['zip_code', 'wt_avg_L', 'walk_score', 'bike_score']
    writer = csv.DictWriter(f_out, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        zipc = row['zip_code']
        if zipc in wt_map:
            writer.writerow({
                'zip_code':  zipc,
                'wt_avg_L':  wt_map[zipc],
                'walk_score': row.get('walk_score', ''),
                'bike_score': row.get('bike_score', '')
            })

print(f"Wrote merged data to {output_file}")


