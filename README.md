# GC bias visualization

## Introduction

This branch generates a basic stats report for bam files including plots investigating sequencing bias.
The report contains stats about mapping quality, coverage and sequencing bias.
For investigating sequencing bias, the reference is split into 150-mers. Of every 150-mer the coverage and the
GC content are calculated. Those values are visualized as a 2d histogram. Because this plot is mainly interesting to study low coverage areas, only 150-mers with coverage < 20 are visualized.
K-mer size can be controllable with the flag `--window-size`. An example report can be found in this repository.

## Installation

**This package requires samtools>=1.11 in your PATH.**  
The package can be installed using pip.

```
git clone https://github.com/nahanoo/gc_bias.git
cd gc_bias
pip install .
```

## Usage

```
usage: report_bam_stats [-h] [--window_size WINDOW_SIZE]
                        [--plotting_only]
                        reference bam_file labels
                        output_dir

Generates report for bam files including sequence bias
visualization. In order to do so the reference is split
default to 150-mers. For every 150-mer the GC content and
the coverage is calculated. Those values are visualized as
2d histograms. This package requires SAMtools in your
path.
Help page called with `report_bam_stats -h`: 

positional arguments:
  reference             path to reference sequence in
                        fasta.
  bam_file              path to sorted BAM file.
  labels                json file labels for plots. see
                        https://github.com/nahanoo/gc_bias
                        for example file.
  output_dir            output direcotry.

optional arguments:
  -h, --help            show this help message and exit
  --window_size WINDOW_SIZE
                        window size used for GC content
                        calculations [default 150]
  --plotting_only       if added, only the plot will be
                        regenerated.
```

### Plot labels

Plot labels for the coverage histogram and the sequencing bias histogram are specified in a json file.
Example json file:
```
{
    "density_plot": {
        "title": "Comamonas testosteroni in T11.2.1",
        "xlabel": "coverage per window",
        "ylabel": "GC content per window",
        "theme": "plotly"
    },
    "histogram": {
        "title": "Comamonas testosteroni in T11.2.1",
        "xlabel": "coverage",
        "ylabel": "counts",
        "theme": "plotly"
    }
}
```