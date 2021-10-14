from samples import Samples
import subprocess
import json
import os

def plot_gc_bias():
    """Plotting GC bias, plotting is done by package gc_bias."""
    strain = 'ct'
    labels = dict()
    labels['title'] = strain+' in '+'T22.2.4'
    labels['xlabel'] = 'GC content per window'
    labels['ylabel'] = 'coverage per window'
    labels['theme'] = 'plotly_dark'

    j = json.dumps(labels,indent=4) 
    with open('./labels.json','w') as handle:
        handle.write(j)

    #Calling bash script to call gc_bias package
    #See https://github.com/nahanoo/gc_bias

    cmd = ['python','main.py','testdata/reference.fasta','testdata/mapped_reads.sorted.bam','testdata/']
    subprocess.call(' '.join(cmd),shell=True)
    
if __name__ == "__main__":
    plot_gc_bias()