# importing libraries
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
# creating a subplot
ax1 = fig.add_subplot(1, 1, 1)


def animate(i):
	data = open('fitness.txt', 'r').read()
	lines = data.split('\n')
	xs = []
	ys = []
	xa = []
	ya = []
	for line in lines:
		if len(line.split()) == 0:
			break
		x, y = line.split()
		xs.append(float(x))
		ys.append(float(y))

	data = open('avg_fitness.txt', 'r').read()
	lines = data.split('\n')
	for line in lines:
		if len(line.split()) == 0:
			break
		x, y = line.split()
		xa.append(float(x))
		ya.append(float(y))

	ax1.clear()
	ax1.plot(xs, ys, 'r', ya, 'b')

	plt.xlabel('Generation')
	plt.ylabel('Fitness')
	plt.title('Animated Graph')


ani = animation.FuncAnimation(fig, animate, interval=60)
plt.show()

