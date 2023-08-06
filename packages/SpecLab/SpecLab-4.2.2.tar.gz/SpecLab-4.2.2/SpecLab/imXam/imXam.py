#!/usr/bin/env python

# export QT_QPA_PLATFORM=offscreen
#  https://stackoverflow.com/questions/68036484/qt6-qt-qpa-plugin-could-not-load-the-qt-platform-plugin-xcb-in-even-thou/68058308#68058308

import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from pyqtgraph.Point import Point
from astropy.io import fits
import astropy.io.ascii as ascii
from scipy.interpolate import RegularGridInterpolator
import matplotlib
import matplotlib.pyplot as plt
from photutils.aperture import CircularAperture, CircularAnnulus
from photutils.aperture import aperture_photometry
from matplotlib.backend_bases import key_press_handler
from photutils.centroids import centroid_2dg
import sys
import scipy, scipy.optimize
import matplotlib.pyplot as plt
import os
from matplotlib.patches import Circle
import plotly.graph_objects as go
#os.environ['QT_QPA_PLATFORM'] = 'offscreen'

#export QT_DEBUG_PLUGINS=1

# updates 2023 (v4.0.5)
##  renamed from imxam.py to imXam.py so as to not interfere with astropys dist
##  replaced mpld3 with plotly
##  cubic spline added
##  g, x, t keys all work for KOSMOS spectra as long as -dispax 2 is set
##  cube_val should have a value with a single .fits is read in and there is a datacube.
##  ext now refers to an extension of a fits file.
##  Added IRAFs zscale algorithm as default.
##  Added image scaling printout.
##  Changed l2 to irisras, and irisras now takes a value corresponding to the image to plot starting from 0, same for value following -cube
##  Added keyword scube so now can subtract a preflare image if -cube is used.  Check 'threshold' key 'T' ...
##  Added such that lastheader.txt is automatically opened from 'H' key use.  
##  Many more things:  ....

## see KNOWN_ISSUES file 

# 7/11/23:  SpecLab_config.py, this copies over several routines in PyQtGraph so that they work with imXam functionality.
# ======================

import site

your_site_packages_location = site.getsitepackages()

imexam_path = your_site_packages_location[0]+'/SpecLab/aux/param_files/' # this is default location of default imXam_param.dat

import SpecLab.gen.SpecLabFunctions as SpecLab
plotly_hist_color= '#000000'

def findind(array,value):
    ''' findind(array, value)'''
    idx = (np.abs(array-value)).argmin()
    return idx

def prep_pmesh(z):
# z is an irregular grid and must be at cell boundaries for pcolormesh (therefore make an array that is ndep + 1 dimensions.)
    ndep = len(z)
    midz = (z[1:len(z)] + z[0:len(z)-1])/2.
    newz = np.insert(midz, 0, z[0] + (z[0]-midz[0]))
    ndep2=len(newz)
    z_bdry = np.append(newz, z[ndep-1] + (z[ndep-1]-midz[ndep-2]))
    return z_bdry

def find_zscale(imsel): # imsel should be two dimensional array
   # Following: https://js9.si.edu/js9/plugins/help/scalecontrols.html
    imflt = imsel.flatten()
    sinds = np.argsort(imflt)
    imsrt = imflt[sinds]
    notbad = (imsrt > -80) # select only those greater than -200 to clean IRIS SJI images.
    imclean = imsrt[notbad]
    med = np.median(imclean)
    midpoint = findind(imclean, med)
    iii = np.linspace(0,len(imclean)-1,len(imclean))
    xtofit = iii - midpoint
    coeffsz = np.polyfit(xtofit, imclean, 1)
    npoints = len(imclean)
    z1_zscale = imclean[midpoint] + (coeffsz[0] / 1.0) * (1.0 - midpoint)
    z2_zscale = imclean[midpoint] + (coeffsz[0] / 1.0) * (npoints - midpoint)
    return z1_zscale, z2_zscale



print('======================================================')
print('======================================================')
print('imXam: v4.2.2 (July 12, 2023)')
print(' To shut down gui, type q into terminal, type h for interactive commands, use middle mouse wheel to zoom in and out')
print(' You may have to click on gui with left mouse button in order to use interactive commands')
print(' To get a list of command-line options, type imXam.py -h from a terminal.')
print('======================================================')
print('imXam.py located in ',your_site_packages_location[0]+'/SpecLab/imXam/')
print(' and .../anaconda3/envs/<your_env_name>/bin/')
print('Default param files located in ',your_site_packages_location[0]+'/SpecLab/aux/param_files/')
print('--> To edit imXam_param.dat with vim, type epar_imXam.py from a terminal.')
print('======================================================')
print('======================================================')

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
parser = ArgumentParser(formatter_class=RawTextHelpFormatter)

parser.add_argument("-f", "--file", dest="filename", help="FITS file name to examine")
parser.add_argument("-z1", "--z1", dest="z1", help="lower ADU value for display. Default is using IRAFs zscale algorithm.")
parser.add_argument("-z2", "--z2", dest="z2", help="upper ADU value for display. Default is using IRAFs zscale algorithm.")
parser.add_argument("-b", "--bias", dest="biasname", help="Bias (or Dark) filename to subtract (or any other fits image you want to subtract).  Can click ROI to set a rectangle for a quick aperture sum (with no background subtraction).")
parser.add_argument("-dispax", "--dispax", dest="dispaxis", help="Dispersion axis:  1 for along x (e.g., DIS), 2 for along y (e.g., KOSMOS) ",default='1')
parser.add_argument("-hcut", "--horizcut", dest="hcut", help="Method for horizontal cuts (simple,interp) shown in lower left window. Default is simple. ",default='simple')
parser.add_argument("-vcut", "--vertcut", dest="vcut", help="Method for vertical cuts (simple,interp) shown in lower right window. Default is simple.",default='simple')
parser.add_argument("-ext", "--extension", dest="uextension", help="Extension number of multi-extension FITS file. Default is 0.", default='0')
parser.add_argument("-repl", "--replace", dest="replace", help="Replace NaN, -Inf, and Inf values of array with value specified after -repl.  Must be > -999 or doesn't replace.", default=-9999.)
parser.add_argument("-irisras", "--iris_lvl2", dest="lvl2", help='IRIS Level 2 spec raster;  the integer after -irasras will be the image to plot starting from 0')
parser.add_argument("-cube", "--datacube", dest="cube", help='data dube FITS file with time (or another quantity such as wavelength) along one of the dimensions;  time (or wavelength) dimension is the one that is the 0th dimension [nt, ny, nx] if reading in with astropy.io.fits.getdata;  the integer after -cube will be the extension starting from 0 to plot')
parser.add_argument("-scube", "--sdatacube", dest="scube", help='3rd axis image to subtract of data cube; default is last index',default=-1)
parser.add_argument("-tlim1", "--tlim1", dest="tlim1", help='starting index of cube to plot ',default=0)
parser.add_argument("-tlim2", "--tlim2", dest="tlim2", help='ending index of cube to plot',default=-1)
parser.add_argument("-hsg", "--hsg", dest="hsg",help='if any integer, then reads in cal.xxx.fits FITS file with first extension a [nrast, ny, nx] data cube from Adams HSG reduction pipeline. Does fits.getdata(file,1).  There are many other extensions in cal.xxx.fits so this is why there is a separate -hsg trigger;  NOTE:  -cube should be used for .other fits files with datacubes read in through fits.getdata(file).')
parser.add_argument("-i", "--param_file", dest="param",help='You can use a custom parameter file by specifying its FULL path; default is the one in .../site-packages/SpecLab/aux/param_files/ (default:  imXam_param.dat)',default='imXam_param.dat')
parser.add_argument("-ec", "--", dest="echelle",help='(0 or 1) if 1, loads in default imXam_param_ARCES.dat with some reasonable parameters for inspecting echelle, is the one in .../site-packages/SpecLab/aux/param_files/ (default: 0)',default=0)

        

from matplotlib.colors import LinearSegmentedColormap
# paul tol color blind safe colors:https://personal.sron.nl/~pault/
from matplotlib import cm # this can be interpolated!
clrs = [  '#C3A8D1', '#B58FC2','#A778B4',\
        '#9B62A7', '#8C4E99', '#6F4C9B', '#6059A9', \
        '#5568B8', '#4E79C5', '#4D8AC6', '#4E96BC', '#549EB3', \
        '#59A5A9', '#60AB9E', '#69B190', '#77B77D', '#8CBC68', \
        '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C', '#E49C39', \
        '#E78C35', '#E67932', '#E4632D', '#DF4828', '#DA2222', \
        '#B8221E', '#95211B', '#721E17', '#521A13']  # bad data grey is 102,102,102

# Can also flip color s cheme if you prefer the opposite:   clrs = np.flip(clrs)
cmap_name = 'smrb'  # smooth rainbow.
usermap = LinearSegmentedColormap.from_list(cmap_name, (clrs), N=100)
rcol = (220,5,12)
pcol = (238, 102,119)
bl_col = (25./255.,101./255.,176./255.)
red_col = (220./255., 5./255., 12./255.)
gr_col = (144./255., 201./255., 135./255.)
ltpur = (174,118,163)
BR_red_col = (238.0/255., 102./255., 119./255.)
BR_pur_col = (170./255., 51./255., 119./255.)
BR_gr_col = (34./255., 136./255., 51./255.)
BR_blue_col = (102./255., 204./255., 238./255.)
BR_yl_col = (204./255., 187./255., 68./255.)
BR_nav_col = (68./255., 119./255., 170./255.)
BR_red_col_HEX = "#EE6677"

boxx0= []
boxy0=[]
boxx1=[]
boxy1=[]
box_mean =[]
box_med = []
box_max = []
box_min = []
box_std = []

QtCore.pyqtRemoveInputHook()

args = parser.parse_args()

ifile = args.filename

param_file = args.param

ec_param = int(args.echelle)

if param_file == 'imXam_param.dat':
    if ec_param == 0:
        full_imexam_parm_path = imexam_path+param_file
        print('Reading default imXam_param.dat')
    else:
        full_imexam_parm_path = imexam_path+'imXam_param_ARCES.dat'
        print('Reading default imXam_param_ARCES.dat')
else:
    full_imexam_parm_path = param_file

uparm = ascii.read(full_imexam_parm_path)  # Can edit this parameter file
#user_params = {'Window':uparm[1][2], 'Apphot_Radius':uparm[4][2], 'Color':uparm[0][2], 'Plot_Radius':uparm[3][2], \
#                   'N_Contours':uparm[5][2],  'Apspec_upper':uparm[6][2], 'Apspec_lower':uparm[7][2], 'Aptrace_radius':uparm[10][2], 'Sat_Limit':uparm[11][2]}
colid = np.array((uparm[0][:]))
colparm = np.array(uparm[1][:])
colval = (uparm[2][:])
col_desc = (uparm[3][:])


#app = QtGui.QGuiApplication([])
app = pg.mkQApp()
## Create window with two ImageView widgets
win = QtWidgets.QMainWindow()

win.statusbar = QtWidgets.QStatusBar()
win.setStatusBar(win.statusbar)
win.resize(1024,1024)
win.setWindowTitle('imXam')
cw = QtWidgets.QWidget()
win.setCentralWidget(cw)
l = QtWidgets.QGridLayout()
#l = QtGui.QGridLayout()
cw.setLayout(l)
imv1 = pg.ImageView(view=pg.PlotItem())
imv2 = pg.PlotWidget()
imv3 = pg.PlotWidget()
imv4 = pg.PlotWidget()

l.addWidget(imv4, 0,0,3,4)
l.addWidget(imv1, 0,0,3,4)  # row, col, rowspan, columnspan
l.addWidget(imv2, 3,0,1,2)   # rowspan, columnspan
l.addWidget(imv3, 3,2,1,2)    # rowspan, columnspan

win.show()
uext = int(args.uextension)

dispaxis = int(args.dispaxis)

test_iris = args.lvl2 == None
test_cube = args.cube == None
if test_cube == 0:
    cube_val = int(args.cube)

test_hsg = args.hsg == None

if test_iris == 1 and test_cube == 1 and test_hsg == 1:  # if test_hsg is None
    try:
        with fits.open(ifile) as o:
            datax = np.float32(np.transpose(o[uext].data))
            print('Dimensions of the FITS data:')
            print(datax.shape)
            if datax.ndim > 2:
                datax = np.squeeze(datax)
            if (int(float(args.replace)) > -999):
                datax = np.where(np.isfinite(datax) == False, float(args.replace), datax)
    except:
        try:
            dat3d = fits.getdata(ifile, 1)
            print('Guessing that this is a reduced HSG fits file from Adams pipeline.')
            dat2d = dat3d[uext, :, :].squeeze()
            datax = np.float32(np.transpose(dat2d))
        except:
            print('Failed to read in the image cube fits file.')

if test_iris == 0:
    iris_raster_ext = int(args.lvl2)
    try:
        import iris_lmsalpy.extract_irisL2data as extract_irisL2data
        sp = extract_irisL2data.load(ifile)
        #  Need to add keyword to specify wavelength window here, and ability to construct from all. #
        dataxyz = sp.raster['Mg II k 2796'].data
        datax = np.transpose(dataxyz[:,iris_raster_ext,:])
    except:
        print('Need to install LMSALs IRIS python distribution: https://iris.lmsal.com/itn45/IRIS-LMSALpy_chapter1.html ')

if test_cube == 0:  # ==0 means it is a datacube file (3rd axis)
    if test_hsg == 1:  # ==1 means NOT hsg file
        dc = fits.getdata(ifile)
    datax3 = np.transpose(dc)
    if int(args.tlim2) > int(args.tlim1):
        datax2 = np.transpose(dc)
        datax2 = datax2[:,:,int(args.tlim1):int(args.tlim2)]
        print('Plotting 3rd axis slice in lower-left panel at cursor location.')
    print('Dimensions of FITS cube: ')
    print(np.float32(datax3.shape))
    datax = np.float32(datax3[:,:, cube_val])
    if int(args.scube) >= 0:
        datax = datax - np.float32(datax3[:,:, int(args.scube)])

if test_hsg == 0:
    if test_hsg == 0:
        dc = fits.getdata(ifile, 1)
    datax3 = np.transpose(dc)
    if int(args.tlim2) > int(args.tlim1):
        datax2 = np.transpose(dc)
        datax2 = datax2[:,:,int(args.tlim1):int(args.tlim2)]
        print('Plotting 3rd axis slice in lower-left panel at cursor location.')
    print('Dimensions of FITS cube: ')
    print(np.float32(datax3.shape))
    datax = np.float32(datax3[:,:, cube_val])
    print('Guessing that this is a reduced HSG fits file from Adams pipeline.')


nxx = datax.shape[0]
nyy = datax.shape[1]
data = np.zeros((nxx, nyy))
bias = np.zeros_like(data)
testb = args.biasname == None
if testb == False:
    bfile = args.biasname
    with fits.open(bfile) as bx:
        biasx = np.float32(np.transpose(bx[0].data))
    data = datax -  biasx
else:
    data = datax


imv1.setImage(data)
imv1.view.invertY(False)
#imv1.setColorMap('viridis')

print('   ')
print('File [ny , nx] = ',ifile,'[',nyy,',',nxx,']','   Max = ',np.max(data),'   Median = ',np.median(data))
print('   ')

roi = pg.LineSegmentROI([[int(nxx*0.03), int(nyy*0.5)], [int(nxx*0.97),int(nyy*0.5)]], pen=rcol)#,handlePen=(220,5,12),hoverPen=(0,0,0),handleHoverPen=(0,0,0))  # x = 0, y = 0 is at the top, left
roi_v = pg.LineSegmentROI([[int(nxx*0.5), int(nyy*0.15)], [int(nxx*0.5),int(nyy*0.85)]], pen=rcol)#,handlePen=(220,5,12),hoverPen=(0,0,0),handleHoverPen=(0,0,0))  # x = 0, y = 0 is at the top, left
# colors of hovering, endpoints, etc. are controlled in ROI.py in .../site-packages/pyqtgraph/graphicsItems/ but many arguments were added recently so I don't need to e. 

imv1.addItem(roi)
imv1.addItem(roi_v)

penax = pg.mkPen(color=(0,0,0))


# lower left window
def update():
    global data, imv1
    imv2 = pg.PlotWidget()
    l.addWidget(imv2, 3,0,1,2)
    d2 = roi.getArraySlice(data, imv1.imageItem, axes=(0,1), returnSlice=False)
    a = d2[0]
    x1= a[0][0]  # x-coordinate
    x2 = a[0][1]  # y-coordinate
    y1 = a[1][0]
    y2 = a[1][1]

    x22 = x2
    x11 = x1
    y11 = y1
    y22 = y2
    if x2 < x1:
        x11=x2
        x22=x1
        y11=y2
        y22=y1
    if y2 < y1:
        y11=y2
        y22=y1
        x11=x2
        x22=x1

    nx = x22-x11+1
    ny = y22-y11+1
    nvec = (nx**2 + ny**2)**0.5
    yarr = np.linspace(y11, y22, int(round(nvec)))
    m = (x22-x11) /(y22-y11)
    b = x22 - m*y22
    xarr = m * yarr + b
    dx = x22-x11
    dy = y22-y11
    xx = np.linspace(1,data.shape[0],data.shape[0])
    yy = np.linspace(1,data.shape[1],data.shape[1])
    myfunc = RegularGridInterpolator((xx,yy), data)
    nn=0
    vec=[0.]
    while nn < len(yarr):
        xarr[nn] = np.rint(xarr[nn])
        if dy > dx:  # vertical cuts
            if xarr[nn] < data.shape[0]-1 and yarr[nn] < data.shape[1] - 1:
                val = data[int(xarr[nn]),int(yarr[nn])].tolist()
                vec = np.append(vec, val)
        if dx > dy:   #horizontal cuts
            if xarr[nn] > 1 and  xarr[nn] < data.shape[0]-1 and yarr[nn] < data.shape[1] - 1:
                if args.hcut == 'simple':
                    val = data[int(xarr[nn]),int(yarr[nn])].tolist()
                if args.hcut == 'interp':
                    val = myfunc((xarr[nn],yarr[nn]))   ##-- this uses the interpolation function (it's slow)
                vec = np.append(vec, val)
        nn=nn+1
    if len(vec) > 2:
        imv2.plot(vec[1:,])
       # imv2.plotItem.getAxis('left').setPen(color=(0, 0, 0), width=0.8) #.setStyle(tickTextColor= 'b')
      #  graphWidget.plotItem.getAxis('bottom').setPen(color=(0, 0, 0), width=0.8) #.setStyle(tickTextColor= 'b')
        imv2.setLabel('left', 'Counts / Pix')
        imv2.setLabel('bottom', 'Pix along slice')


        
roi.sigRegionChanged.connect(update)




# lower left window
def update_3(sli_x, sli_y):
    global data, imv1, datax2
    imv2 = pg.PlotWidget()
    l.addWidget(imv2, 3,0,1,2)
    plot_tslice = datax2[sli_x, sli_y, :]
    if int(args.scube) >= 0:
        plot_tslice = datax2[sli_x, sli_y, :] - datax2[sli_x, sli_y, int(args.scube)]
    imv2.plot(plot_tslice)

# Create a custom color map from Paul Tol's guide:  https://personal.sron.nl/~pault/
# This is just a sample one I selected -- its the Somooth Rainbow, rainbow_WhBr aka rainbow34 with the whites and light purples removed.
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm # this can be interpolated! 
clrs = ['#C3A8D1', '#B58FC2','#A778B4',\
        '#9B62A7', '#8C4E99', '#6F4C9B', '#6059A9', \
        '#5568B8', '#4E79C5', '#4D8AC6', '#4E96BC', '#549EB3', \
        '#59A5A9', '#60AB9E', '#69B190', '#77B77D', '#8CBC68', \
        '#A6BE54', '#BEBC48', '#D1B541', '#DDAA3C', '#E49C39', \
        '#E78C35', '#E67932', '#E4632D', '#DF4828', '#DA2222', \
        '#B8221E', '#95211B', '#721E17', '#521A13']  # bad data grey is 102,102,102

# Can also flip color s cheme if you prefer the opposite:   clrs = np.flip(clrs)
cmap_name = 'smrb'  # smooth rainbow.
map_rnbw = LinearSegmentedColormap.from_list(cmap_name, clrs, N=100)
rainbow = [(209,187,215), (174,118,163), (136,46,114), (25,101,176), (82,137,199), (123,175,222), (77,178,101), (144,201,135), (202, 224, 171), (247, 240, 86), (246,193, 65), (241,147,45), (232, 96,28), (220, 5,12), (119, 119, 119)]
for i in range(len(rainbow)):    
    r, g, b = rainbow[i]    
    rainbow[i] = (r / 255., g / 255., b / 255.)    

    
BuRd = ["#2166AC", "#4393C3", "#92C5DE", "#D1E5F0","#F7F7F7", "#FDDBC7","#F4A582", "#D6604D", "#B2182B"]  # bad = 255,238,153 = FFEE99
cmap_name = 'BuRd'  # smooth rainbow.
map_burd = LinearSegmentedColormap.from_list(cmap_name, BuRd, N=100)



#/anaconda3/envs/hst/lib/python3.6/site-packages/pyqtgraph/GraphicsScene/GraphicsScene.py
def ifkeypress(evnt):
    # need to setClickable on pop up spectrum.
    # need to y-flip t-key and check coordinates.
    val = evnt.text()
    global user_x, user_y, apspec_radius, boxx0,boxx1, boxy0,boxy1, box_std,box_mean,box_med,box_min,box_max
    global uxlim1, uxlim2
    if val == 'e' or val == 'p':
        print('   ')
        print('Location of imXam_param.dat: ', full_imexam_parm_path)
        print('   ')
        for ee in range(max(colid)+1):
            print(colid[ee],'|', colparm[ee],':',' <',colval[ee],'>', '::',col_desc[ee])
        print('   ')

        if val == 'e':
            parm_2_edit =  input('Enter integer corresponding to first column in imXam_param.dat (note: will not be saved upon quitting imXam): ')
            parm_new = input('Enter its new value: ')
            colval[int(parm_2_edit)] = parm_new


    test = np.argwhere(colparm == 'Window')
    sqz = np.squeeze(colval[test][0])
    imw = int( sqz )

    test = np.argwhere(colparm == 'Statsec')
    sqz = np.squeeze(colval[test][0])
    mrad = int( sqz )
    
    test = np.argwhere(colparm == 'Apphot_Radius')
    sqz = np.squeeze(colval[test][0])
    apr = int( sqz )
    

    test = np.argwhere(colparm == 'Back_1')
    sqz = np.squeeze(colval[test][0])
    urin = int( sqz )
    
    test = np.argwhere(colparm == 'Back_2')
    sqz = np.squeeze(colval[test][0])
    urout = int( sqz )
    
    test = np.argwhere(colparm == 'Color')
    sqz = np.squeeze(colval[test][0])
    user_map = sqz
    
    test = np.argwhere(colparm == 'RMax')
    sqz = np.squeeze(colval[test][0])
    Rplot = int( sqz )

    test = np.argwhere(colparm == 'N_Contours')
    sqz = np.squeeze(colval[test][0])
    Ncontours = int( sqz )

    test = np.argwhere(colparm == 'Apspec_Upper')
    sqz = np.squeeze(colval[test][0])
    apspec_radius_u = int( sqz )
    
    test = np.argwhere(colparm == 'Apspec_Lower')
    sqz = np.squeeze(colval[test][0])
    apspec_radius_l = int( sqz )
    
    test = np.argwhere(colparm == 'Window_Search')
    sqz = np.squeeze(colval[test][0])
    aptrace_window = int( sqz )
    
    test = np.argwhere(colparm == 'TSum')
    sqz = np.squeeze(colval[test][0])
    TSum = int( sqz )
    
    test = np.argwhere(colparm == 'NTrace')
    sqz = np.squeeze(colval[test][0])
    NTrace = int( sqz )
    
    test = np.argwhere(colparm == 'OTrace')
    sqz = np.squeeze(colval[test][0])
    OTrace = int( sqz )
    
    test = np.argwhere(colparm == 'Window_Show')
    sqz = np.squeeze(colval[test][0])
    imc = int( sqz )
    
    test = np.argwhere(colparm == 'Zmax')
    sqz = np.squeeze(colval[test][0])
    zmax = int( sqz )

    test = np.argwhere(colparm == 'Zmin')
    sqz = np.squeeze(colval[test][0])
    zmin = int( sqz )

    test = np.argwhere(colparm == 'Undo')
    sqz = np.squeeze(colval[test][0])
    undo = int( sqz )
    
    test = np.argwhere(colparm == 'FTrace')
    sqz = np.squeeze(colval[test][0])
    trace_func = sqz
    
    test = np.argwhere(colparm == 'ITrace')
    sqz = np.squeeze(colval[test][0])
    trace_iter = int( sqz )
                   
    if zmin < 0 and zmax < 0:
        Vmax = v1
        Vmin = v0
        
    else:
        Vmax = zmax
        Vmin = zmin
    
    QtCore.QCoreApplication.processEvents()


    if val == '1':  # lower left
        boxx0.append(user_x)
        boxy0.append(user_y)

    if val == '2': # upper right
        boxx1.append(user_x)
        boxy1.append(user_y)

        chk = np.nanstd(data[boxx0[-1]:boxx1[-1]+1, boxy0[-1]:boxy1[-1]+1])
        box_std.append(chk)
        chk = np.nanmean(data[boxx0[-1]:boxx1[-1]+1, boxy0[-1]:boxy1[-1]+1])
        box_mean.append(chk)
        chk = np.nanmedian(data[boxx0[-1]:boxx1[-1]+1, boxy0[-1]:boxy1[-1]+1])
        box_med.append(chk)
        chk = np.min(data[boxx0[-1]:boxx1[-1]+1, boxy0[-1]:boxy1[-1]+1])
        box_min.append(chk)
        chk = np.max(data[boxx0[-1]:boxx1[-1]+1, boxy0[-1]:boxy1[-1]+1])
        box_max.append(chk)
        n_boxes = len(boxx0)
        for nnn in range(0, n_boxes):
            print('-- Box # ',nnn+1, ' of ', n_boxes, ' stored --')
            print('Coordinates start at (0,0) relative to PyQTGraph display')
            print('x0 = {:8d}'.format(boxx0[nnn]))
            print('x1 = {:8d}'.format(boxx1[nnn]))
            print('y0 = {:8d}'.format(boxy0[nnn]))
            print('y1 = {:8d}'.format(boxy1[nnn]))
            print('dx = {:8d}'.format(np.abs(boxx0[nnn]- boxx1[nnn] + 1)))
            print('dy = {:8d}'.format(np.abs(boxy0[nnn]- boxy1[nnn] + 1)))
            print('mean = {:8f}'.format(box_mean[nnn]))
            print('median = {:8f}'.format(box_med[nnn]))
            print('standard dev = {:8f}'.format(box_std[nnn]))
            print('min = {:8f}'.format(box_min[nnn]))
            print('max = {:8f}'.format(box_max[nnn]))    

    if val == 'x' or val == 's':
        print('x:  Fractional pixel extraction using an aperture width of ', apspec_radius_u + apspec_radius_l, ' pixels with background subtraction.')

        if dispaxis == 1:
            t_data = np.transpose(data)
            xtrace, ytrace, bsubtrace, xvalsfitted, yvalsfitted = SpecLab.trace_1d(t_data, yguess=user_y, xstrt=user_x, search_win = aptrace_window, tsum=TSum, ntrace=NTrace,otrace=OTrace, bmin=urin, bmax=urout, N_iter=trace_iter, t_func = trace_func)
            ap_extract = SpecLab.extract_1d_frac(t_data, xtrace, ytrace, bsubtrace,apl=apspec_radius_l, apu=apspec_radius_u)

        else:
            t_data = np.array(data)
            xtrace, ytrace, bsubtrace, xvalsfitted, yvalsfitted = SpecLab.trace_1d(t_data, yguess=user_x, xstrt=user_y, search_win = aptrace_window, tsum=TSum, ntrace=NTrace,otrace=OTrace, bmin=urin, bmax=urout, N_iter=trace_iter, t_func = trace_func)
            ap_extract = SpecLab.extract_1d_frac(t_data, xtrace, ytrace, bsubtrace,apl=apspec_radius_l, apu=apspec_radius_u)

        fig = go.Figure(data=[go.Scatter(x=xtrace, y=ap_extract, marker_color="#000000",line_shape="hvh")])
        fig.update_layout(font_family='Times New Roman',font_size=15,title=ifile)
        fig.update_yaxes(title='Summed counts per wave pixel',nticks=10)
        fig.update_xaxes(title='Wavelength pixel')
        fig.show()
        print('Trace parameters:  xstart = ', user_x, '  tsum = ',TSum, '   ntrace = ',NTrace, '   t_func =', trace_func, ' otrace = ', OTrace, '  N_iter = ', trace_iter)
        
        if val == 's':
            np.save('tmp.x1d', ap_extract)

        QtCore.QCoreApplication.processEvents()
        
    if val == 'g':
        fit_succ = 1
        if dispaxis == 1:
            b_data = (np.transpose(data[user_x , user_y-urout:user_y-urin]) + np.transpose(data[user_x , user_y+urin:user_y+urout]) ) / 2.0
            t_data = np.transpose(data[user_x , user_y-int(apspec_radius_l*2):user_y+int(apspec_radius_u*2)])
            b_data = np.nanmedian(b_data)
            t_data = t_data - b_data
            ncol = len(data[0,:])
            pix_1d0 = np.linspace(0,ncol-1, ncol)
            pix_1d = pix_1d0[user_y-int(apspec_radius_l*2):user_y+int(apspec_radius_u*2)]
            try_y0 = user_y
        else:
            b_data = (data[user_x-urout:user_x-urin,user_y] + data[user_x+urin:user_x+urout,user_y]) / 2.0
            t_data = data[user_x-int(apspec_radius_l*2):user_x+int(apspec_radius_u*2),user_y] - np.nanmedian(b_data)
            ncol = len(data[:,0])
            pix_1d0 = np.linspace(0,ncol-1, ncol)
            pix_1d = pix_1d0[user_x-int(apspec_radius_l*2):user_x+int(apspec_radius_u*2)]
            try_y0 = user_x

        try:    
            fit3_parms = scipy.optimize.curve_fit( single_gau,  pix_1d, t_data, p0=(np.max(t_data),try_y0, 2),maxfev=7500)
            fit3_parms_0 = fit3_parms[0]
            (c1, mu1,  sigma1) = fit3_parms_0
            fitprof = single_gau(pix_1d, c1,  mu1, sigma1)

        except:
            mu1 = float(user_y)
            print('Gaussian fit failed.')
            fit_succ=0

        if fit_succ == 0: 
            fig = go.Figure(data=[go.Scatter(x=pix_1d-mu1, y=t_data, marker_color="#000000",line_shape="hvh")])
        if fit_succ ==1:
            FWHM = 2.35 * sigma1
            fig = go.Figure(data=[go.Scatter(x=pix_1d-mu1, y=t_data, marker_color="#000000", name="Data",line_shape="hvh"), go.Scatter(x=pix_1d-mu1, y=fitprof, marker_color=BR_red_col_HEX, name="Gaussian fit", mode="markers+lines")])
            print('Gaussian FWHM = {0:8.3f} pixels'.format(FWHM))
        fig.update_layout(font_family='Times New Roman',font_size=15,title=ifile+"<br>Gaussian FWHM (pix) = {0:8.3f}".format(FWHM))
        fig.update_xaxes(title='Spatial pixel - Centroid',nticks=10)
        fig.update_yaxes(title='Counts per pixel')
        fig.show()
                
        QtCore.QCoreApplication.processEvents()
           
    if val == 'c':
        yarr_1d = np.arange(0,len(data[user_x,:]),1)
        fig = go.Figure(data=[go.Scatter(x=yarr_1d, y=data[user_x, :], marker_color="#000000",line_shape="hvh")])
        fig.update_layout(font_family='Times New Roman',font_size=15)
        fig.update_yaxes(title='Counts per pixel',nticks=10)
        fig.update_xaxes(title='y pixel')
        fig.show()
        QtCore.QCoreApplication.processEvents()
        
    if val == 'l':
        
        f, ax = plt.subplots()
        xarr_1d = np.arange(0,len(data[:,user_y]),1) # starts at 0
        fig = go.Figure(data=[go.Scatter(x=xarr_1d, y=data[:,user_y], marker_color="#000000",line_shape="hvh")])
        fig.update_layout(font_family='Times New Roman',font_size=15)
        fig.update_yaxes(title='Counts per pixel',nticks=10)
        fig.update_xaxes(title='x pixel')
        fig.show()
        QtCore.QCoreApplication.processEvents()

    if val == 'm':
        t_data = np.transpose(data[user_x-mrad:user_x+mrad, user_y-mrad:user_y+mrad])
        print('     ')
        print('Stats in box of side ',  mrad*2, 'pixels')
        print('Max = {:8.2f}'.format(np.max(t_data)))
        print('Mean = {:8.2f}'.format(np.mean(t_data)))
        print('Median = {:8.2f}'.format(np.median(t_data)))
        print('Std Dev = {:8.2f}'.format(np.std(t_data)))
        print('     ')

        QtCore.QCoreApplication.processEvents()

            
            
    if val == 'r' or val == 'a' or val == 'z':
        t_data = np.transpose(data[user_x-aptrace_window:user_x+aptrace_window, user_y-aptrace_window:user_y+aptrace_window]) # just for centroidin
        t_data_all = np.transpose(data)
        dy = float( urout + 5 - aptrace_window)
        try:
            xcen1, ycen1 = centroid_2dg(t_data) # center in tiny frame transposed 
            xcen0 = xcen1 + float(user_x) - float(aptrace_window)  # center in full frame t_data_all[ycen0, xcen0)
            ycen0  = ycen1 + float(user_y) - float(aptrace_window)
            if val == 'z':

                xtemp = np.arange(0,len(t_data_all[0,:]),1)
                ytemp = np.arange(0,len(t_data_all[:,0]),1)
                xtemp = xtemp[user_x-urout-5:user_x+urout+5]
                ytemp = ytemp[user_y-urout-5:user_y+urout+5]
                zvals = t_data_all[user_y-urout-5:user_y+urout+5, user_x-urout-5:user_x+urout+5]
                fig_heatmap = go.Figure(data=go.Heatmap(x=xtemp, y=ytemp, z = zvals, zmin=Vmin,zmax=Vmax,\
                                                        colorscale="Greys_r"))

                
                fig = go.Figure(data=[fig_heatmap.data[0]])
                #x
                fig.add_shape(type="circle", \
                              xref="x", yref="y",\
                              x0=xcen0 - apr, y0=ycen0 - apr, x1=xcen0 + apr, y1=ycen0+apr, line_color="#EE6677")
                fig.add_shape(type="circle", \
                              xref="x", yref="y",\
                              x0=xcen0 - urin, y0=ycen0 - urin, x1=xcen0 + urin, y1=ycen0+urin, line_color="#228833")
                fig.add_shape(type="circle", \
                              xref="x", yref="y",\
                              x0=xcen0 - urout, y0=ycen0 - urout, x1=xcen0 + urout, y1=ycen0+urout, line_color="#228833")

                fig.update_layout(
                    width=540,
                    height=540)

                fig.update_yaxes(
                    scaleanchor = "x",
                    scaleratio = 1,
                )
                fig.update_layout(font_family='Times New Roman',font_size=15)
                fig.update_yaxes(title='y pixel')
                fig.update_xaxes(title='x pixel')
                fig.show()
    
                QtCore.QCoreApplication.processEvents()



            
            if val == 'r' or val == 'a':
                aper = CircularAperture([xcen0, ycen0], r=float(apr))
                annulus_aperture = CircularAnnulus([xcen0, ycen0], r_in =  urin, r_out = urout)
                annulus_masks = annulus_aperture.to_mask(method='center')
                annulus_data = annulus_masks.multiply(t_data_all)
                mask = annulus_masks.data
                annulus_data_1d =  annulus_data[mask > 0]
                bkg_med = np.median(annulus_data_1d)
                apphot_table = aperture_photometry(t_data_all - bkg_med, aper)
                bkg_sdev = np.std(annulus_data_1d)
                apphot_table['median_bkg'] = bkg_med
                apphot_table['aperture_sum'].format = '%10.3e'
                apphot_table['xcenter'].format = '%8.3f'
                apphot_table['ycenter'].format = '%8.3f'
                apphot_table['peak'] = np.max(t_data - bkg_med) # consider smaller section for max.

                t_data_all_sub = t_data_all - bkg_med
                print('    ')
                print('x, y = ({0:8.3f}, {1:8.3f} )'.format(apphot_table['xcenter'][0], apphot_table['ycenter'][0]))
                print('Aperture Sum = {0:10.3e}'.format(apphot_table['aperture_sum'][0]))
                print('Peak = {0:10.1f}'.format(apphot_table['peak'][0]))
                print('    ')

                if val == 'r':
                    fit_succ = 1
                    pix_1d = np.zeros(1)
                    pix_1d_r = np.zeros(1)
                    
                    nn = int(ycen0-urout-5)
                    pp = 0
                    while  nn < int(ycen0+urout+5):
                        mm=int(xcen0-urout-5)
                        while mm < int(xcen0+urout+5):
                            val = np.float32(t_data_all_sub[nn, mm])
                            pix_1d = np.append(pix_1d, [val])
                            val2 =  ((float(mm) - xcen0)**2 + (float(nn)  - ycen0)**2)**0.5 # xcen0 and ycen0 start at 0 unlike iraf so there is a 1 pixel offset.  
                            pix_1d_r = np.append(pix_1d_r, [val2])
                            mm+=1
                            pp+=1
                        nn+=1

                    pix_1d = pix_1d[1:,]
                    pix_1d_r = pix_1d_r[1:,]
                    try:    
                        fit3_parms = scipy.optimize.curve_fit( single_gau_fix, pix_1d_r, pix_1d, p0=(np.max(pix_1d), 2),maxfev=7500)
                        fit3_parms_0 = fit3_parms[0]
                        (c1,  sigma1) = fit3_parms_0
                        xdum = np.linspace(0,int(Rplot),300)
                        fitprof = single_gau_fix(xdum, c1,  sigma1)
                    except:
                        print('Could not fit gaussian to radial profile.')
                        fit_succ=0
            
                    if fit_succ == 0: 
                        fig = go.Figure(data=[go.Scatter(x=pix_1d_r, y=pix_1d, mode="markers",marker_color="#000000")])
                    if fit_succ ==1:
                        FWHM = 2.35 * sigma1
                        fig = go.Figure(data=[go.Scatter(x=pix_1d_r, y=pix_1d, mode="markers",marker_color="#000000", name="Data"), go.Scatter(x=xdum, y=fitprof, marker_color=BR_red_col, line_width=3, name="Gaussian fit") ])
                        
                        print('  ')
                        print('Gaussian FWHM = {0:8.3f} pixels'.format(FWHM))
                        print('   ')
                    fig.update_layout(font_family='Times New Roman',font_size=15,title=ifile+"<br>"+"Gaussian FWHM (pix) = {0:8.3f},   Aperture Sum (cts) = {1:10.0f}".format(FWHM,apphot_table['aperture_sum'][0]))
                    fig.update_xaxes(title='Spatial pixel',nticks=10)
                    fig.update_yaxes(title='Counts per pixel')
                    fig.update_xaxes(range=[0, Rplot])
                    fig.add_vline(x=apr, line_dash="dash", line_color="#EE6677", line_width=3,annotation_text="aperture radius")
                    fig.add_vline(x=urin, line_dash="dash", line_color="#228833", line_width=3,annotation_text="inner bkgd radius",annotation_position="bottom right")
                    fig.add_vline(x=urout, line_dash="dash", line_color="#228833", line_width=3,annotation_text="outer bkgd radius")
                    #fig.update_annotations(font=dict(color="#BBBBBB"))
                    fig.update_layout(
                        width=720,
                        height=540)

                    fig.show()
                
            
          #      https://pyqtgraph.readthedocs.io/en/latest/graphicsItems/axisitem.html
        #        http://www.silx.org/doc/silx/0.2.0/modules/gui/plot/plotwidget.html
    
        #https://www.learnpyqt.com/courses/graphics-plotting/plotting-pyqtgraph/

                    QtCore.QCoreApplication.processEvents()
        except:
            print('Failed to get centroid with centroid_2dg')

    if val == 'o':
        t_data = np.transpose(data[user_x-imc:user_x+imc, user_y-imc:user_y+imc])
        data_ap = data[user_x-imc:user_x+imc, user_y-imc:user_y+imc]
        aper = CircularAperture([user_x, user_y], r=float(apr))
        annulus_aperture = CircularAnnulus([user_x, user_y], r_in =  urin, r_out = urout)
        annulus_masks = annulus_aperture.to_mask(method='center')
        annulus_data = annulus_masks.multiply(np.transpose(data))
        mask = annulus_masks.data
        annulus_data_1d =  annulus_data[mask > 0]
        bkg_med = np.median(annulus_data_1d)
        tb_data = t_data - bkg_med
        max_data =np.max(tb_data)

        fig = go.Figure(data=
                        go.Contour(
                            z=tb_data,
                                colorscale='Hot',
                            contours=dict(
                                start=max_data/float(Ncontours),
                                end=max_data,
                                size=max_data/float(Ncontours),
                            ),))
        fig.update_layout(
                    width=540,
                    height=540)

        fig.update_yaxes(
                    scaleanchor = "x",
                    scaleratio = 1,
                )
        fig.update_layout(font_family='Times New Roman',font_size=15)
        fig.update_yaxes(title='y pixel')
        fig.update_xaxes(title='x pixel')
        fig.show()

        QtCore.QCoreApplication.processEvents()

    if val == 't':  # trace a spectrum and show trace with plotly 
        if dispaxis == 1:
            t_data = np.transpose(data)
            xtrace, ytrace, bsubtrace, xvalsfitted, yvalsfitted = SpecLab.trace_1d(t_data, yguess=user_y, xstrt=user_x, search_win = aptrace_window, tsum=TSum, ntrace=NTrace,otrace=OTrace, bmin=urin, bmax=urout, N_iter=trace_iter, t_func = trace_func)
            print('Trace parameters:  xstart = ', user_x, '  tsum = ',TSum, '   ntrace = ',NTrace, '   t_func =', trace_func, ' otrace = ', OTrace, '  N_iter = ', trace_iter)
            winup = int(np.max(ytrace))
            windwn = int(np.min(ytrace))
            t_shape = t_data.shape
            if winup + 20 >= t_shape[0]:
                ylimup = t_shape[0]-1
            else:
                ylimup = winup + 20
            if windwn - 20 <= 0:
                ylimdwn = 0
            else:
                ylimdwn = windwn - 20
            
            xtemp = np.arange(0,len(t_data[0,:]),1)
            ytemp = np.arange(0,len(t_data[:,0]),1)
            ytemp = ytemp[ylimdwn:ylimup]
            zvals = t_data[ylimdwn:ylimup, :]
            fig_heatmap = go.Figure(data=go.Heatmap(x=xtemp, y=ytemp, z = zvals, zmin=Vmin,zmax=Vmax,\
                                                        colorscale="Greys_r"))
            fig = go.Figure(data=[fig_heatmap.data[0]])

            fig.add_trace(
                go.Scatter(
                    x=xtrace,
                    y=ytrace,
                    mode="lines",
                    line=go.scatter.Line(color=BR_red_col_HEX),
                    showlegend=False)
            )

            fig.add_trace(go.Scatter(x=xvalsfitted, y=yvalsfitted, mode="markers", marker_color=BR_red_col_HEX,marker_size=12,showlegend=False))
            fig.update_yaxes(
                    scaleanchor = "y",
                    scaleratio = 1,
                )
        else:
            t_data = np.array(data)
            xtrace, ytrace, bsubtrace, xvalsfitted, yvalsfitted = SpecLab.trace_1d(t_data, yguess=user_x, xstrt=user_y, search_win = aptrace_window, tsum=TSum, ntrace=NTrace,otrace=OTrace, bmin=urin, bmax=urout, N_iter=trace_iter, t_func = trace_func)
            t_data = np.transpose(t_data)
            xtemp = np.arange(0,len(t_data[:,0]),1)
            ytemp = np.arange(0,len(t_data[0,:]),1)
            ytemp = ytemp[user_x-urout-5:user_x+urout+5]
            zvals = t_data[:, user_x-urout-5:user_x+urout+5]
            fig_heatmap = go.Figure(data=go.Heatmap(x=ytemp, y=xtemp, z = zvals, zmin=Vmin,zmax=Vmax,\
                                                        colorscale="Greys_r"))
            fig = go.Figure(data=[fig_heatmap.data[0]])

            fig.add_trace(
                go.Scatter(
                    x=ytrace,
                    y=xtrace,
                    mode="lines",
                    line=go.scatter.Line(color=BR_red_col_HEX),
                    showlegend=False)
            )
            fig.add_trace(go.Scatter(x=yvalsfitted, y=xvalsfitted, mode="markers", marker_color=BR_red_col_HEX,marker_size=12,showlegend=False))

            fig.update_yaxes(
                    scaleanchor = "y",
                    scaleratio = 1,
                )

        fig.update_layout(font_family='Times New Roman',font_size=15)
        fig.update_yaxes(title='y pixel')
        fig.update_xaxes(title='x pixel')
        fig.show()
        print('Trace parameters:  xstart = ', user_x, '  tsum = ',TSum, '   ntrace = ',NTrace, '   t_func =', trace_func, ' otrace = ', OTrace, '  N_iter = ', trace_iter)
 

        QtCore.QCoreApplication.processEvents()

    if val == 'T':  # Find and show pixels above a threshold.
        thressh =  input('Enter threshold value: ')
        thresh = float(thressh)
        t_data = np.transpose(data)

        sat_pixels = (t_data >= thresh)
        inds2d = np.argwhere(sat_pixels)
        if inds2d.shape[0] > 0:
            
            fig_heatmap = go.Figure(data=go.Heatmap(z = t_data, zmin=Vmin,zmax=Vmax,\
                                                        colorscale="Greys_r"))


            
            fig = go.Figure(data=[fig_heatmap.data[0], go.Scatter(x=inds2d[:,1], y=inds2d[:,0], mode="markers", marker_color=BR_red_col_HEX)])

            fig.update_layout(
                    width=720,
                    height=720)

            fig.update_yaxes(
                    scaleanchor = "x",
                    scaleratio = 1,
                )
            fig.update_layout(font_family='Times New Roman',font_size=15)
            fig.update_yaxes(title='y pixel')
            fig.update_xaxes(title='x pixel')
            fig.show()

        if inds2d.shape[0] == 0:
            print('  ')
            print('No pixels found above ', thresh)
            print('  ')
        else:
            print('Number of pixels found above threshold = ', thresh, ' is ',inds2d.shape[0])
        QtCore.QCoreApplication.processEvents()

    if val == 'H':
        try:
            hdr = fits.getheader(ifile)
            hdr.totextfile('lastheader.txt',overwrite=True)
            hdr.totextfile(ifile+'.header.txt',overwrite=True)
            print('Printed header to lastheader.txt and '+ifile+'.header.txt')
            os.system('open lastheader.txt &')
            try:
                print('DATE-OBS = ',hdr['DATE-OBS'])
                print('EXPTIME = ',hdr['EXPTIME'])
            except:
                print('Could not find DATE-OBS and EXPTIME in header.')
        except:
            print('Could not print header.')
    if val == 'q':
        QtCore.QCoreApplication.exit()
    if val == 'h' or val == '?' or  val == 'help' or val == 'Help':
        print('           ')
        print('************************************************************')
        print('q:  quit imXam.')
        print('r:  plot radial profile, print fwhm, and print aperture photometry w/ sky annulus subtraction centered at cursor location; plot x-range can be set with RMax.')
        print('x:  trace and extract spectrum with sky subtraction, at cursor location (can change params in imXam_param.dat).')
        print('g:  fits a Gaussian to the spatial profile (uniform weighting in fit) of a spectrum at cursor location. An estimate of a constant background level (e.g., bias in a raw frame) is subtracted before the fit')
        print('T:  show (e.g., saturated) pixels above some threshold.  Prompts for a threshold (ENTER an INTEGER, not e.g., 1.5e4) above which to color red.')
        print('a:  print fwhm and apperture photometry w/ sky annulus subtraction centered at cursor location.')
        print('o:  plot contours at cursor location (not centroided) and shows in +/- Window.')
        print('z:  zoom in on cursor location (can change scaling with Zmax and Zmin and color table with Color).  Overplots the aperture photometry annuli.')
        print('s:  does exactly what x does but also saves the extraction as tmp.x1d.npy')
        print('t:  show a fit to a trace of a spectrum on the 2D image.')
        print('m:  prints to terminal various statistics in a box +/- Statsec centered at cursor location.')
        print('l:  plot a row (line) through entire image at cursor location')
        print('c:  plot a column through entire image at cursor location')
        print('p:  show parameters in imXam_param.dat but dont edit.')
        print('e:  edit parameters in imXam_param.dat; use p to see which can be edited.')
        print('1 & 2:  clicking 1 in lower-left and 2 in upper-right will print stats within that box.')
        print('H:  prints header to file.header.txt and lastheader.txt; also prints EXPTIME and DATE-OBS to screen.')
        print('************************************************************')
        print('           ')



    return None


    
def mouseMovedEvent(pos):
        # Check if event is inside image, and convert from screen/pixels to image xy indicies
    mousePoint = roi.getViewBox().mapSceneToView(pos)
    x_i = int(np.floor(mousePoint.x()))
    y_i = int(np.floor(mousePoint.y()))
    global user_x
    global user_y
    user_x = x_i
    user_y = y_i
    if x_i >= 0 and x_i < nxx and y_i >= 0 and y_i < nyy:
        win.statusbar.showMessage("x = {}, y = {}, z = {:0.2f}; lower-left = (0,0)".format(x_i, y_i,data[x_i,y_i]))
        if test_cube == 0 and (int(args.tlim2) > int(args.tlim1)):
            update_3(x_i, y_i)
roi.scene().sigMouseMoved.connect(mouseMovedEvent)
roi.scene().sigKeyPress.connect(ifkeypress)



#https://stackoverflow.com/questions/40423999/pyqtgraph-where-to-find-signal-for-key-preses


## Display the data
imv1.setImage(data)
#imv1.setColorMap('CET-L17')

#mpl_connect('key_press_event', on_key_event)

zscale0, zscale1 = find_zscale(data)


if args.z1 == None:
    v0 = zscale0 # np.min(data)
   # v0 = np.median(data) * 0.50

if args.z2 == None:
    v1 = zscale1 # np.median(data)*1.2
    
if args.z1 != None:
    v0 = float(args.z1)

if args.z2 != None:
    v1 = float(args.z2)

print('Image scaling = ',int(v0), ' -- ', int(v1))
    
imv1.setHistogramRange(v0, v1)
imv1.setLevels(v0, v1)

#if test_cube == 1:  ## got rid of this if statement in v4.0.0
update()

# lower right window
def update_2():
    global data, imv1
    imv3 = pg.PlotWidget()
    l.addWidget(imv3, 3,2,1,2)
    d3 = roi_v.getArraySlice(data, imv1.imageItem, axes=(0,1), returnSlice=False)
    a = d3[0]
    x1= a[0][0]  # x-coordinate
    x2 = a[0][1]  # y-coordinate
    y1 = a[1][0]
    y2 = a[1][1]

    x22 = x2
    x11 = x1
    y11 = y1
    y22 = y2
    if x2 < x1:
        x11=x2
        x22=x1
        y11=y2
        y22=y1
    if y2 < y1:
        y11=y2
        y22=y1
        x11=x2
        x22=x1

    nx = x22-x11+1
    ny = y22-y11+1
    nvec = (nx**2 + ny**2)**0.5
    yarr = np.linspace(y11, y22, int(round(nvec)))
    m = (x22-x11) /(y22-y11)
    b = x22 - m*y22
    xarr = m * yarr + b
    dx = x22-x11
    dy = y22-y11
    xx = np.linspace(1,data.shape[0],data.shape[0])
    yy = np.linspace(1,data.shape[1],data.shape[1])
    myfunc = RegularGridInterpolator((xx,yy), data)
    nn=0
    vec=[0.]
    while nn < len(yarr):
        xarr[nn] = np.rint(xarr[nn])
        if dy > dx:  # vertical cuts
            if xarr[nn] < data.shape[0]-1 and yarr[nn] < data.shape[1] - 1:
                if args.vcut == 'simple':
                    val = data[int(xarr[nn]),int(yarr[nn])].tolist()
                if args.vcut == 'interp':
                    val = myfunc((xarr[nn],yarr[nn]))   ##-- this uses the interpolation function (it's slow)
                vec = np.append(vec, val)
        if dx > dy:   #horizontal cuts
            if xarr[nn] < data.shape[0]-1 and yarr[nn] < data.shape[1] - 1:
                val = data[int(xarr[nn]),int(yarr[nn])].tolist()
                vec = np.append(vec, val)
        nn=nn+1
    if len(vec) > 2:
        imv3.plot(vec[1:,])
        imv3.setLabel('left', 'Counts / Pix')
        imv3.setLabel('bottom', 'Pix along slice')


roi_v.sigRegionChanged.connect(update_2)

update_2()

mouse_tooltip = QtWidgets.QLabel()
# Commented these out b/c they don't work with PyQtGraph 0.13.
#mouse_tooltip.setFrameShape(QtWidgets.QFrame.StyledPanel)
#mouse_tooltip.setWindowFlags(QtCore.Qt.ToolTip)
#mouse_tooltip.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
mouse_tooltip.show()



def single_gau_fix( x, c1,sigma1):
    res =   c1 * np.exp( - (x - 0.0)**2.0 / (2.0 * sigma1**2.0) ) 
    return res
def single_gau( x, c1,  mu1, sigma1 ):
    res =   c1 * np.exp( - (x - mu1)**2.0 / (2.0 * sigma1**2.0) )
    return res



#https://stackoverflow.com/questions/60183177/issue-with-matplotlib-plotting
#roi.scene().sigMouseClicked.connect(keyPressEvent)

if __name__ == '__main__':
    #import sys
    #if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    pg.exec()
#QtGui.QGuiApplication.instance()
## Start Qt event loop unless running in interactive mode.
#if __name__ == '__main__':
    #import sys
    #if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#    QtGui.QGuiApplication.instance().open()

        
