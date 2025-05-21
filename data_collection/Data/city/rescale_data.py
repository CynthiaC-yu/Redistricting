import csv
'''
This code can rescale data of a table and output a csv file. 
Just need to make sure the directory you are contains both the data file and this method file.
'''

# file_name = 'allTransit_county'
file_name = 'zip_walk_bike_scores_county'

# file_name = 'allTransit_city'
# file_name = 'zip_walk_bike_scores_city'

input_file = file_name + '.csv'
output_file = file_name +'_rescaled'+ '.csv'

with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    
    header = next(reader)
    writer.writerow(header)
    '''
    For Rescale AllTransit data
    '''
    # wt_avg_L_index = header.index('wt_avg_L')
    
    # for row in reader:
    #     try:
    #         value = float(row[wt_avg_L_index])
    #         row[wt_avg_L_index] = str(round(value / 10, 2))
    #     except ValueError:
    #         # If conversion fails, leave the original value
    #         pass
    #     writer.writerow(row)    



    '''
    For Rescale WalkScore data
    '''
    walk_score_index = header.index('walk_score')
    bike_score_index = header.index('bike_score')

    for row in reader:
        try:
            value_walk = float(row[walk_score_index])
            value_bike = float(row[bike_score_index])
            row[walk_score_index] = str(round(value_walk / 100, 2))
            row[bike_score_index] = str(round(value_bike / 100, 2))
        except ValueError:
            # If conversion fails, leave the original value
            pass
        writer.writerow(row)



print(f"Modified CSV saved to: {output_file}")

