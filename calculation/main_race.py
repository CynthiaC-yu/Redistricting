"""
Area: e.g. St. Louis City 
Transit Score: e.g. walk_score
We will allow user to choose STL City or County.
We will also allow user to choose the criterion of transit score.  

1. Partition design for race & ethnicity (X):
   - Input CSV columns (excluding "not hispanic or latino" and "two or more race"): zip_code, population, 
     American Indian and Alaska Native, Asian,Black or African American, Hispanic or Latino, 
     Native Hawaiian and Other Pacific Islander, Some Other Race, White.
   - We assign each ZIP to its predominant race if that group's share ≥ 0.8; otherwise, label it “mixed.”
     For example, if ZIP 63139 has White ≥ 0.8, we tag it “White.”
   - X is the set of these labels (at most 8: {mixed, American Indian…, Asian, Black…, Hispanic…, 
     Native Hawaiian…, Some Other Race, White}).
   - Let p_ij be the total population in the (X = i, Y = j) cell. Then
     Ent(X | Y = j) = Σ_i p_ij · log2(1 / p_ij).

2. Partition design for transit score (Y), following is an example:
   - Number of bins j = 3:
       • good: walk_score ≥ 0.8
       • average: 0.2 ≤ walk_score < 0.8
       • bad: walk_score < 0.2
   - Y is the bin label for each ZIP.

We compute the overall conditional entropy, which is calculating the sum while weighted each Y_j:
   Ent(X | Y) = Σ_j P(Y = j) · Ent(X | Y = j)

"""


"""
Normalize 
Calculate Ent(X)
Divide the conditonal entropy to Ent(X)

"""

import csv
import math

area = "county"
transit_score = "walk_score"
main_race_thresh = 0.75 
good_thresh = 0.8
bad_thresh = 0.2

'''
Input files.
Load census data. 
Load transit score and assign Y_label (Evaluating the Quality of Transit).

'''
race_file    = f'race_normalized_{area}.csv' # zip_code, population, race proportions
transit_file = f'transit_scores_{area}.csv' # zip_code, walk_score
output_file  = f'main_race_results_{area}_{transit_score}_{main_race_thresh}.txt'

race_cols = [
    'American Indian and Alaska Native',
    'Asian',
    'Black or African American',
    'Hispanic or Latino',
    'Native Hawaiian and Other Pacific Islander',
    'Some Other Race',
    'White'
]

race_data = {}
with open(race_file, newline='') as rf:
    reader = csv.DictReader(rf)
    for row in reader:
        zipc = row['zip_code']
        pop  = float(row['population'])
        props = {race: float(row[race]) for race in race_cols}
        race_data[zipc] = {'population': pop, 'proportions': props}

transit_data = {}
with open(transit_file, newline='') as tf:
    reader = csv.DictReader(tf)
    for row in reader:
        zipc = row['zip_code']
        score = float(row[transit_score])
        if score >= good_thresh:
            y_label = 'good'
        elif score >= bad_thresh:
            y_label = 'average'
        else:
            y_label = 'bad'
        transit_data[zipc] = y_label

labels_X = race_cols + ['mixed']
labels_Y = ['good', 'average', 'bad']

# Prepare containers for zip lists - for later ouput/debug purpose
zips_by_X = {x: [] for x in labels_X}
zips_by_Y = {y: [] for y in labels_Y}

'''
Build joint population counts for XY -- which is like a table that will help us to 
find the cooresponding popultion given to the input of main race label and transit quality

pop_XY[y][x]: Total population of ZIP areas whose main-race label X = x (e.g X = 'White')
                within the transit-quality partition Y = y (e.g. Y = 'bad').
# pop_Y[y]: Total population of all ZIP areas in the transit-quality partition Y = y.
'''
# Init dictionaries
pop_XY = {y: {x: 0.0 for x in labels_X} for y in labels_Y} # which is a nested dictionary
pop_Y  = {y: 0.0 for y in labels_Y}

# Every iteration we are attempting to label one zip code
for zipc, info in race_data.items():
    if zipc not in transit_data:
        continue
    pop   = info['population']
    props = info['proportions']
    main_race, main_prop = max(props.items(), key=lambda kv: kv[1]) 
    # the lambda func tells max() to compare the second element - the proportion - rather than the headers
    x_label = main_race if main_prop >= main_race_thresh else 'mixed'
    y_label = transit_data[zipc]

    # accumulate populations -- this stage we assign values to the dictionaries
    pop_XY[y_label][x_label] += pop 
    pop_Y[y_label] += pop

    # record zip assignments
    zips_by_X[x_label].append(zipc)
    zips_by_Y[y_label].append(zipc)
'''
Compute conditional entropy Ent(X|Y)
'''
total_pop = sum(pop_Y.values()) # Checking if normalized properly
ent_Y = {}
detailed = {}
for y in labels_Y:
    ent = 0.0
    detailed[y] = []
    for x in labels_X:
        p_xy = pop_XY[y][x]
        if p_xy > 0:
            term = p_xy * math.log2(1.0 / p_xy)
            ent += term
            
        else:
            term = 0.0
        detailed[y].append((x, p_xy, term))
    ent_Y[y] = ent

# using linear combination to calculate Ent(X|Y). We can safely do this as we already normalized 
# all data to the Zip code
ent_X_given_Y = sum(pop_Y[y] * ent_Y[y] for y in labels_Y)

pop_X_total = {x: 0.0 for x in labels_X}
for y in labels_Y:
    for x in labels_X:
        pop_X_total[x] += pop_XY[y][x]

ent_X = 0.0
for x in labels_X:
    p_x = pop_X_total[x] 
    if p_x > 0:
        ent_X += p_x * math.log2(1.0 / p_x)

seg_score = ent_X_given_Y / ent_X if ent_X > 0 else float('nan')

'''
Output result into txt file
'''
with open(output_file, 'w') as out:
    out.write("Conditional entropy of main-race partition X given transit score partition Y:\n\n")
    out.write(f"Area of Interest: {area}\n")
    out.write(f"Transit Score Criterion: {transit_score}\n")
    out.write(f"Total population (proportion): {total_pop:.2f}\n")
    out.write(f"Main-race Threshold: {main_race_thresh}\n")
    out.write(f"Good Transit-quality Threshold: {good_thresh}\n")
    out.write(f"Bad Transit-quality Threshold: {bad_thresh}\n\n")


    for y in labels_Y:
        out.write(f"Y = {y!r}:\n")
        out.write(f"\tpopulation in Y: {pop_Y[y]:.2f}\n")
        out.write(f"\tEnt(X|Y={y}): {ent_Y[y]:.4f} bits\n")
        out.write(f"\tSeg(X|Y={y}): {pop_Y[y] * ent_Y[y] / ent_X:.4f} bits\n")
        out.write("\t** Breakdown by main-race partition X **\n")
        for x, p_xy, term in detailed[y]:
            out.write(f"\t{x:45s} p_ij={p_xy:.4f}\tcontribution={term:.4f}\n")
        out.write("\n")
    out.write(f"Overall Ent(X): {ent_X:.4f} bits\n")
    out.write(f"Overall Ent(X|Y): {ent_X_given_Y:.4f} bits\n")
    out.write(f"Overall Seg(X|Y): {seg_score:.4f}\n\n")

    # ZIP codes in each Y partition
    out.write("ZIP codes by walk-score partition (Y):\n")
    for y in labels_Y:
        out.write(f"\t{y}: {', '.join(sorted(zips_by_Y[y]))}\n")
    out.write("\n")

    # ZIP codes in each X partition
    out.write("ZIP codes by main-race partition (X):\n")
    for x in labels_X:
        out.write(f"\t{x}: {', '.join(sorted(zips_by_X[x]))}\n")

print(f"Results (including full entropy breakdown) written to {output_file}")



zip_output_file = f'zip_results_{area}_{transit_score}_{main_race_thresh}.txt'

labels = labels_Y  # ['good','average','bad']

zips_lists = {y: sorted(zips_by_Y[y]) for y in labels}

max_len = max(len(v) for v in zips_lists.values())

with open(zip_output_file, 'w') as out:

    out.write('\t'.join(labels) + '\n')
    for i in range(max_len):
        row = []
        for y in labels:
            if i < len(zips_lists[y]):
                row.append(zips_lists[y][i])
            else:
                row.append('00000')  
        out.write('\t'.join(row) + '\n')

print(f"Vertical ZIP list for Y written to {zip_output_file}")
