# -*- coding: utf-8 -*-
"""
Use Paraview to generate the .png bitmap image files of modes from 3d .vtp files

Paraview must be installed, and the script should be run with the `pvpython`
Python interpreter embedded into Paraview.

@author: dap124
"""

from paraview.simple import *
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

reader = XMLPolyDataReader(FileName=input_file)
view = servermanager.CreateRenderView()


# set the camera position and angle
view.CameraViewUp = [0, 1, 0]
view.CameraFocalPoint = [0, 0, 0.5]
#view.CameraViewAngle = 90
view.CameraPosition = [-3.5,1,3]
view.OrientationAxesVisibility = 0
zoom_level = 2

view.ViewSize = [800, 400] # [width, height] 

# allow the plotted quantity to be specified on command line
if len(sys.argv) > 4:
    scalar_name = sys.argv[3]
    vector_name = sys.argv[4]
else:
    scalar_name = "rho_e_imag"
    vector_name = "J_imag"

#set the background color
view.Background = [1,1,1]  # white

repr = servermanager.CreateRepresentation(reader, view)
repr.Representation = "Surface"
reader.UpdatePipeline()

dataInfo = reader.GetDataInformation()

# The scalar surface charges are represented as cell data
cellDataInfo = dataInfo.GetCellDataInformation()
chargeInfo = cellDataInfo.GetArrayInformation(scalar_name)

range = chargeInfo.GetComponentRange(0)
lut = servermanager.rendering.PVLookupTable()
                  
lut.RGBPoints  = [range[0], 0.231373, 0.298039, 0.752941,
                  range[1], 0.705882, 0.156863, 0.14902]

repr.LookupTable = lut
repr.ColorArrayName = ['CELLS', scalar_name]
repr.UpdatePipeline()

currentInfo = cellDataInfo.GetArrayInformation(vector_name)
 
gl = Glyph()
gl.Vectors = ['CELLS', vector_name]
gl.GlyphType = 'Cone'
gl.ScaleFactor = 2e-8
 
repr = servermanager.CreateRepresentation(gl, view)
gl.UpdatePipeline()

# zooming must be done after an initial render has worked out automatic camera placement
Render(view)
cam = view.GetActiveCamera()
cam.Zoom(zoom_level)


Render(view)
SaveScreenshot(output_file, view, magnification=2)
