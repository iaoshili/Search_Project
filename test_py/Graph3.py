#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

N = 5
accuracy = (0.855, 0.82875, 0.8625, 0.70625, 0.89)

ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, accuracy, width, color='#9999ff')

precision =  (0.817796610169, 0.713197969543, 0.558139534884, 0.227118644068, 0.245614035088)
rects2 = ax.bar(ind+width, precision, width, color='#ff9999')

recall =  (0.725563909774, 0.92131147541, 0.738461538462, 0.905405405405, 0.933333333333)
rects3 = ax.bar(ind+2*width, recall, width, color='y')

fMeasure =  (0.768924302789, 0.804005722461, 0.635761589404, 0.363143631436, 0.388888888889)
rects4 = ax.bar(ind+3*width, fMeasure, width, color='b')

# add some text for labels, title and axes ticks
ax.set_ylabel('Results')
ax.set_title('Accuracy, precision, recall and F measure of different algorithms on different categories')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Tech', 'Culture', 'US&World', 'Design', 'Transportation') )

ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), ('Accuracy', 'Precision','Recall','F measure') )

# def autolabel(rects):
#     # attach some text labels
#     for rect in rects:
#         height = rect.get_height()
#         ax.text(rect.get_x()+rect.get_width()/4., 1.05*height, '%d'%int(height),
#                 ha='center', va='bottom')

# autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)
# autolabel(rects4)

plt.show()