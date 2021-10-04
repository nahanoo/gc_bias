import argparse
from gc_bias import GC
from gc_bias import Plotting
import os
import pandas as pd

def parse_args():
    """Parsing required and optional arguments."""
    parser =  argparse.ArgumentParser(description='Plot GC bias with\
        2d histograms. The GC content in percent is calculated using\
        a window size. For every window the according coverage is\
        calculated. GC content and coverage tuples are then visualized\
        using plotly. This package requires SAMtools in your path.')
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
    if args.window_size is None:
        args.window_size = 150
    if args.plotting_only:
        if os.path.exists(os.path.join(args.output_dir,'gc_coverage.tsv')):
            p = Plotting()
            df = pd.read_csv(os.path.join(args.output_dir,'gc_coverage.tsv'),sep='\t')
            p.density_plot(df)
            p.update_labels(args.labels)
            p.heatmap.write_image('density_plot.png')
        else:
            print('You need to run the analysis first, therefore remove the\
                --plotting_only flag from your command.')
    else:
        gc = GC(args.reference,args.bam_file)
        gc.get_gc_coverage_tuples(args.window_size)
        gc.drop_df(args.output_dir)
        p = Plotting()
        df = pd.read_csv(os.path.join(args.output_dir,'gc_coverage.tsv'),sep='\t')
        p.density_plot(df)
        p.update_labels(args.labels)
        p.heatmap.write_image('density_plot.png')