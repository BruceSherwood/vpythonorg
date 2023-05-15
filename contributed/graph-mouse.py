from visual.graph import *

oscillation = gdisplay(title='Test Plotting', xtitle='Time', ytitle='Response')

funct1 = gcurve(color=color.cyan)
funct2 = gvbars(color=color.red, delta=0.8)
funct3 = gdots(color=color.yellow)

for t in arange(-30, 76, 1):
    funct1.plot(pos=(t, 5.0+5.0*cos(-0.2*t)*exp(0.015*t)) )
    funct2.plot(pos=(t, 2.0+5.0*cos(-0.1*t)*exp(0.015*t)) )
    funct3.plot(pos=(t, 5.0*cos(-0.03*t)*exp(0.015*t)) )

showxy = label(display=oscillation.display, yoffset=10, opacity=1, visible=0)
gray = (0.5,0.5,0.5)
hor = curve(display=oscillation.display, color=gray, visible=0)
vert = curve(display=oscillation.display, color=gray, visible=0)
pos = None
while 1:
    rate(300)
    status = oscillation.display.mouse
    if status.events:
        m = status.getevent()
        if m.press == 'left':
            pos = status.pos
            showxy.visible = 1
            disp = oscillation.display
            xmax = disp.range.x
            ymax = disp.range.y
            xcenter = disp.center.x
            ycenter = disp.center.y
            hor.visible = 1
            vert.visible = 1
        elif m.release == 'left':
            pos = None
            showxy.visible = 0
            hor.visible = 0
            vert.visible = 0
    if pos and (pos is not status.pos):
        showxy.pos = pos = status.pos
        hor.pos = [(xcenter-xmax,pos.y),(xcenter+xmax,pos.y)]
        vert.pos = [(pos.x,ycenter-ymax),(pos.x,ycenter+ymax)]
        showxy.text = '%0.3g,%0.3g' % (status.pos.x,status.pos.y)
 
