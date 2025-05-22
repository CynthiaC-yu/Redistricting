import csv
place = 'county'
input_file  = f'census_normalized_{place}.csv'
output_file = f'race_normalized_{place}.csv'

drop_cols = {'Not Hispanic or Latino', 'Two or More Races'}

with open(input_file, newline='') as infile, \
     open(output_file, 'w', newline='') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = [fn for fn in reader.fieldnames if fn not in drop_cols]
    
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        # Remove unwanted keys
        for col in drop_cols:
            row.pop(col, None)
        writer.writerow(row)

print(f"Filtered data written to {output_file}")