import numpy as np
import pandas as pd
import matplotlib.pyplot as plt




w   = [-3, -2.5,  -2,  -1, -.6,  -.5, -.3, .3,    .5,    .8]
wins = [0,   1,    2,   3,   4,    5,   6,  7,     8,     9]

wins[0] = 67.9/67.4
wins[1] = 66.9/67.4
wins[2] = (67.4/67.4 + 66.7/64.5)/2
wins[3] = 66.9/65.2
wins[4] = (69.8/67.4 + 66.2/64.5 + 72.4/68.1)/3
wins[5] = 66.9/65.2
wins[6] = 68.6/68.1

wins[7] = (68/66.7 + 68.4/67.3 + 67/64.7)*100 + (70.2/66.9)*60
wins[7] = wins[7]/360
wins[8] = 65.5/68.1
wins[9] = 65.5/68.1


baseline = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]




plt.plot(w, wins)
plt. plot(w, baseline)

plt.xlabel('Weight w')
plt.ylabel('Success (Normalized by AB_Improved)')
plt.title('Success of Heuristic: Diff + w * Dist')


plt.show()

