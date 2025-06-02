import csv
import math
import numpy as np
import matplotlib.pyplot as plt


'''
3 or 5: edit the parameters
'''
def load_data(area, transit_score, main_race_thresh,
              very_good_thresh = 0.8, good_thresh=0.6, bad_thresh=0.4, very_bad_thresh=0.2):
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
    labels_Y = ['very_good', 'good', 'average', 'bad', 'very_bad']


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
            score = float(r[transit_score])
            '''
            3
            '''
            # if score >= good_thresh:
            #     y_label = 'good'
            # elif score >= bad_thresh:
            #     y_label = 'average'
            # else: 
            #     y_label = 'bad'

            '''
            5
            '''
            if score >= very_good_thresh:
                y_label = 'very_good'
            elif score >= good_thresh:
                y_label = 'good'
            elif score >= bad_thresh:
                y_label = 'average'
            elif score >= very_bad_thresh:
                y_label = 'bad'
            else:
                y_label = 'very_bad'


            transit[z] = y_label
    # cumulate pop_XY, pop_Y
    pop_XY = {y:{x:0.0 for x in labels_X} for y in labels_Y}
    pop_Y  = {y:0.0 for y in labels_Y}

    for z,(pop,props) in race_data.items():
        if z not in transit: 
            continue

        main_race, main_p = max(props.items(), key=lambda kv: kv[1])
        x_lab = main_race if main_p>=main_race_thresh else 'mixed'
        y_lab = transit[z]
        pop_XY[y_lab][x_lab] += pop
        pop_Y[y_lab] += pop

    return labels_X, labels_Y, pop_XY, pop_Y


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
    total = sum(pop_Y.values()) # check if sum to 1
    '''
    I already checked the total is sum to 1.
    '''
    # P(X=i), P(Y=j)
    # It should be sum(pop_XY[y][x] for y in labels_Y)/total, but we will omit total since it's 1 in code
    p_X = {x: sum(pop_XY[y][x] for y in labels_Y) for x in labels_X}
    p_Y = {y: pop_Y[y] for y in labels_Y}

    seg_i = {}
    for x in labels_X:
        s = 0.0
        for y in labels_Y:
            p_x_given_y = (pop_XY[y][x]/pop_Y[y]) if pop_Y[y]>0 else 0.0
            s += p_Y[y]*abs(p_x_given_y - p_X[x])
        seg_i[x] = s
    seg_prob = sum(p_X[x]*seg_i[x] for x in labels_X)


    '''
    calc max
    '''
    max_seg = 2 * sum(p_X[x]**2 * (1-p_X[x]) for x in labels_X)

    '''
    Normalized
    '''
    seg_prob_norm = seg_prob / max_seg if max_seg>0 else float('nan')
    seg_prob_flip = 1 - seg_prob_norm
    return seg_prob_flip

area = "county"
transit_score = "walk_score"


transit_threshold_sets = [
    (0.80, 0.60, 0.40, 0.20),   
    (0.90, 0.70, 0.50, 0.30),   
    (0.70, 0.50, 0.30, 0.10)   
]
# thresholds_main_race = [0.55, 0.6, 0.7, 0.75, 0.8, 0.81, 0.85, 0.9, 0.905, 0.91]
thresholds_main_race = [i * 0.01 for i in range(100)]


n_sets = len(transit_threshold_sets)
ent_curve  = np.full((n_sets, len(thresholds_main_race)), np.nan)
prob_curve = np.full((n_sets, len(thresholds_main_race)), np.nan)


print("thresh|Seg ent|Seg prob")
print("------|-------|--------")

counter = 0
for idx, (vg_th, g_th, b_th, vb_th) in enumerate(transit_threshold_sets):
    r_seg_ent = []
    r_seg_prob = []
    counter += 1
    for i, r_thresh in enumerate(thresholds_main_race):
        labels_X, labels_Y, pop_XY, pop_Y = load_data(
            area, transit_score, r_thresh,
            very_good_thresh=vg_th,
            good_thresh=g_th,
            bad_thresh=b_th,
            very_bad_thresh=vb_th
        )
        se = compute_ent(labels_X, labels_Y, pop_XY, pop_Y)
        sp = compute_prob(labels_X, labels_Y, pop_XY, pop_Y)
        ent_curve[idx, i]  = se
        prob_curve[idx, i] = sp

        r_seg_ent.append(se)
        r_seg_prob.append(sp)

        var_ent = np.nanvar(r_seg_ent)
        var_prob = np.nanvar(r_seg_prob)
    print(f"Iteration: {counter}")
    print(f"Variance of entropy method: {var_ent}")
    print(f"Variance of probabilistic method: {var_prob}")

all_ent_vals  = ent_curve.flatten()
all_prob_vals = prob_curve.flatten()
var_ent_all  = np.nanvar(all_ent_vals)
var_prob_all = np.nanvar(all_prob_vals)

print("=== Overall Variance ===")
print(f"Seg_entropy Overall Var: {var_ent_all:.6f}")
print(f"Seg_prob_flip Overall Var: {var_prob_all:.6f}")




# '''
# Evaluating metric: Variance
# '''
# var_ent = np.nanvar(overall_seg_ent)
# var_prob = np.nanvar(overall_seg_prob)

# print(f"Variance of entropy method: {var_ent}")
# print(f"Variance of probabilistic method: {var_prob}")



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

# plot_seg_comparison(thresholds_main_race, r_seg_ent, r_seg_prob)




plt.figure(figsize=(12, 5))


ax1 = plt.subplot(1, 2, 1)
for idx, (vg_th, g_th, b_th, vb_th) in enumerate(transit_threshold_sets):
    ax1.plot(
        thresholds_main_race,
        ent_curve[idx],
        label=f"VG={vg_th},G={g_th},B={b_th},VB={vb_th}"
    )
ax1.set_title("Entropy")
ax1.set_xlabel("main_race_thresh")
ax1.set_ylabel("Seg_entropy")
ax1.legend(fontsize=8)
ax1.grid(True)
ax1.set_xlim(0,1)
ax1.set_ylim(0,1)


ax2 = plt.subplot(1, 2, 2)
for idx, (vg_th, g_th, b_th, vb_th) in enumerate(transit_threshold_sets):
    ax2.plot(
        thresholds_main_race,
        prob_curve[idx],
        label=f"VG={vg_th},G={g_th},B={b_th},VB={vb_th}"
    )
ax2.set_title("Probability")
ax2.set_xlabel("main_race_thresh")
ax2.set_ylabel("Seg_prob_flip")
ax2.legend(fontsize=8)
ax2.grid(True)

ax2.set_ylim(0,1)
ax2.set_xlim(0,1)
plt.show()
