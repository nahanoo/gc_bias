from setuptools import setup, find_packages

setup(name='gc_bias',
      version='1.0',
      description='Visualizes GC bias by plotting GC content of k-mers vs coverage of k-mers',
      author='Eric Ulrich',
      url='https://github.com/nahanoo/gc_bias',
      packages=['gc_bias'],
      install_requires=['pandas',
                        'plotly',
                        'biopython',
                        'subprocess.run',
                        'numpy'],
      entry_points={
          'console_scripts': [
              'plot_gc_bias = gc_bias.main:main'
          ]
      }
     )
