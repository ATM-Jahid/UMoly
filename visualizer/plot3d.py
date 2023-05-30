#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def draw(time, frame):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def update(t):
        for n in range(len(frame[t])):
            type = frame[t][n][0]
            if type == 1:
                colo = 'r'
            else:
                colo = 'b'

            orig = frame[t][n][1:4]
            vec = frame[t][n][4:]
            ax.plot([orig[0], vec[0]],
                    [orig[1], vec[1]],
                    [orig[2], vec[2]], color=colo)
            ax.scatter(*vec, color=colo)

    ax.set_xlim([0, 275])
    ax.set_ylim([0, 70])
    ax.set_zlim([0, 70])

    anim = FuncAnimation(fig, update, frames=len(time),
                         interval=250, repeat=False)
    #anim.save('animation.mp4', writer='ffmpeg', fps=2)
    plt.show()

def main():
    file = sys.argv[1]
    print(file)

    time = []; frame = []
    with open(file, 'r') as f:
        while True:
            f.readline()
            line = f.readline()
            if not line:
                break
            t = int(line.split()[1])
            time.append(t)

            f.readline()
            N = int(f.readline().split()[0])

            f.readline()
            coords = []
            for i in range(N):
                coord = [float(x) for x in f.readline().split()[1:]]
                coords.append(coord)
            frame.append(coords)

    draw(time, frame)

if __name__ == '__main__':
    main()
