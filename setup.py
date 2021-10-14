from setuptools import setup, find_packages

setup(name='bam_stats',
      version='1.0',
      description='Creates a markdown report with stats about a bamfile. Includes GC bias visualization.',
      author='Eric Ulrich',
      url='https://github.com/nahanoo/gc_bias',
      packages=['report'],
      install_requires=['pandas',
                        'plotly',
                        'biopython',
                        'subprocess.run'
                        ],
      entry_points={
          'console_scripts': [
              'report_bam_stats = report.main:main'
          ]
      }
     )
