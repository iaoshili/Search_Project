#!/usr/bin/env python
# a bar plot with errorbars
import numpy as np
import matplotlib.pyplot as plt

N = 5
accuracy = (0.855, 0.81625, 0.8125, 0.79375, 0.79875)

ind = np.arange(N)  # the x locations for the groups
width = 0.2       # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(ind, accuracy, width, color='#9999ff')

precision =  (0.817796610169, 0.736842105263, 0.744855967078, 0.88, 0.851351351351)
rects2 = ax.bar(ind+width, precision, width, color='#ff9999')

recall =  (0.725563909774, 0.658823529412, 0.672862453532, 0.47311827957, 0.475471698113)
rects3 = ax.bar(ind+2*width, recall, width, color='y')

fMeasure =  (0.768924302789, 0.695652173913, 0.70703125, 0.615384615385, 0.610169491525)
rects4 = ax.bar(ind+3*width, fMeasure, width, color='b')

# add some text for labels, title and axes ticks
ax.set_ylabel('Results')
ax.set_title('Accuracy, precision, recall and F measure of different algorithms on category tech')
ax.set_xticks(ind+width)
ax.set_xticklabels( ('Multinomial NB', 'Bernoulli NB', 'Logistic Regression', 'SVM', 'Null SVC') )

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