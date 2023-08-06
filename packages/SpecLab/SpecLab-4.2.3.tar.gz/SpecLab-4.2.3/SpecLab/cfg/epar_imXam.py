#!/Users/adamkowalski/anaconda3/envs/astroconda/bin/python

import os
import site
import tarfile


try:
    your_site_packages_location = site.getsitepackages()
    full_parm_path = your_site_packages_location[0]+'/'+'SpecLab/aux/param_files/imXam_param.dat'
    os.system('vim '+full_parm_path)
except:
     print('Unable to open '+full_parm_path)
     print('Tried using vim')
