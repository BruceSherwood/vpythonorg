from visual import *

# This program by Bruce Sherwood (Sept. 2010) turns off the default user spin and zoom
# and handles these functions itself. This gives more control to the program and addresses
# the problem that at the time of writing, Visual has a hidden user scaling variable that
# makes it impossible to force the camera position by setting range, if the user has
# already zoomed using the mouse.

# As a demonstration of this, press "f" or "g" to change the range, before or after zooming.

scene.userzoom = False
scene.userspin = False
scene.range = 2
print scene.range
box(color=color.red)
arrow(pos=(0,.5,0), axis=(0,1,0), color=color.green)
arrow(pos=(.5,0,0), axis=(1,0,0), color=color.cyan)
zoom = False
spin = False
rangemin = .5
rangemax = 20
while True:
    rate(50)
    if scene.kb.keys:
        k = scene.kb.getkey()
        if k == 'f':
            scene.range = 5
        elif k == 'g':
            scene.range = 3
    elif scene.mouse.events:
        m = scene.mouse.getevent()
        if m.drag == 'middle':
            zoom = True
            lasty = m.pos.y
        elif m.drop == 'middle':
            zoom = False
        elif m.drag == 'right':
            spin = True
            lastray = scene.mouse.ray
        elif m.drop == 'right':
            spin = False
    elif zoom:
        newy = scene.mouse.pos.y
        if newy != lasty:
            distance = (scene.center-scene.mouse.camera).mag
            scaling = 10**((lasty-newy)/distance)
            newrange = scaling*scene.range.y
            if rangemin < newrange < rangemax:
                scene.range = newrange
                lasty = scaling*newy
    elif spin:
        newray = scene.mouse.ray
        dray = newray-lastray
        right = scene.forward.cross(scene.up).norm() # unit vector to the right
        up = right.cross(scene.forward).norm() # unit vector upward
        anglex = -4*arcsin(dray.dot(right))
        newforward = vector(scene.forward)
        newforward = rotate(newforward, angle=anglex, axis=scene.up)
        newray = rotate(newray, angle=anglex, axis=scene.up)
        angley = 4*arcsin(dray.dot(up))
        maxangle = scene.up.diff_angle(newforward)
        if not (angley >= maxangle or angley <= maxangle-pi):
            newforward = rotate(newforward, angle=angley, axis=right)
            newray = rotate(newray, angle=angley, axis=right)
        scene.forward = newforward
        lastray = newray
