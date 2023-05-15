from visual import *

print """
Change the colors in a scene to shades of gray, which is what
scene.stereo = 'redblue' or scene.stereo = 'redcyan' needs
to be able to produce a stereo image viewable with red-blue
glasses.
"""

# Each of the grayscale conversions given here has disadvantages.
# Schemes 1 and 2 are standard schemes for converting a color scene
# to grayscale, but they lead to very dim grays in the VPython context.
# Scheme 3 concentrates solely on intensity, making a bright scene,
# but there is no difference in the appearance of objects with pure
# colors (such as red or blue), since these have the same intensity.

##You can run this directly (it has a test scene in it), or do this:
##
##from visual import *
##from grayscale import *
##
##scene.stereo = 'redblue' # or 'redcyan'
### make a color scene
##grayscale(scene)
### do animation, etc. in 3D using red-blue glasses

def grayscale(thisscene):
    GAMMA = 2.5
    for obj in thisscene.objects:
        if 'color' in obj.__members__:
            try:
                r,g,b = obj.color
            except:
                r,g,b = 1,1,1 # curve for example may have list of colors
                
##            Pick one of these schemes, or create your own:
                
##            s = 0.15*r+0.55*g+0.30*b # 1) a standard grayscale algorithm
##            s = min(1.0, 0.35*r+0.75*g*+0.50*b) # 2) like previous, but brighter
##            s = max(r,g,b) # 3) intensity only
            # The following conversion takes into account gamma correction:
            s = ( .299 * r**GAMMA + .587 * g**GAMMA + .114 * b**GAMMA ) ** (1/GAMMA)
            obj.color = (s,s,s)
            
if __name__ == '__main__': # for testing the module
    
    scene.stereo = 'redblue' # or 'redcyan'
    scene.stereodepth = 2
    
    darkgreen = (0,0.5,0)
    density = 0.7
    grey = (density,density,density)
    box(pos=(-1,0,0), color=color.green)
    box(pos=(1,-1,0), color=darkgreen)
    arrow(pos=(-0.5,0,0), axis=(1,-1,0), color=color.yellow)
    cylinder(pos=(-1,1.5,0), axis=(2,0,0), radius=0.4, color=grey)
    sphere(pos=(1,0.5,0), radius=0.5, color=color.red)
    sphere(pos=(-1,-1.4,0), radius=0.5, color=color.blue)
    cylinder(pos=(-2.5,-2,0), axis=(0,3,0), radius=0.3, color=color.cyan)
    box(pos=(2.5,0,0), size=(0.5,3,1), color=color.magenta)

    rate(1) # change to grayscale after 1 second
    scene.mouse.getclick()
    grayscale(scene)

    
    
