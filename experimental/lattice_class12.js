////////////////////////////////////////////////////////////////////
//// class definition for square_lattice                           //
//// see Lattice_Motion.py for an example of how to use this class //
////////////////////////////////////////////////////////////////////

// wall made of particles that moveable particles can stick to??

function encode(x,y) { return x.toString()+':'+y.toString() }

function random_order(alist,num) {
    if (alist.length < num)
        throw new Error("can't pick more values than exist in a list")        
    var b = []
    var a = alist.slice(0)  // copy of alist
    while (b.length < num) {
        var rr = random()
        var jj = Math.floor(rr*a.length)
        b.push(a[jj])
        a.splice(jj,1)
    }
    return b
}

function square_lattice(args) {
    if (!(this instanceof square_lattice)) return new square_lattice(args)
    args = args || {}
    this.xmax = ('xmax' in args) ? args.xmax : 10
    this.ymax = ('ymax' in args) ? args.ymax : 10
    this.bc = ('bc' in args) ? args.bc : 'nonperiodic'
    this.barrierx = ('barrierx' in args) ? args.barrierx : null
    this.sites = []
    this.xy_to_site = {}
    this.particles = []
    this.clusters = []
    this.monitors = []
    this.entropy_monitors = []
    this.mon_display = graph({background:vec(0.9,0.9,0.9),
                              foreground:color.black, title:'density', align:'right',
                              width:500, height:200})
    this.ent_display = graph({background:vec(0.9,0.9,0.9),
                              foreground:color.black, title:'entropy', align:'right',
                              width:500, height:200})
    Lcanvas.center = vec((this.xmax-1)/2, (this.ymax-1)/2, 0)
    Lcanvas.range = Math.max((this.xmax),(this.ymax))/2 +1
    
    var count = 0
    var xx, yy
    for (yy=0; yy<this.ymax; yy++) {      // create tiny boxes at lattice sites
        for (xx=0; xx<this.xmax; xx++) {
            var a = vp_box({pos:vec(xx,yy,0), size:vec(0.1,0.1,0.1), occupant:null,
                         neighbors:[], color:color.black})
            this.sites.push(a)    // list of box objects
            this.xy_to_site[encode(xx,yy)] = a    // xy to box object
            count += 1
        }
    }
    var barrier_sites = []
    var i
    if (this.barrierx !== null) {
        if (this.ymax < 6) throw new Error('lattice y dimension too small for barrier')
        var brange = []
        for (i=0; i<Math.floor(this.ymax/2)-1; i++) brange.push(i)
        for (i=Math.floor(this.ymax/2)+1; i<this.ymax; i++) brange.push(i)
        for (i=0; i<brange.length; i++) {
            barrier_sites.push(encode(this.barrierx,i))
        }
        for (i=0; i<barrier_sites.length; i++) {
            var ss = barrier_sites[i]
            ss.size = vec(1,1,1)
        }
    }
    
    for (yy=0; yy<this.ymax; yy++) { // now list neighbors
        for (xx=0; xx<this.xmax; xx++) {
            var site = this.xy_to_site[encode(xx,yy)]   // sphere object
            var xlp = xx-1   // x to the left
            var xlnp = xx-1
            if (xlp < 0) {
                xlp = this.xmax-1
                xlnp = null
            }
            var xrp = xx+1     //x to the right
            var xrnp = xx+1
            if (xrp > this.xmax-1) {
                xrp = 0
                xrnp = null
            }
            var yup = yy+1     // y up
            var yunp = yy+1
            if (yup > this.ymax-1) {
                yup = 0
                yunp = null
            }
            var ydp = yy-1     // y down
            var ydnp = yy-1
            if (ydp < 0) {
                ydp = this.ymax-1
                ydnp = null
            }
            if (this.bc == 'periodic') { // periodic boundary conditions                   
                site.neighbors = [this.xy_to_site[encode(xlp,yy)], this.xy_to_site[encode(xrp,yy)],
                                 this.xy_to_site[encode(xx,yup)], this.xy_to_site[encode(xx,ydp)]]
            } else {   // walls, not periodic
                if (xlnp !== null)
                    site.neighbors.push(this.xy_to_site[encode(xlnp,yy)])
                if (xrnp !== null)
                    site.neighbors.push(this.xy_to_site[encode(xrnp,yy)])
                if (yunp !== null)
                    site.neighbors.push(this.xy_to_site[encode(xx,yunp)])            
                if (ydnp !== null)
                    site.neighbors.push(this.xy_to_site[encode(xx,ydnp)])
            }
            // remove barrier sites from neighbors
            for (i=0; i<barrier_sites.length; i++) {
                var ss = barrier_sites[i]
                if (ss in site.neighbors) { //site.neighbors.remove(ss)
                    var loc = site.neighbors.indexOf(ss)
                    site.neighbors.splice(loc,1)
                }
            }
        }
        this.count = count
    }

    vp_box({pos:vec((this.xmax-1)/2, (this.ymax-1)/2, -1), size:vec(this.xmax+1,this.ymax+1, 0.5),
         color:Lcanvas.background, shininess:0})
}

square_lattice.prototype.show_neighbors = function show_neighbors(xxi,xxf,yyi,yyf) { // for debugging
    var nn
    for (var xx=xxi; xx<xxf; xx++) {
        for (var yy=yyi; yy<yyf; yy++) {
            var site = this.xy_to_site[encode(xx,yy)]
            for (var i in site.neighbors) {
                nn = site.neighbors[i]
                nn.color = color.red
                nn.size = vec(1.0,1.0,1.0)
            }
            //sleep(1, wait)
            for (var i in site.neighbors) {
                nn = site.neighbors[i]
                nn.color = color.black
                nn.size = vec(0.1,0.1,0.1)
            }
        }
    }
}

square_lattice.prototype.make_particles = function make_particles(number,xi,xf,yi,yf, pcolor, trail, shape) {
    var ret = 1000
    var sitelist = []
    var nplaces = (xf-xi)*(yf-yi)
    var msg
    if (number > nplaces) {
        msg = 'too many particles for ' + nplaces.toString() + ' lattice sites'
        throw new Error(msg)
        return
    } else if (number < 1) {
        msg = number.toString() + ' is not a valid number of particles'
        throw new Error(msg)
        return
    }
    for (var xx=xi; xx<xf; xx++) {
        for (var yy=yi; yy<yf; yy++) {
            sitelist.push(this.xy_to_site[encode(xx,yy)])
        }
    }
    
    var a
    var ro = random_order(sitelist,number)
    for (var i=0; i<ro.length; i++) {
        var loc = ro[i]
        if (shape == 'sphere') {
            a = vp_sphere({pos:loc.pos, size:vec(.8,.8,.8), color:pcolor, make_trail:trail, retain:ret, interval:1})
        } else {
            a = vp_box({pos:loc.pos, size:vec(.8,.8,.8), color:pcolor, make_trail:trail, retain:ret, interval:1})
        }
        loc.occupant = a
        this.particles.push(a)
        this.clusters.push(a)
    }
}            

square_lattice.prototype.get_sites = function get_sites(xi,xf,yi,yf) {
    var ssites = []
    var xx, yy
    try {
        for (xx=xi; xx<xf; xx++) {
            for (yy=yi; yy<yf; yy++) {
                ssites.push(this.xy_to_site[encode(xx,yy)])
            }
        }
    } catch(err) {
        print(xx,yy)
        throw new Error('invalid coordinate range')
    }
    return ssites
}
            
square_lattice.prototype.make_monitor = function make_monitor(xi,xf,yi,yf, quantity) {
    if (this.monitors.length > 3)
        throw new Error('too many monitors -- maximum 3')
    var msites = this.get_sites(xi,xf,yi,yf)
    var loc =  vec(xf,yf,0)
    var cols = [color.blue, color.red, vec(0.7,0,0.7), color.black ]
    var gcolor = cols[this.monitors.length]
    var vertices = [xi,xf,yi,yf]
    var mon = particle_monitor(msites, vertices, loc, this.mon_display, gcolor, quantity)
    this.monitors.push(mon)
    return mon
}

square_lattice.prototype.make_entropy_monitor = function make_entropy_monitor(xi,xf,yi,yf) {
    if (this.entropy_monitors.length > 1)
        throw new Error('too many entropy monitors -- maximum 1')
    if (this.bc !== 'nonperiodic')
        throw new Error('entropy monitors require nonperiodic boundary conditions')
    var msites = this.get_sites(xi,xf,yi,yf)
    var cols = [color.orange, color.green]
    var gcolor = cols[this.entropy_monitors.length]
    var vertices = [xi,xf,yi,yf]
    var mon = entropy_monitor(msites, vertices, this.ent_display, gcolor)
    this.entropy_monitors.push(mon)
    return mon
}
       
square_lattice.prototype.random_step = function random_step() { // loop thru particles in random order
    var plist = random_order(this.particles, this.particles.length)
    var i
    for (i=0; i<plist.length; i++) {
        var pp = plist[i]
        var site = this.xy_to_site[encode(pp.pos.x, pp.pos.y)]
        var N = random_order(site.neighbors,1)[0]
        if (N.occupant === null) {
            pp.pos = N.pos
            site.occupant = null
            N.occupant = pp
        }
    }
    var mm
    for (i=0; i<this.monitors.length; i++) {
        mm = this.monitors[i]
        mm.update()
    }
    for (i=0; i<this.entropy_monitors.length; i++) {
        mm = this.entropy_monitors[i]
        mm.update()
    }
}

square_lattice.prototype.log_arrangements = function log_arrangements() {
    var np = this.particles.length
    if (np < 1) return 1
    var x0 = this.xmax
    var y0 = this.ymax
    var x1 = 0
    var y1 = 0   
    for (var i in this.particles) { // find current volume of gas
        var pp = this.particles[i]
        if (pp.x < x0) x0 = pp.x
        if (pp.y < y0) y0 = pp.y
        if (pp.x > x1) x1 = pp.x
        if (pp.y > y1) y1 = pp.y
    }
    var available_sites = (x1-x0)*(y1-y0)
    if (available_sites < 0)    // with np > 0 should never happen
        throw new Error('volume undefined')
    var comb = combin((available_sites+np-1), np)
    return Math.log(comb)
}
    
// end of square_lattice class

function particle_monitor(args) {
    if (!(this instanceof particle_monitor)) return new particle_monitor(args)
//    def __init__(self, sites, vertices, location, gdisp, gcolor, quantity):
        this.sites = arguments[0]     // a list of the sites included
        this.vertices = arguments[1]  // a list of vertices (3D vectors)
        var location = arguments[2]
        this.gd = arguments[3]
        this.color = arguments[4]
        this.quantity = arguments[5]
        
        this.pcount = 0
        var dx = 0.3
        var xi = this.vertices[0]
        var xf = this.vertices[1]
        var yi = this.vertices[2]
        var yf = this.vertices[3]
        var corners = [vec(xi-dx,yi-dx,0), vec(xf+dx,yi-dx,0), vec(xf+dx,yf+dx,0),
            vec(xi-dx,yf+dx,0), vec(xi-dx,yi-dx,0)]

        this.ticks = 0          // total number of data points summed
        this.densitysum = 0     // cumulative sum
        this.tag = label({pos:location, text:'0', color:this.color, linecolor:this.color})
        this.border = curve({pos:this.corners, radius:0.05, color:this.color})
        this.graf = gcurve({color:this.color, graph:this.gd})
        this.last100 = []
}
        
particle_monitor.prototype.update = function update() {
    this.ticks += 1
    var np = 0
    var xmx = this.vertices[0]   // set min, max for finding volume
    var ymx = this.vertices[2]
    var xmn = this.vertices[1]
    var ymn = this.vertices[3]
    for (var i in this.sites) {
        var ss = this.sites[i]
        if (ss.occupant !== null) np++
    }
    var d = np/this.sites.length
    this.densitysum += d
    this.tag.text = np.toString()     // show number of particles
    if (this.last100.length > 99) // only keep last 100 points - moving average
        this.last100.pop()       // remove first point
    this.last100.push(d)      // add current point
    var total = 0
    for (var i in this.last100) total += this.last100[i]
    var avg = total/this.last100.length      
    if (this.pcount % 100 === 0) {
        this.pcount = 0
        if (this.quantity == 'density') {
            this.graf.plot(this.ticks, d)
        } else if (this.quantity == 'average_density') {
            this.graf.plot(this.ticks, avg)
        } else if (this.quantity == 'average_density_1') {
            this.graf.plot(this.ticks,this.densitysum/this.ticks)  // total cumulative
        }
    }
} // end of particle_monitor class

function entropy_monitor(args) {
    if (!(this instanceof entropy_monitor)) return new entropy_monitor(args)
//    def __init__(self, sites, vertices, gdisp, gcolor):
        this.sites = arguments[0]     // a list of the sites included
        this.vertices = arguments[1]
        this.gd = arguments[2]
        this.color = arguments[3]
        
        this.pcount = 0
        var dx = 0.3
        var xi = this.vertices[0]
        var xf = this.vertices[1]
        var yi = this.vertices[2]
        var yf = this.vertices[3]
        this.corners = [vec(xi-dx,yi-dx,0), vec(xf+dx,yi-dx,0), vec(xf+dx,yf+dx,0),
            vec(xi-dx,yf+dx,0), vec(xi-dx,yi-dx,0)]
        this.ticks = 0          // total number of data points summed
        this.border = curve({pos:this.corners, radius:0.05, color:this.color})
        this.graf = gcurve({color:this.color, graph:this.gd})
}

entropy_monitor.prototype.update = function update() {
    this.ticks += 1
    var np = 0
    var xmx = this.vertices[0]   // set min, max for finding volume
    var ymx = this.vertices[2]
    var xmn = this.vertices[1]
    var ymn = this.vertices[3]
    for (var i in this.sites) {
        var ss = this.sites[i]
        if (ss.occupant !== null) {
            np += 1
            if (ss.pos.x < xmn) xmn = ss.pos.x
            if (ss.pos.x > xmx) xmx = ss.pos.x
            if (ss.pos.y < ymn) ymn = ss.pos.y
            if (ss.pos.y > ymx) ymx = ss.pos.y
        }
    }
    var vol = (xmx-xmn+1)*(ymx-ymn+1)   // volume currently occupied
    if (np < 0) throw new Error('np < 0')
    if (vol <= 0) throw new Error('vol <=0, vol='+vol.toString()+', np='+np.toString())
//        ways = combin((np+vol),np)
//        npp = max(np,0)
    var ways = combin(vol,np)
    var S = Math.log(ways)   
    if (this.pcount % 100 === 0) {
        this.pcount = 0
        this.graf.plot(this.ticks,S)
    }
} // end of entropy_monitor class

function random_step(alattice) { alattice.random_step() }

function make_particles(args) {                
    args = args || {}
    var lattice = ('lattice' in args) ? args.lattice : null
    var number = ('number' in args) ? args.number : 2
    var xi = ('xi' in args) ? args.xi : 0
    var xf = ('xf' in args) ? args.xf : 10
    var yi = ('yi' in args) ? args.yi : 0
    var yf = ('yf' in args) ? args.yf : 10
    var color = ('color' in args) ? args.color : color.yellow
    var trail = ('trail' in args) ? args.trail : false
    var shape = ('shape' in args) ? args.shape : 'sphere'
    lattice.make_particles(number, xi, xf, yi, yf, color, trail, shape)
}

function monitor(args) {            
    args = args || {}
    var lattice = ('lattice' in args) ? args.lattice : null
    var ymax = ('ymax' in args) ? args.ymax : null
    var xi = ('xi' in args) ? args.xi : 0
    var xf = ('xf' in args) ? args.xf : 2
    var yi = ('yi' in args) ? args.yi : 0
    var yf = ('yf' in args) ? args.yf : 2
    var quantity = ('quantity' in args) ? args.quantity : 'average_density'    
    
    if (xf < xi || yf < yi)
        throw new Error('(xi,yi) must be lower left corner')
    var mm
    if (quantity == 'entropy') mm = lattice.make_entropy_monitor(xi,xf,yi,yf)
    else mm = lattice.make_monitor(xi,xf,yi,yf, quantity)
    return mm
}

var Lcanvas

function setup_screen(args) {
    args = args || {}
    Lcanvas = ('canvas' in args) ? args.canvas : scene  // oddly, scene is undefined
    Lcanvas.width = ('width' in args) ? args.width : 400
    Lcanvas.height = ('height' in args) ? args.height : 400
    Lcanvas.background = ('background' in args) ? args.background : vec(0.9,0.9,0.9)
    Lcanvas.align = 'left'
    Lcanvas.title = 'Square Lattice'
}