import matplotlib
matplotlib.use('Gdk') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt

fig = plt.figure()
plt.plot(range(10))
fig.savefig('temp.png')
