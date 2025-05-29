import csv
import math
import numpy as np

import matplotlib.pyplot as plt


def load_data(area, transit_score, main_race_thresh,
              good_thresh=0.8, bad_thresh=0.2):
    race_cols = [
        'American Indian and Alaska Native',
        'Asian',
        'Black or African American',
        'Hispanic or Latino',
        'Native Hawaiian and Other Pacific Islander',
        'Some Other Race',
        'White'
    ]
    labels_X = race_cols + ['mixed']
    labels_Y = ['good', 'average', 'bad']

    # read race
    race_data = {}
    with open(f'race_normalized_{area}.csv', newline='') as rf:
        reader = csv.DictReader(rf)
        for r in reader:
            z = r['zip_code']
            pop = float(r['population'])
            props = {c: float(r[c]) for c in race_cols}
            race_data[z] = (pop, props)

    # read transit
    transit = {}
    with open(f'transit_scores_{area}.csv', newline='') as tf:
        reader = csv.DictReader(tf)
        for r in reader:
            z = r['zip_code']
            s = float(r[transit_score])
            if s >= good_thresh:    
                transit[z] = 'good'
            elif s >= bad_thresh:     
                transit[z] = 'average'
            else:                     
                transit[z] = 'bad'

    # cumulate pop_XY, pop_Y
    pop_XY = {y:{x:0.0 for x in labels_X} for y in labels_Y}
    pop_Y  = {y:0.0 for y in labels_Y}

    for z,(pop,props) in race_data.items():
        if z not in transit: continue
        main_race, main_p = max(props.items(), key=lambda kv: kv[1])
        x_lab = main_race if main_p>=main_race_thresh else 'mixed'
        y_lab = transit[z]
        pop_XY[y_lab][x_lab] += pop
        pop_Y[y_lab] += pop

    return labels_X, labels_Y, pop_XY, pop_Y


# def compute_ent(labels_X, labels_Y, pop_XY, pop_Y):
#     """
#     Return Seg_entropy = H(X|Y)/H(X), guaranteed in [0,1].
#     pop_XY[y][x] 和 pop_Y[y] 都是“人数”。
#     """
#     total = sum(pop_Y.values())

#     # 1) H(X|Y)
#     #    H(X|Y=j) = - sum_i P(X=i | Y=j) * log2 P(X=i | Y=j)
#     #    H(X|Y)   = sum_j P(Y=j) * H(X | Y=j)
#     ent_cond = 0.0
#     for y in labels_Y:
#         if pop_Y[y] == 0:
#             continue
#         py = pop_Y[y] / total
#         # H(X|Y=j)
#         h_xyj = 0.0
#         for x in labels_X:
#             p_ij = pop_XY[y][x] / pop_Y[y]    # P(X=i | Y=j)
#             if p_ij > 0:
#                 h_xyj -= p_ij * math.log2(p_ij)
#         ent_cond += py * h_xyj


#     ent_X = 0.0
#     # P(X=i) = sum_j pop_XY[j][i] / total
#     for x in labels_X:
#         px = sum(pop_XY[y][x] for y in labels_Y) / total
#         if px > 0:
#             ent_X -= px * math.log2(px)


#     seg_entropy = ent_cond / ent_X if ent_X > 0 else float('nan')
#     return seg_entropy


def compute_ent(labels_X, labels_Y, pop_XY, pop_Y):
    ent_Y = {}
    for y in labels_Y:
        ent = 0.0
        if pop_Y[y] == 0:
            ent_Y[y] = 0.0
            continue
        for x in labels_X:
            p_xy = pop_XY[y][x] / pop_Y[y]
            if p_xy > 0:
                term = - p_xy * math.log2(p_xy) #!!!
                ent += term
            else:
                term = 0.0
        ent_Y[y] = ent

    # using linear combination to calculate Ent(X|Y). We can safely do this as we already normalized 
    # all data to the Zip code
    ent_X_given_Y = sum(pop_Y[y] * ent_Y[y] for y in labels_Y)


    ent_X = 0.0
    for x in labels_X:
        # P(X=x)
        p_x = sum(pop_XY[y][x] for y in labels_Y) 
        if p_x > 0:
            ent_X += - p_x * math.log2(p_x) #!!!

    seg_entropy = ent_X_given_Y / ent_X if ent_X > 0 else float('nan')
    return seg_entropy

def compute_prob(labels_X, labels_Y, pop_XY, pop_Y):
    total = sum(pop_Y.values())
    # P(X=i), P(Y=j)
    p_X = {x: sum(pop_XY[y][x] for y in labels_Y)/total for x in labels_X}
    p_Y = {y: pop_Y[y]/total for y in labels_Y}

    seg_i = {}
    for x in labels_X:
        s = 0.0
        for y in labels_Y:
            p_x_given_y = (pop_XY[y][x]/pop_Y[y]) if pop_Y[y]>0 else 0.0
            s += p_Y[y]*abs(p_x_given_y - p_X[x])
        seg_i[x] = s
    seg_prob = sum(p_X[x]*seg_i[x] for x in labels_X)

    max_seg = 2 * sum(p_X[x]**2 * (1-p_X[x]) for x in labels_X)

    seg_prob_norm = seg_prob / max_seg if max_seg>0 else float('nan')

    return seg_prob_norm

area = "county"
transit_score = "walk_score"
# thresholds_main_race = [0.55, 0.6, 0.7, 0.75, 0.8, 0.81, 0.85, 0.9, 0.905, 0.91]
thresholds_main_race = [i * 0.1 for i in range(10)]

overall_seg_ent = []
overall_seg_prob = []
print("thresh|Seg ent|Seg prob")
print("------|-------|--------")
for thresh in thresholds_main_race:
    labels_X, labels_Y, pop_XY, pop_Y = load_data(area, transit_score, thresh)
    se = compute_ent(labels_X, labels_Y, pop_XY, pop_Y)
    sp = compute_prob(labels_X, labels_Y, pop_XY, pop_Y)
    overall_seg_ent.append(se)
    overall_seg_prob.append(sp)
    print(f"{thresh:.3f}  |{se:.4f} |{sp:.4f}")



def plot_seg_comparison(thresholds, seg_entropy, seg_prob):
    plt.figure()
    plt.plot(thresholds, seg_entropy, marker='o', label='Seg_entropy')
    plt.plot(thresholds, seg_prob, marker='o', label='Seg_prob')
    plt.xlabel('main_race_thresh')
    plt.ylabel('Segmentation Metric')
    plt.title('comparison of Seg_entropy vs Seg_prob')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_seg_comparison(thresholds_main_race, overall_seg_ent, overall_seg_prob)
