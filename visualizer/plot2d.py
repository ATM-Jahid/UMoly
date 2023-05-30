#!/usr/bin/env python

import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def draw(time, frame, fileName):
    # save in a mp4 file
    writeFile = fileName[:fileName.find('.pd')] + '.mp4'
    print(writeFile)

    fig, ax = plt.subplots()
    ln, = ax.plot([], [])

    def init():
        ax.set_xlim(0, 275)
        ax.set_ylim(0, 70)
        ax.set_aspect('equal')
        return ln,

    def update(t):
        for n in range(len(frame[t])):
            type = frame[t][n][0]
            if type == 1:
                colo = 'r'
            else:
                colo = 'b'

            orig = frame[t][n][1:3]
            vec = frame[t][n][4:-1]
            ax.plot([orig[0], vec[0]], [orig[1], vec[1]], color=colo)
            #ax.scatter(*vec, color=colo)

    anim = FuncAnimation(fig, update, frames=len(time), init_func=init,
                         interval=250, repeat=False)
    anim.save(writeFile, writer='ffmpeg', dpi=300, fps=2)
    #plt.show()

def main():
    files = sys.argv[1:]

    for file in files:
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

        draw(time, frame, file)

if __name__ == '__main__':
    main()
