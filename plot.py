import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import json

def drawPlots(fig, file_name, data_ind, mark_ind=None):
    with open(file_name, 'r') as f:
        data = json.loads(f.read())

    samples = []
    for sample in data[data_ind]["DATABLOCK"]:
        samples.append(sample["data"])

    if mark_ind:
        start, end = data[mark_ind]["MARK"][1]["MARK_START"], data[mark_ind]["MARK"][2]["MARK_END"]
    data = np.array(samples)
    np.place(data, data > 10**4, 0)
    np.place(data, data < -10**4, 0)

    axes = fig.get_axes()

    for i, ax in enumerate(axes):
        if not mark_ind:
            ax.plot(data[:, i])
        else:
            ax.plot([j for j in range(start, len(data) if end > len(data) else end)], data[start:end, i])

fig = plt.figure(figsize=(8, 8), dpi=100)
for j in range(8):
    fig.add_subplot(8, 1, j+1)

drawPlots(fig, 'data/Disgust.json', 7)
drawPlots(fig, 'data/Disgust.json', 7, 6)
# drawPlots(fig, 'data/sadReal.json', 7, 6)
drawPlots(fig, 'data/JOY.json', 8, 7)


# drawPlots(fig, 'data/Disgust.json', 7)
# drawPlots(fig, 'data/lool.json', 10, 6)
# drawPlots(fig, 'data/lool.json', 10, 7)

plt.show()


def calculate_freqs(samples, freq):
    segments = int(len(smaples)/250)
    freqs = [[0,]*8]*segments

    for i in range(segments-1):
        for j in range(8):
            
#Частоты
# segments = int(len(data)/250)
# freqs = [[0] * segments] * 8

# fig = plt.figure(figsize=(8, 8), dpi=100)

# for j in range(8):
#       fig.add_subplot(8, 1, j+1)

# axes = fig.get_axes()

# for i in range(segments-1):
#   for j, ax in enumerate(axes):
#       seg = data[i*250:i*250+250]

#       f = 0
#       isMin, isMax = False, False
#       for k in range(1, len(seg)-1):
#           if seg[k-1][j] < seg[k][j] > seg[k+1][j]: #Если максимум
#               isMax = True
#           elif seg[k-1][j] > seg[k][j] < seg[k+1][j]: #Если максимум
#               isMin = True

#           if isMax and isMin:
#               f += 1
#               isMax, isMin = False, False

        
#       freqs[j][i] = f


# for j, ax in enumerate(axes):
#   # ax.plot(freqs[j])
#   ax.plot([j for j in range(int(start/250), segments if int(end/250)>segments else int(end/250))], 
#       freqs[j][int(start/250):int(end/250)])


