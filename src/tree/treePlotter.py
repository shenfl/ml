import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

t = np.arange(0, 5, 0.2)

# plt.plot([1, 2, 3, 4], [1, 4, 9, 16], "b-")
# plt.axis([0, 6, 0, 20])
# plt.show()

# line = plt.plot(t, t, linewidth=4.0)
# aa = plt.setp(line)
# print(aa)

# img = mpimg.imread("E:\\python\\1.png")
# print(img)
# img = img[:, :, 0]
# # imgplot = plt.imshow(img, cmap="hot")
# # plt.colorbar()
# plt.hist(img.ravel(), bins=256, range=(0.0, 1.0), fc='k', ec='k')
# plt.show()


x = np.arange(0, 10, 0.005)
y = np.exp(-x/2.) * np.sin(2*np.pi*x)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y)
ax.set_xlim(0, 10)
ax.set_ylim(-1, 1)

plt.show()