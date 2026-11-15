import sys

import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from matplotlib.animation import FuncAnimation



#file = np.genfromtxt(fname="//wsl.localhost/Ubuntu-24.04/home/fba/projects/MATINS-intel/out/2D/Bmap_surf.dat", skip_header=1, skip_footer=1)

fname = "//wsl.localhost/Ubuntu-24.04/home/fba/projects/MATINS-intel/out/2D/Bmap_surf.dat"

# Choose which snapshot to plot: 0 = initial snapshot, 1 = next, etc.
snapshot_index = 1

snapshots = []
current_snapshot = []

with open(fname, "r") as f:
    for line in f:
        parts = line.split()

        if not parts:
            continue

        if parts[0] == "snapshot":
            # Save the preceding snapshot, if one exists
            if current_snapshot:
                snapshots.append(np.asarray(current_snapshot, dtype=np.float64))
                current_snapshot = []

        elif parts[0] == "snapshot_end":
            if current_snapshot:
                snapshots.append(np.asarray(current_snapshot, dtype=np.float64))
                current_snapshot = []

        else:
            # Keep only rows containing exactly 17 numeric columns
            if len(parts) == 17:
                try:
                    current_snapshot.append([float(x) for x in parts])
                except ValueError:
                    pass

# Handle a final snapshot without a trailing snapshot_end marker
if current_snapshot:
    snapshots.append(np.asarray(current_snapshot, dtype=np.float64))

if snapshot_index >= len(snapshots):
    raise IndexError(
        f"Requested snapshot {snapshot_index}, "
        f"but only {len(snapshots)} snapshots were read."
    )

file = snapshots[snapshot_index]

theta = file[:,0]
phi = file[:,1]
br = file[:,2]
N = len(theta)

# Try a dipole:
#for i in range(0,len(theta),1):
#  br[i] = np.cos(theta[i])*np.sin(phi[i])


theta = math.pi/2 - theta
phi = np.asarray(phi) - math.pi

p = []
t = []
v = []

for i in range(0,N,1):
  if (phi[i] == -math.pi):
    p.append(math.pi)
    t.append(theta[i])
    v.append(br[i])

theta = np.concatenate([theta,np.asarray(t)])
phi   = np.concatenate([phi,np.asarray(p)])
br    = np.concatenate([br,np.asarray(v)])


Ncont=100

fig = plt.figure() 


ax = fig.add_subplot(221, projection='aitoff')
#ax.scatter(phi,theta,c=br, cmap=plt.cm.Spectral_r)
#ax.tricontour(phi, theta, br, Ncont, linewidths=0.5, cmap=plt.cm.Spectral_r)
ax.tricontourf(phi, theta, br, Ncont, cmap=plt.cm.Spectral_r)
ax.set_title("aitoff")
ax.set_xticks([])
ax.set_yticks([])
#ax.grid(True)

ax = fig.add_subplot(222, projection='hammer') 
ax.tricontour(phi, theta, br, Ncont, linewidths=0.5, cmap=plt.cm.Spectral_r)
ax.set_title("hammer")
ax.set_xticks([])
ax.set_yticks([])
#ax.grid(True) 

ax = fig.add_subplot(223, projection='lambert') 
ax.tricontour(phi, theta, br, Ncont, linewidths=0.5, cmap=plt.cm.Spectral_r)
ax.set_title("lambert")
ax.set_xticks([])
ax.set_yticks([])
#ax.grid(True) 

ax = fig.add_subplot(224, projection='mollweide') 
ax.tricontour(phi, theta, br, Ncont, linewidths=0.5, cmap=plt.cm.Spectral_r)
ax.set_title("Mollweide")
ax.set_xticks([])
ax.set_yticks([])
#ax.grid(True) 

#plt.xlabel('R.A.') 
#plt.ylabel(r'Decl.') 
plt.savefig("proyecciones.pdf",  bbox_inches="tight")
plt.show()
#plt.close()


