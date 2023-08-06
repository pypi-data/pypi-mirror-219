import tarfile
import itertools
import math
from Bio import SeqIO
from pankmer.index import print_err, kmer_size, generate_mem_blocks, measure_genomes
from os import listdir
from os.path import join, exists, isfile, isdir

from pankmer.version import __version__
from pankmer.gzip_agnostic_open import gzip_agnostic_open


def dryrun(genomes_input, split_memory: int = 1, threads: int = 1) -> dict:
    """Perform a dry run of indexing and return the metadata

    Parameters
    ----------
    genomes_input
        path to directory or tar file containing input genomes
    split_memory : int
        number of memory blocks per thread
    threads : int
        number of threads

    Returns
    -------
    dict
        index metadata
    """
    
    if not isinstance(genomes_input, (tuple, list)):
        genomes_input = list(genomes_input) if isinstance(genomes_input, set) else [genomes_input]
    if len(genomes_input) == 1 and isfile(genomes_input[0]) and tarfile.is_tarfile(genomes_input[0]):
        input_is_tar = True
        with tarfile.open(genomes_input[0]) as tar:
            genomes = [tarinfo.name for tarinfo in tar if tarinfo.isreg()]
    else:
        input_is_tar = False
        genomes = list(itertools.chain.from_iterable(
            ([join(g, f) for f in sorted(listdir(g))] if isdir(g) else [g])
            for g in genomes_input))
        for genome in genomes:
            if not exists(genome) or not isfile(genome):
                raise RuntimeError(f"{genome} does not exist or is not a file!")
    print_err('Recording genome sizes')
    genomes_dict = measure_genomes(genomes, str(genomes_input[0]) if input_is_tar else '')
    mem_blocks = generate_mem_blocks(split_memory, threads)
    all_core_blocks = []
    for m in range(1, len(mem_blocks)):
        temp_core_block = [mem_blocks[m-1][-1]]
        for i in range(len(mem_blocks[m])):
            temp_core_block.append(mem_blocks[m][i])
            all_core_blocks.append(temp_core_block)
            temp_core_block = [mem_blocks[m][i]]
    return {'kmer_size': kmer_size(),
        'version': __version__,
        'genomes': {c: g for c, g in enumerate(genomes)},
        'genome_sizes': genomes_dict,
        'positions': {},
        'mem_blocks': all_core_blocks
    }
