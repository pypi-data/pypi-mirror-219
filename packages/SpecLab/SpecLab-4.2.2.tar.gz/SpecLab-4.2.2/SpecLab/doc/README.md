# imXam:  v4.2.2 (Latest)

**imXam** is the first interactive program finished for the **SpecLab** python-only
data reduction package.  More (identify, standard, sensfunc, apall) will be added
with the same GUI design (PyQtGraph + Plotly) in the future as these get finished.

This uses [PyQTGraph](https://www.pyqtgraph.org/) 0.13.3, which will be installed automatically.  
A customized version of a few routines (`ROI.py`, `GraphicsScene.py`, `ImageView.py`) will be copied
to your site-packages/pyqtgraph/ by running the config below.  The installation below will install PyQt6 (6.5.1).

author: Adam F Kowalski (July 12, 2023)

## Installing imXam 

### Step 1

From terminal (if you want to install to your current conda environment; if not, go to Step 2):

`pip install SpecLab`


### Step 2

Create a conda environment to install into.  If you already have
run `pip install SpecLab` in that environment, then skip to Step 3 below.

To set up a fresh conda environment:

From a terminal window:

`conda create --name your_env_name python=3.11`

`conda activate your_env_name`

`pip install SpecLab`


### Step 3

After pip install, run the command (from anywhere), which will untar the modifications to PyQtGraph to your site-packages:

`SpecLab_config.py`

You may have to open a fresh tab in your terminal for your system to see the new routines in .../your_env_name/bin/.  You can also:

`cd /location_of_your_anaconda/anaconda3/envs/your_env_name/bin/`

`python SpecLab_config.py`


### Basic Usage

You will then be able to run imXam.py from anywhere (it is located in .../anaconda3/envs/your_env_name/bin/).

Basic usage (or create an alias for `imXam.py -f` in your .bash_profile):

`imXam.py -f file.fits`

To get a list of command-line options, type in a Unix terminal:

`imXam.py -h`

To load in a spectrum with the dispersion axis vertical (e.g., ARC3.5m/KOSMOS spectrum):

`imXam.py -f KOSMOS_spectrum.fits -dispax 2`

To load in some reasonable parameters for tracing, extracting, etc with an ARCES / echelle spectrum, use:

`imXam.py -f ARCES_spectrum.fits -ec 1`

You can also create your own imXam_param.dat file and specify to load it in with `-i /full_path_to_custom_param/your_custom_param.dat`

You can edit imXam_param.dat directly from Unix command line by typing into a terminal:

`epar_imXam.py`

(requires vim)

Please see KNOWN_ISSUES.

Enjoy!


## Interactive Commands

Will need to left mouse click on pyqtgraph display image for these to register.  Please use the wheel on your mouse to zoom in and out of the PyQTGraph display window.

click 'h' key to print this to screen from within imXam:

The default parameters used to do the calculations are in imXam_param.dat.  You can edit this file from command line by typing `epar_imXam.py'


q:  quit imXam.

r:  plot radial profile, print fwhm, and print aperture photometry w/ sky annulus subtraction centered at cursor location; plot x-range can be set with RMax.

x:  trace and extract spectrum with sky subtraction, at cursor location (can change params in imXam_param.dat).

g:  fits a Gaussian to the spatial profile (uniform weighting in fit) of a spectrum at cursor location. An estimate of a constant background level (e.g., bias in a raw frame) is subtracted before the fit

T:  show (e.g., saturated) pixels above some threshold.  Prompts for a threshold above which to color red.

a:  print fwhm and apperture photometry w/ sky annulus subtraction centered at cursor location.

o:  plot contours at cursor location (not centroided) and shows in +/- Window.

z:  zoom in on cursor location (can change scaling with Zmax and Zmin and color table with Color).  Overplots the aperture photometry annuli.

s:  does exactly what x does but also saves the extraction as tmp.x1d.npy

t:  show a fit to a trace of a spectrum on the 2D image.

m:  prints to terminal various statistics in a box +/- Statsec centered at cursor location.

l:  plot a row (line) through entire image at cursor location

c:  plot a column through entire image at cursor location

p:  show parameters in imXam_param.dat but dont edit.

e:  edit parameters in imXam_param.dat; use p to see which can be edited.

1 & 2:  clicking 1 in lower-left and 2 in upper-right will print stats within that box.

H:  prints header to file.header.txt and lastheader.txt; also prints EXPTIME and DATE-OBS to screen.


# To Upgrade

`pip install SpecLab --upgrade`

# To Uninstall

`pip uninstall SpecLab`

Will have to remove pyqtgraph10_speclab/ from your environment site-packages by hand.

# Acknowledgments

Thanks to Isaiah Tristan and Yuta Notsu for testing and feedback on an early version.
Thanks to Bill Ketzeback for helpful feedback and testing the most recent versions.  
Thanks to Gordon MacDonald for helpful suggestions.

# Troubleshooting
On a Linux, one may have to try these commands if one gets an error during `pip install Speclab`:

`sudo apt install libxcb-cursor0`

or

`sudo apt install --reinstall libxcb-cursor0`

or

`sudo apt-get install --reinstall libxcb-xinerama0`

