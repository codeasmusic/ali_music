import cPickle as pickle
import matplotlib.pyplot as pyplot


def load(file_name):
	with open(file_name, "r") as fid:
		return pickle.load(fid)


def plot_multi_lines(xlist, ylist, path, xlabel, ylabel, title):
	max_y = -1
	for idx in range(len(xlist)):
		pyplot.plot(xlist[idx], ylist[idx])

		new_max = max(ylist[idx])
		if new_max > max_y:
			max_y = new_max

	max_x = max(xlist[0])
	max_y *= 1.05

	pyplot.xlabel(xlabel)
	pyplot.ylabel(ylabel)
	pyplot.title(title)

	pyplot.axis([0, max_x, 0, max_y])
	pyplot.savefig(path)

	pyplot.clf()
	#Don't close pyplot; otherwise, pyplot could not be called next time
	# pyplot.close()