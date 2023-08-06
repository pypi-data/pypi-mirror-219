#!/usr/bin/env python

# import os
import site
import tarfile


try:
    your_site_packages_location = site.getsitepackages()
    tar_fname = your_site_packages_location[0]+'/'+'SpecLab/aux/pyqtgraph_modifications.tar.gz'
#    current_dir = os.getcwd()+'/'

 #   if not os.path.exists(your_site_packages_location[0]+'/pyqtgraph10_speclab/'):
#        print('Extracting PyQTGraph v10 tarfile (pyqtgraph10_speclab.tar.gz) contents to ', your_site_packages_location[0]+'/pyqtgraph10_speclab/')
 #       print('If uninstall SpecLab through pip (pip uninstall SpecLab), you may also want to rm -r pyqtgraph10_speclab/ from within your site-packages/ directory. ** Please be careful with the rm -r command **')

        
 
    tarfgz = tarfile.open(tar_fname)
    tarfgz.extractall(your_site_packages_location[0]+'/')
    tarfgz.close()
    #else:
    #    print('Could not unpack pyqtgraph modifications.')

    print('    ')
    print('    PyQtGraph is in ', your_site_packages_location[0]+'/pyqtgraph/')
    print('    Several routines were overwritten with imXam modifications:  ')
    print('      pyqtgraph/imageview/ImageView.py')
    print('      pyqtgraph/GraphicsScene/GraphicsScene.py')
    print('      pyqtgraph/graphicsItems/ROI.py')
    print('  ')
    print('    SUCCESS. Installation and configuration complete! ')
    print('  ')
    print('    Basic use (from anywhere on disk) in Unix command line: imXam.py -f <file.fits>')
    print('  ')
    print('   ')
    print('    Notes:  Can put alias in .bash_profile:  alias imXam=<single quotes>imXam.py -f<single quotes>')
    print('If the command python imXam.py is not recognized (it should be in your anaconda3 environment bin/), the source is located here:  ', your_site_packages_location[0]+'/SpecLab/imXam/')
    print('    in which case, just put an alias to the command <single quotes>python .../site-packages/SpecLab/imXam/imXam.py -f<single quotes> in .bash_profile (or create a softlink through ln -s to a bin/ folder')
    print('  ')
    print('  ')
    print('To uninstall:  pip uninstall SpecLab')
    print('  ')
    

except:
    print('Unable to complete configuration of PyQtGraph routines for imXam.')


