from distutils.core import setup
import py2exe, sys, os

Icons = []
for files in os.listdir('./drawables/'):
    f1 = './drawables/' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'drawables', [f1]
        Icons.append(f2)

sys.argv.append('py2exe')
setup( 
	data_files = Icons,
    options = {
		'py2exe' : {
			'includes': ['numpy', 'pygame'],
			'optimize': 2,
			'skip_archive': False,
			'compressed': True,
			'bundle_files': 0, #Options 1 & 2 do not work on a 64bit system
			'dist_dir': 'dist',  # Put .exe in dist/
			}
		},                   
    zipfile=None, 
    windows = ['launcher.py'],
)