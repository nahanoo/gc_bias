from Bio import SeqIO
import pandas as pd
from io import StringIO
import os
import subprocess

class GC():
    """Class for investigating GC content and coverage correlation.
    Class needs to be initiated per sample and reference"""
    def __init__(self,reference,bam_file):
        self.reference = {contig.name:contig for contig in SeqIO.parse(reference,'fasta')}
        self.get_depth(bam_file)
        self.depth_to_dict(self.depth_df)

    def get_depth(self,bam_file):
        cmd = ['samtools','depth','-aa','-J',bam_file]
        process = subprocess.run(cmd,capture_output=True)
        self.depth_df = pd.read_csv(StringIO(process.stdout.decode()),sep='\t',\
            names=['chromosome','position','depth'])

    def depth_to_dict(self,depth):
        """Converts depth dataframe to dictionary.
        Chromosome and position as a tuple act as keys."""
        depth_dict = dict()
        for chromosome,position,depth in zip(depth['chromosome'],\
            depth['position'],depth['depth']):
            depth_dict[(chromosome,position-1)] = depth
        self.depth = depth_dict

    def get_gc_content(self,sequence):
        """This returns the gc content for a sequence."""
        return 100.0*len([base for base in sequence if base in "GC"])/len(sequence)

    def get_reference_gc_content(self):
        """Stores average gc content of entire reference sequence."""
        sequence = str()
        for contig in self.reference.values():
            sequence+=str(contig.seq)
        self.reference_gc_content = self.get_gc_content(sequence)
    
    def get_average_coverage(self):
        self.average_coverage = sum(self.depth_df['depth'])/len(self.depth_df)

    def get_coverage(self,chrom_pos_tuple,window_size):
        """Calculates coverage of sequence window.
        Carefull when calling that this doesn't result in key error
        if position is at end of contig.
        """
        coverage = []
        for pos in range(chrom_pos_tuple[1],chrom_pos_tuple[1]+window_size):
            coverage.append(self.depth[(chrom_pos_tuple[0],pos)])
        return sum(coverage)/len(coverage)

    def get_gc_coverage_tuples(self,window_size):
        """This returns a list of tuples where the first item is 
        the GC content in % and the second item average coverage.
        window_size specifies the window over which GC content and
        coverage is calculated.
        """
        self.gc_coverage = []
        for chromosome,record in self.reference.items():
            for position in range(len(record)-window_size):
                gc_content = self.get_gc_content(record[position:position+window_size])
                coverage = self.get_coverage((chromosome,position),window_size)
                if coverage < 20:
                    self.gc_coverage.append((gc_content,coverage))

    def drop_df(self,out):
        """Dropping gc content/coverage tuples as dataframe because 
        computationally too heavy to call on the spot."""
        df = pd.DataFrame(self.gc_coverage,columns=['gc_content','coverage'])
        df.to_csv(os.path.join(out,'gc_coverage.tsv'),sep='\t',index=False)
