Primary contact: Anthony Aylward, aaylward@salk.edu

# PanKmer

_k_-mer based and reference-free pangenome analysis. See the quickstart below, or read the [documentation](https://salk-tm.gitlab.io/pankmer/index.html).

## Installation
### In a conda environment
First create an environment that includes all dependencies:
```
conda create -c conda-forge -c bioconda -n pankmer rust python \
  biopython seaborn urllib3 python-newick pyfaidx gff2bed upsetplot \
  pybedtools
```
Then install PanKmer with `pip`:
```
conda activate pankmer
pip install pankmer
```

### With pip
PanKmer is built with [Rust](https://doc.rust-lang.org/stable/book/title-page.html),
so you will need to [install](https://doc.rust-lang.org/stable/book/ch01-01-installation.html)
it if you have not already done so. Then you can install PanKmer with `pip`:
```
pip install pankmer
```

### Check installation
Check that the installation was successful by running:
```
pankmer --version
```

## Tutorial
### Download example dataset

The `download-example` subcommand will download a small example dataset of
Chr19 sequences from _S. polyrhiza._
```
pankmer download-example -d .
```
After running this command the directory `PanKmer_example_Sp_Chr19/` will be present in the working directory. It contains FASTA files representing Chr19 from three genomes, and GFF files giving their gene annotations.
```
ls PanKmer_example_Sp_Chr19/*
```
```
PanKmer_example_Sp_Chr19/README.md

PanKmer_example_Sp_Chr19/Sp_Chr19_features:
Sp9509_oxford_v3_Chr19.gff3.gz Sp9512_a02_genes_Chr19.gff3.gz

PanKmer_example_Sp_Chr19/Sp_Chr19_genomes:
Sp7498_HiC_Chr19.fasta.gz Sp9509_oxford_v3_Chr19.fasta.gz Sp9512_a02_genome_Chr19.fasta.gz
```

To get started, navigate to the downloaded directory.
```
cd PanKmer_example_Sp_Chr19/
```

### Build a _k_-mer index

The _k_-mer index is a table tracking presence or absence of _k_-mers in the set of input genomes. To build an index, use the `index` subcommand and provide a directory containing the input genomes.

```
pankmer index -g Sp_Chr19_genomes/ -o Sp_Chr19_index.tar
```

After completion, the index will be present as a tar file `Sp_Chr19_index.tar`.
```
tar -tvf Sp_Chr19_index.tar
```
```
Sp_Chr19_index/
Sp_Chr19_index/kmers.b.gz
Sp_Chr19_index/metadata.json
Sp_Chr19_index/scores.b.gz
```

> #### Note
> The input genomes argument proided with the `-g` flag can be a directory, a tar archive, or a space-separated list of FASTA files.
>
> If the output argument provided with the `-o` flag ends with `.tar`, then the index will be written as a tar archive. Otherwise it will be written as a directory.


### Create an adjacency matrix

A useful application of the _k_-mer index is to generate an adjacency matrix. This is a table of _k_-mer similarity values for each pair of genomes in the index. We can generate one using the `adj-matrix` subcommand, which will produce a CSV or TSV file containing the matrix.

```
pankmer adj-matrix -i Sp_Chr19_index.tar -o Sp_Chr19_adj_matrix.csv
pankmer adj-matrix -i Sp_Chr19_index.tar -o Sp_Chr19_adj_matrix.tsv
```

> #### Note
> The input index argument proided with the `-i` flag can be tar archive or a directory.

### Plot a clustered heatmap

To visualize the adjacency matrix, we can plot a clustered heatmap of the adjacency values. In this case we use the Jaccard similarity metric for pairwise comparisons between genomes:

```
pankmer clustermap -i Sp_Chr19_adj_matrix.csv \
  -o Sp_Chr19_adj_matrix.svg \
  --metric jaccard \
  --width 6.5 \
  --height 6.5
```

![example heatmap](docs/source/_static/Sp_Chr19_adj_matrix.svg)

### Generate a gene variability heatmap

Generate a heatmap showing variability of genes across genomes. The following command uses the `--n-features` option to limit analysis to the first two genes from each input GFF3 file. The resulting image shows the level of variability observed across genes from each genome.

```
pankmer reg_heatmap -i Sp_Chr19_index/ \
  -r Sp_Chr19_genomes/Sp9509_oxford_v3_Chr19.fasta.gz Sp_Chr19_genomes/Sp9512_a02_genome_Chr19.fasta.gz \
  -f Sp_Chr19_features/Sp9509_oxford_v3_Chr19.gff3.gz Sp_Chr19_features/Sp9512_a02_genes_Chr19.gff3.gz \
  -o Sp_Chr19_gene_var.png \
  --n-features 2 \
  --height 3
```

![example heatmap](example/Sp_Chr19_gene_variability.png)
