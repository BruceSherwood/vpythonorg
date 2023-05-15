#!/usr/bin/env python
# To use:
#       python setup.py install
#

import os, glob

from distutils.core import setup, Extension
from distutils.command.build_py import build_py
from distutils.command.install_lib import install_lib

pkgname="visual"
src_dir="cvisual"
extra_compile_args = ['/D', "WIN32", '/D', "_WINDOWS", '/D', "_MBCS"
                     ,'/D', "_USRDLL", '/D', "CVISUAL_EXPORTS",
                     '/D', "VECTOR_EXPORTS"]
extra_link_args=[]
demo_dir=os.path.join(pkgname,'demos')
idle_dir=os.path.join(pkgname,'idle_VPython')
packages = [pkgname,demo_dir,idle_dir]
##pkg_dir= {"visual": ".",demo_dir:"demos"}

txt_files = ['LICENSE.txt','README.txt',os.path.join('docs','visual.html')]
doc_dir = os.path.join(pkgname,"docs","visual")
docs_files = glob.glob1(doc_dir,"*.html")
docs_files += glob.glob1(doc_dir,"*.gif")
docs_files += glob.glob1(doc_dir,"*.txt")
docs_files += glob.glob1(doc_dir,"*.css")
icon_dir = os.path.join(pkgname,"docs","icons")
icon_files = glob.glob1(icon_dir,"*.gif")
idle_txtfiles = glob.glob1(idle_dir,"*.txt")
idle_txtfiles += glob.glob1(idle_dir,"*.pyw")

for docs in docs_files:
##    txt_files.append(os.path.join(os.path.join('docs','visual',docs)))
    txt_files.append(os.path.join('docs','visual',docs))

for icon in icon_files:
##    txt_files.append(os.path.join(os.path.join('docs','icons',docs)))
    txt_files.append(os.path.join('docs','icons',icon))

for idle in idle_txtfiles:
    txt_files.append(os.path.join('idle_VPython',idle))

src = [
	os.path.join(pkgname,src_dir,"CXX","src","cxx_extensions.cxx"),
	os.path.join(pkgname,src_dir,"CXX","src","cxxextensions.c"),
	os.path.join(pkgname,src_dir,"CXX","src","cxxsupport.cxx"),
	os.path.join(pkgname,src_dir,"arrow.cpp"),
	os.path.join(pkgname,src_dir,"box.cpp"),
	os.path.join(pkgname,src_dir,"cone.cpp"),
	os.path.join(pkgname,src_dir,"convex.cpp"),
	os.path.join(pkgname,src_dir,"curve.cpp"),
	os.path.join(pkgname,src_dir,"cylinder.cpp"),
	os.path.join(pkgname,src_dir,"faceset.cpp"),
	os.path.join(pkgname,src_dir,"frame.cpp"),
	os.path.join(pkgname,src_dir,"label.cpp"),
	os.path.join(pkgname,src_dir,"ring.cpp"),
	os.path.join(pkgname,src_dir,"sphere.cpp"),
	os.path.join(pkgname,src_dir,"arrprim.cpp"),
	os.path.join(pkgname,src_dir,"color.cpp"),
	os.path.join(pkgname,src_dir,"cvisual.cpp"),
	os.path.join(pkgname,src_dir,"display.cpp"),
	os.path.join(pkgname,src_dir,"displaylist.cpp"),
	os.path.join(pkgname,src_dir,"gldevice.cpp"),
	os.path.join(pkgname,src_dir,"kbobject.cpp"),
	os.path.join(pkgname,src_dir,"light.cpp"),
	os.path.join(pkgname,src_dir,"mouseobject.cpp"),
	os.path.join(pkgname,src_dir,"platwin.cpp"),
	os.path.join(pkgname,src_dir,"prim.cpp"),
	os.path.join(pkgname,src_dir,"pvector.cpp"),
	os.path.join(pkgname,src_dir,"rate.cpp"),
	os.path.join(pkgname,src_dir,"tmatrix.cpp"),
	os.path.join(pkgname,src_dir,"vcache.cpp"),
	os.path.join(pkgname,src_dir,"wgl.cpp")
	]

incl_dir=[os.path.join(pkgname,src_dir,"CXX","Include")]

class IDLE_Builder(build_py):
    def get_plain_outfile(self, build_dir, package, file):
        # like get_module_outfile, but does not append .py
        outfile_path = [build_dir] + list(package) + [file]
        return apply(os.path.join, outfile_path)

    def run(self):
        # Copies all .py files, then also copies the txt and gif files
        build_py.run(self)
        for name in txt_files:
            outfile = self.get_plain_outfile(self.build_lib, [pkgname], name)
            dir = os.path.dirname(outfile)
            self.mkpath(dir)
            self.copy_file(os.path.join(pkgname, name), outfile,
                           preserve_mode = 0)
            
    def get_outputs(self, include_bytecode=1):
        # returns the built files
        outputs = build_py.get_outputs(self, include_bytecode)
        if not include_bytecode:
            return outputs
        for name in txt_files:
            filename = self.get_plain_outfile(self.build_lib, [pkgname], name)
            outputs.append(filename)

# Arghhh. install_lib thinks that all files returned from build_py's
# get_outputs are bytecode files

#class IDLE_Installer(install_lib):
#    def _bytecode_filenames(self, files):
#        files = [n for n in files if n.endswith('.py')]
#        return install_lib._bytecode_filenames(self, files)


pyd_dir=os.path.join(pkgname,src_dir)
setup (name = "VPython",
       packages = packages,
       version="2002-12-31",
       description="VPython - 3D Programming for Ordinary Mortals",
       author="David Scherer",
       url="http://www.vpython.org",
       license = "see LICENSE.txt",
       long_description = """VPython - 3D Programming for Ordinary Mortals.
       Python itself does not provide graphics output. The Tk
       graphics library can be used to create 2D graphics, but
       it is difficult to use. While a sophomore in computer
       science at Carnegie Mellon University, David Scherer
       created a 3D graphics module for Python, called "Visual,"
       that is exceptionally easy to use. A program can create
       3D objects (such as spheres, curves, etc.) and position
       them in 3D space. Visual, running in a separate thread,
       automatically updates a 3D scene many times per second,
       to reflect the current positions of the objects. The
       programmer does not need to deal with display management,
       but can focus on the computational aspects of the program.
       The user can navigate in the 3D scene by using the mouse
       to zoom and rotate while the program is running. Visual
       supports full vector algebra.""",
       include_dirs = incl_dir,
       cmdclass = {'build_py':IDLE_Builder},
       ext_modules = [Extension(pkgname+'.'+src_dir,src,
       extra_compile_args = extra_compile_args,
       extra_link_args = extra_link_args,
       libraries = ["opengl32", "user32", "gdi32", "glu32"])
                     ]
       )
