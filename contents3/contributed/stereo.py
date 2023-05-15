from visual import *

# Bruce Sherwood, December 2002

print """
Display stereo pair of graphics windows.
Look "wall-eyed" to see true 3D. This involves relaxing the eyes as
though looking far away, yet focusing on the screen.  
"""

x = 300
y = 400
w = 200
h = 200
scene.x=300
scene.y=400
scene.width=200
scene.height=200
scene.stereo = 'passive' # double-width window containing left and right views

b1=box(pos=(-1,0,0), color=color.red)
b2=box(pos=(1,-1,0), color=color.cyan)
a1=arrow(pos=(-0.5,0,0), axis=(1,-1,0), color=color.yellow)

# For historical interest, here is how this program was written
# before the availability of true stereo:

##def copyobjects(scene1,scene2):
##    # Copy all Visual objects from scene1 into scene2
##    scene2.select()
##    for obj in scene1.objects:
##        newobj=obj.__class__() # create object in scene2
##        for member in obj.__members__:
##            if member == 'display': continue # avoid putting into scene1
##            setattr(newobj,member,getattr(obj,member))
##
##x = 300
##y = 400
##w = 200
##h = 200
### Interocular angle in radians (estimate 8 cm separation at 55 cm distance):
##eyeangle = 8./55. 
##left = display(x=x, y=y, width=w, height=h)
##right = display(x=x+w, y=y, width=w, height=h)
##
##left.select() # Create objects in "left" display
##b1=box(pos=(-1,0,0), color=color.red)
##b2=box(pos=(1,-1,0), color=color.cyan)
##a1=arrow(pos=(-0.5,0,0), axis=(1,-1,0), color=color.yellow)
##
##copyobjects(left,right) # Copy objects into "right" display
##
### Continually force viewing angle of left and right windows
###   to differ by an angle corresponding to the eye separation:
##while 1:
##    right.up = left.up
##    leftforward = left.center-left.mouse.camera
##    right.forward = rotate(leftforward, angle=eyeangle, axis=left.up)
