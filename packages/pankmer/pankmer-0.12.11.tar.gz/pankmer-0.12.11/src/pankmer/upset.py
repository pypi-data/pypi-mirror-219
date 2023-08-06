import pandas as pd
import upsetplot
import gzip
from collections import Counter
from itertools import compress
from matplotlib import pyplot
from pankmer.index import score_byte_to_blist, subset_scores_to_list

def count_scores(pk_results, genomes, scores: list, idx_map: dict):
    """Compute score counts for input to upsetplot

    Parameters
    ----------
    pk_results : PKResults
        PKResults object representing superset index
    genomes
        iterable of genomes included in subset
    scores : list
        score list after subsetting
    idx_map : dict
        map from superset score index to subset score index
    """

    genomes_ordered = tuple(g for g in pk_results.genomes if g in genomes)
    memberships = {i: tuple(compress(genomes_ordered, score_byte_to_blist(bytes(s), len(genomes))))
                   for i, s in enumerate(scores)}
    idx_map_bytes = {i_sup.to_bytes(8, byteorder='big'): i_sub
                     for i_sup, i_sub in idx_map.items()}
    counts = {}
    for i, n in Counter(i for _, i, _ in pk_results).items():
        if i in idx_map_bytes.keys():
            membership = memberships[idx_map_bytes[i]]
            counts[membership] = counts.get(membership, 0) + n
    return pd.Series(counts.values(), index=pd.MultiIndex.from_tuples(
        (tuple(g in k for g in genomes_ordered) for k in counts.keys()),
        names=genomes_ordered))


def upset(pk_results, output, genomes, vertical=False, show_counts=False,
          min_subset_size=None, max_subset_size=None, exclusive=False,
          table=None):
    scores, idx_map = subset_scores_to_list(str(pk_results.results_dir),
        str(pk_results.results_dir if pk_results.input_is_tar else ''),
        tuple(pk_results.genomes), genomes, exclusive)
    score_counts = count_scores(pk_results, genomes, scores, idx_map)
    if table:
        with (gzip.open if table.endswith('.gz') else open)(table, 'wb') as f:
            score_counts.to_csv(f, sep='\t', header=['k-mers'])
    upsetplot.plot(score_counts,
        orientation='vertical' if vertical else 'horizontal',
        show_counts=show_counts,
        min_subset_size=min_subset_size,
        max_subset_size=max_subset_size)
    pyplot.savefig(output)
