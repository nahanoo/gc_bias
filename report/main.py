import argparse
from report import GC
from report import Plotting
import os
import pandas as pd
from report import Report
import json

def parse_args():
    """Parsing required and optional arguments."""
    parser =  argparse.ArgumentParser(description='Generates report \
        for bam files including sequence bias visualization. \
        In order to do so the reference is split default to 150-mers. \
        For every 150-mer the GC content and the coverage is calculated. \
        Those values are visualized as 2d histograms. \
        This package requires SAMtools in your path.')
    parser.add_argument('reference',help='path to reference\
        sequence in fasta.')
    parser.add_argument('bam_file',help='path to sorted BAM file.')
    parser.add_argument('labels',help='json file labels for plots.\
        see https://github.com/nahanoo/gc_bias for example file.')
    parser.add_argument('output_dir',help='output direcotry.')
    parser.add_argument('--window_size',type=int,help='window size\
        used for GC content calculations [default 150]')
    parser.add_argument('--plotting_only',help='if added, only the plot will be\
        regenerated.',action='store_true')
    return parser.parse_args()

def main():
    args = parse_args()
    #Setting default values
    if args.window_size is None:
        args.window_size = 150
    gc = GC(args.reference,args.bam_file)
    gc.get_average_coverage()
    #Reading plot labels
    with open(args.labels,'r') as handle:
        data = handle.read()
    labels = json.loads(data)

    #Calls for plotting only
    if not args.plotting_only:
        #Calculating gc content and coverage
        gc.get_gc_coverage_tuples(args.window_size)
        gc.drop_df(args.output_dir)
    if os.path.exists(os.path.join(args.output_dir,'gc_coverage.tsv')):
        p = Plotting()
        #Reading precomputed gc content and coverage file
        df = pd.read_csv(os.path.join(args.output_dir,'gc_coverage.tsv'),sep='\t')
        #Generating 2d heatmap
        p.density_plot(df)
        #Updating labels
        p.update_labels(p.heatmap,labels['density_plot'])
        p.heatmap.write_image(os.path.join(args.output_dir,'density_plot.png'))
        #Generating coverage histogram
        p.distribution(gc.depth_df,gc.average_coverage*1.5)
        #Updating labels
        p.update_labels(p.histogram,labels['histogram'])
        p.histogram.write_image(os.path.join(args.output_dir,'histogram.png'))
        #Creating markdown report
        Report().create_md(args.bam_file,labels['histogram'],gc.average_coverage,args.output_dir)
    else:
        print('You need to run the analysis first, therefore remove the\
            --plotting_only flag from your command.')

if __name__ == "__main__":
    main()