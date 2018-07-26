'''
    Erste Zeile; Anzahl gemeldeter Tore: "Tore Quelle 1 (N)" "Tore Quelle 2 (M)" (beides Integer im Bereich 1 − 100)
    Zeile 2 - N+1; einzelne Tore, Quelle 1: "Team" "Zeitpunkt" (Team ist entweder "H" oder (Heim), "G" (Gast); der Zeitpunkt ist in Sekunden (Dezimalzahl) angegeben)
    Zeile N+2 - N+M+1; einzelne Tore, Quelle 2: "Team" "Zeitpunkt" (Details wie zuvor)

'''
import os
import pandas as pd
import numpy as np

try:
    bd = os.path.split(os.path.abspath(__file__))[0]
except NameError:
    bd = os.getcwd()

fp = os.path.join(bd, 'data', 'events.in')

datasrc_count = 2
header_lines = 1


dstruct = pd.read_csv(fp, sep=' ', nrows=header_lines, names=['s{}'.format(i) for i in range(datasrc_count)]).values[0]
data = pd.read_csv(fp, sep=' ', names=['team', 'score_time'], skiprows=header_lines)


# This block can be generalized for n sources with the below notation
n = dstruct[0]
m = dstruct[1]

datasrc_inds = [
    list(np.arange(0, n)),
    list(np.arange(n, n+m))
]

# Use the indices to flag the source

data['src_flag'] = [1 for i in range(n)] + [2 for i in range(m)]

'''
Assumptions datasets of both sources:
    1. The team als always correctly assigned
    2. There are no fake goals, just missing goals
    3. The time when scored lies somewhere between the to score times in both data sources
    4. The biggest dataset doesn't necessarely contain all goals
'''

# Preprocessing: sort by score time
df = data.sort_values(by='score_time')
df.reset_index(inplace=True, drop=True)

# The best solution i can come up with is the following:

# Find out where two neighboring entries are closer than t_limit
# there has to be some limit in order to separate two goals

t_limit = 15        # if from two sources and same team there is a goal, they are counted as two if the score time difference exceeds t_limit
mask = np.diff(df.score_time) < t_limit
merge_inds = np.where(mask)[0] # starting indices from where to merge two rows

# test if the really come from two sources
testing_mask = []
for index in merge_inds:
    if df.src_flag[index] == df.src_flag[index+1]:
        print(index, ': set False')
        testing_mask.append(False)
    else:
        print(index, ': set True')
        testing_mask.append(True)

merge_inds = merge_inds[testing_mask]

rdf = df.copy(deep=True)
for i in merge_inds:
        rdf.loc[i, 'score_time'] = np.mean([rdf.loc[i, 'score_time'], rdf.loc[i+1, 'score_time']]).round(1)

rdf.drop(list(merge_inds+1), inplace=True)

# Write file
header = [str(rdf.shape[0]), None]
fp_out = os.path.join(bd, 'events.out')
rdf.to_csv(fp_out, sep=' ', columns=['team', 'score_time'], index=None, header=header)

