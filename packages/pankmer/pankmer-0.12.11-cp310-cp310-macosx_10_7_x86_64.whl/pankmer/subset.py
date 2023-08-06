import gzip
import os
import os.path
import io
import math
import tarfile
import shutil
import json
from pankmer.index import subset_scores_to_file
from pankmer.version import __version__

def subset(pk_results, output, genomes, exclusive: bool = False,
           gzip_level: int = 6):
    """
    Extract a subset of a superset index given a subset genome list

    Parameters
    ----------
    pk_results : PKResults
        PKResults object representing the superset index
    output
        path to output dir or tar file for subset index
    genomes
        iterable of genomes to include in the subset
    exclusive : bool
        if True, perform an exclusive subset, excluding k-mers observed in
        genomes that are outside the subset [False]
    gzip_level : int
        gzip level for file compression
    """
    
    metadata_dict = {
        "kmer_size": pk_results.kmer_size,
        "version": __version__,
        "genomes": dict(enumerate(g for g in pk_results.genomes if g in genomes)),
        "genome_sizes": {g: pk_results.genomes[g] for g in genomes},
        "positions": {},
        "mem_blocks": pk_results.mem_blocks
    }
    kmer_bitsize = math.ceil((pk_results.kmer_size*2)/8)
    i_bitsize = 8
    output_is_tar = str(output).endswith('.tar')
    output_dir = output[:-4] if output_is_tar else output
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    idx_map = subset_scores_to_file(str(pk_results.results_dir),
        str(pk_results.results_dir if pk_results.input_is_tar else ''),
        tuple(pk_results.genomes), genomes, os.path.join(output_dir, 'scores.pks'),
        exclusive)
    idx_map_bytes = {i.to_bytes(i_bitsize, byteorder="big", signed=False):
                         j.to_bytes(i_bitsize, byteorder="big", signed=False)
                     for i, j in idx_map.items()}
    kmers_out_path = os.path.join(output_dir, f'kmers.bgz')
    indices_out_path = os.path.join(output_dir, f'indices.bgz')
    with gzip.open(kmers_out_path, 'wb', compresslevel=gzip_level) as kmers_out, \
        gzip.open(indices_out_path, 'wb', compresslevel=gzip_level) as indices_out:
        with io.BufferedWriter(indices_out, buffer_size=1000*i_bitsize) as io_buffer ,\
            io.BufferedWriter(kmers_out, buffer_size=1000*kmer_bitsize) as ko_buffer:
            count = 0
            for kmer, i, _ in pk_results:
                idx_remapped = idx_map_bytes.get(i)
                if idx_remapped is None:
                    continue
                ko_buffer.write(kmer)
                io_buffer.write(idx_remapped)
                if count%10000000 == 0 and count != 0: 
                    metadata_dict['positions'][str(pk_results.decode_kmer(kmer))] = count
                    count = 0
                count += 1
    with open(f'{output_dir}/metadata.json', 'w') as f:
        json.dump(metadata_dict, f)
    if output_is_tar:
        with tarfile.open(output, 'w') as tar:
            tar.add(output_dir)
        shutil.rmtree(output_dir)
