import os
# Read the file

bd = os.path.split(os.path.abspath(__file__))[0]
fp = os.path.join(bd, 'data', 'haltestelle.in')

import pandas as pd
import numpy as np

data = pd.read_csv(fp, sep=" ", lineterminator="\n", names=['x', 'y'])

# Assuming we are starting with one point which is the first in the input file

start_xy = data.iloc[0, :]
print('Starting from\n\tx: {}\n\ty: {}'.format(start_xy.x, start_xy.y))

# Dropping the line that indicates the number of haltestellen (hs) coordinates hs_xy

hs_xy = data.dropna().iloc[1:, :]
hs_count = hs_xy.shape[0]
print('Count of haltestellen: {}'.format(hs_count))

# Find the closest haltestelle with Pythagoras

hs_xy['dist'] = np.sqrt(np.square(hs_xy['x'] - start_xy['x']) + np.square(hs_xy['y'] - start_xy['y']))

# Find smallest distance and the index of the frame
ind = hs_xy.dist.idxmin()

result = hs_xy.loc[ind]
print('The resulting coordinates and distance:\n', result)
# Write the ouptufile
r = pd.DataFrame(result[['x', 'y']]).T
r.to_csv(os.path.join(bd, 'haltestelle.out'), sep=' ', header=None, index=None)


