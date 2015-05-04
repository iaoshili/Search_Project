#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

N = 2
accuracy = (0.855, 0.7775)

ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, accuracy, width, color='#9999ff')

precision =  (0.817796610169, 0.919642857143)
rects2 = ax.bar(ind+width, precision, width, color='#ff9999')

recall =  (0.725563909774, 0.378676470588)
rects3 = ax.bar(ind+2*width, recall, width, color='y')

fMeasure =  (0.768924302789, 0.536458333333)
rects4 = ax.bar(ind+3*width, fMeasure, width, color='b')

# add some text for labels, title and axes ticks
ax.set_ylabel('Results')
ax.set_title('Accuracy, precision, recall and F measure with or without tiltle bonus 10')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Without title bonus', 'With title bonus') )

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