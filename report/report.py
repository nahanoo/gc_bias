import subprocess
import markdown
from os.path import join as j
import pandas as pd

class Report():
    """This creates a basic report taking a bamfile as an input.
    Ouput is a markdonw which can be converted to pdf."""

    def get_bam_stats(self,bam_file):
        """Returns mapping stats of a bam file using samtools flagstat."""
        cmd = ['samtools','flagstat',bam_file]
        process = subprocess.run(cmd,capture_output=True)
        stats = process.stdout.decode()
        return stats

    def get_average_coverage(self,out):
        df = pd.read_csv(j(out,'gc_coverage.tsv'),sep='\t')
        return 

    def create_md(self,bam_file,labels,average_coverage,out):
        """This creates the makdown file using the mardkown package."""
        #Creating input for markdown conversion
        title = ['# Report of ',labels['title']]    
        stats = ['## Mapping stats of Illumina reads','\n','<br />'.join(self.get_bam_stats(bam_file).splitlines())]
        coverage = ['## Coverage plot','\n','This plots shows the coverage per position in the genome.',\
        '<br />','Average coverage: ',str(average_coverage),'<br />','\n','![coverage]','(','histogram.png',')',\
            '<br />','<br />','<br />',]
        gc_bias = ['## Sequence bias of Illumina reads','\n','The reference sequence was split into 150 BP windows \
        using a k-mer approach. Of every window the GC content and the coverage was calculated. \
        Those values were visualized using a 2d histogram. There is a cut off for the coverage at 20\
        because we want to inspect low coverage areas using this plot. Therefore if the plot is empty, check the\
        average coverage and the coverage histogram because maybe the coverage over the entire genome is > 20.','\n',\
        '![gc_bias]','(','density_plot.png',')']
        body = [''.join(title), ''.join(stats), ''.join(coverage),''.join(gc_bias)]
        body = '\n'.join(body)

        #Wrting markdown to file
        with open(j(out,'report.md'),'w') as handle:
            handle.write(markdown.markdown(body))