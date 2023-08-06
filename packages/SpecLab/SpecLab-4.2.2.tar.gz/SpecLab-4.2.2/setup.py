from distutils.core import setup
from pathlib import Path

setup(
    name='SpecLab',
    version='4.2.2',
    author='A. F. Kowalski',
    author_email='adam.f.kowalski@colorado.edu',
    packages=['SpecLab','SpecLab.aux','SpecLab.aux.param_files','SpecLab.imXam','SpecLab.doc','SpecLab.gen',],
    package_data = {'':['*.tar.gz', '*.txt', '*.dat', '*.md', '*.rst'],},
   # include_package_data=True,
   # package_dir={"": ""},
    scripts=['SpecLab/cfg/SpecLab_config.py','SpecLab/imXam/imXam.py','SpecLab/cfg/epar_imXam.py',],
    url='http://pypi.python.org/pypi/SpecLab/',
    description='IRAF imexam+DS9 alternative for Python',long_description_content_type='text/markdown',
    long_description=open('SpecLab/doc/README.md').read(),
    install_requires=['numpy>=1.25.0', 'plotly>=5.15.0', 'pandas>=2.0.3','astropy>=5.3.1','scipy>=1.11.1','matplotlib>=3.7.2','PyQt6==6.5.1', 'photutils>=1.8.0','pyqtgraph==0.13.3',]
)

# python setup.py sdist
# python -m twine upload --repository testpypi dist/*
# pip install -i https://test.pypi.org/simple/ speclab-imXam==3.1.2
# pip uninstall speclab-imXam==3.1.2
#  I neeeded to put the #! crap at the top of any of the scripts=
# put alias for imXam.py -f 

#https://test.pypi.org/project/SpecLab/3.1.3/
#https://test.pypi.org/project/SpecLab/3.1.12/
