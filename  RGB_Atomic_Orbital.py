from vpython import *
import math

scene = canvas(title="RGB Atomic Orbital",
               width=900, height=700,
               background=vector(0.01,0.01,0.04))

scene.autoscale = False
scene.range = 4

# Glowing nucleus
sphere(pos=vector(0,0,0), radius=.35,
       color=vector(1,.1,.5), emissive=True)

# Three 3D orbital rings
rings = []
for axis in [vector(1,0,0), vector(0,1,0), vector(0,0,1)]:
    rings.append(curve(color=color.cyan, radius=.025))

# RGB orbiting particles
atoms = []
for i in range(3):
    atoms.append(sphere(radius=.13, emissive=True))

t = 0

while True:
    rate(60)

    for i, ring in enumerate(rings):
        ring.clear()
        for j in range(101):
            a = j*2*pi/100
            p = vector(2*math.cos(a), 2*math.sin(a), 0)
            ring.append(pos=rotate(p, angle=i*pi/3,
                                   axis=vector(1,1,1)),
                        color=vector(
                            .5+.5*math.sin(t+i),
                            .5+.5*math.sin(t+i+2),
                            .5+.5*math.sin(t+i+4)))

    for i, atom in enumerate(atoms):
        a = t*2+i*2*pi/3
        atom.pos = vector(2*math.cos(a),
                          math.sin(a*2),
                          2*math.sin(a))
        atom.color = vector(
            .5+.5*math.sin(t+i),
            .5+.5*math.sin(t+i+2),
            .5+.5*math.sin(t+i+4))

    t += .035