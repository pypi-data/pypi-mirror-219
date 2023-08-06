//==============================================================================
// score_list_io.rs
//==============================================================================

// Imports =====================================================================
use std::{fs, io, str};
use std::boxed::Box;
use std::io::{Read, Write};
use std::path::PathBuf;
use niffler;
use pyo3::prelude::*;
use rmp_serde::Serializer;
use rustc_hash::FxHashMap as HashMap;
use serde::Serialize;
use tar::Archive;
use crate::{Kmer, Score, ScoreList, PKGenomes, IDXMap, ScoreToIDX};
use crate::helpers::{print_err, score_byte_to_blist};
use crate::get_kmers::genome_index_to_byte_idx_and_bit_mask;

//Functions ====================================================================

// Load a partial score list from an in-progress index
//
// Parameters
// ----------
// idx_dir : &str
//    directory of the in-progress index
// lower : Kmer
//     lower bound of the memory block to load
// upper : Kmer
//     upper bound of the memory block to load
//
// Returns
// -------
// ScoreList
//     the partial score list for the given memory block
pub fn load_scores_partial(idx_dir: &str, lower: Kmer, upper: Kmer) -> ScoreList {
    let mut in_path: PathBuf = PathBuf::from(&idx_dir);
    let in_base: String = format!("{lower}_{upper}_scores.pks");
    in_path.push(in_base);
    let inpath = in_path.into_os_string().into_string().unwrap();
    let buffer = fs::read(&inpath).expect(&format!("Can't read file {}", &inpath));
    let scores = rmp_serde::from_slice(&buffer).expect(&format!("Can't deserialize data from {}", &inpath));
    fs::remove_file(&inpath).expect("could not remove partial scores file");
    scores
}

/// Load scores
/// 
/// Load the score list of an index
/// 
/// Parameters
/// ----------
/// idx_dir : str
///     directory or tar file containing an index
/// tar_file : str
///     if the input index is a tar file, the file path. Otherwise, empty string
/// 
/// Returns
/// -------
/// list
///     score list of the index
#[pyfunction]
pub fn load_scores(idx_dir: &str, tar_file: &str) -> PyResult<ScoreList> {
    let mut scores: ScoreList = ScoreList::new();
    if tar_file.len() > 0 {
        let (tar, _format) = niffler::from_path(tar_file).expect(
            &format!("File not found: {}", tar_file));
        for f in Archive::new(tar).entries().expect("Can't read tar file") {
            let f = f.expect("Error reading tar archive");
            let in_path = f.path().expect("Error reading tar archive");
            let mut in_str = format!("{0:?}", &in_path);
            in_str.pop();
            let in_base = format!("scores.pks");
            if !(&in_str.ends_with(&in_base)) { continue; }
            let (mut reader, _format) = niffler::get_reader(Box::new(f)).expect("Can't read from tar archive");
            let mut buffer: Vec<u8> = Vec::new();
            reader.read_to_end(&mut buffer).expect(&format!("Can't read file {}", &in_str));
            scores = rmp_serde::from_slice(&buffer).expect(&format!("Can't deserialize data from {}", &in_str));
        }
    } else {
          let mut in_path: PathBuf = PathBuf::from(&idx_dir);
          let in_base: String = format!("scores.pks");
          in_path.push(in_base);
          let inpath = in_path.into_os_string().into_string().unwrap();
          let buffer = fs::read(&inpath)?;
          scores = rmp_serde::from_slice(&buffer).expect(&format!("Can't deserialize data from {}", inpath));
    }
    Ok(scores)
}

/// Dump scores
/// 
/// Write score list to disk, serialized by `rmp_serde`
/// 
/// Parameters
/// ----------
/// scores : list
///     the score list
/// outpath : str
///     path to output file
#[pyfunction]
pub fn dump_scores(scores: ScoreList, outpath: &str) -> PyResult<()> {
    let mut buf: Vec<u8> = Vec::new();
    scores.serialize(&mut Serializer::new(&mut buf)).expect("Couldn't serialize ScoreList");
    if outpath != "-" {
        let mut file = fs::File::create(&outpath).expect(
            &format!("Can't open file {} for writing", &outpath)
        );
        file.write_all(&buf).expect(
            &format!("Couldn't write ScoreList to file {}", &outpath)
        );
    }
    else {
        io::stdout().write_all(&buf).expect("Couldn't write ScoreList to stdout");
    }
    Ok(())
}

/// Compress scores
/// 
/// Extract a subset of genomes from a score list and generate a new score list
/// matching the genome subset
/// 
/// Parameters
/// ----------
/// supserset_scores : list
///     score list of the superset index
/// superset_genomes : list
///     genome list of the superset index
/// subset_genomes : list
///     genome list of the subset index
/// 
/// Returns
/// -------
/// list, dict
///     score list of the subset index, map from superset indices to subset
///     indices
#[pyfunction]
pub fn compress_scores(superset_scores: ScoreList, superset_genomes: PKGenomes, subset_genomes: PKGenomes) -> PyResult<(ScoreList, IDXMap)> {
    let n_superset_genomes = superset_genomes.len();
    let n_subset_genomes = subset_genomes.len();
    let n_superset_bytes = (n_superset_genomes + 7) / 8;
    let n_subset_bytes = (n_subset_genomes + 7) / 8;
    let mut memberships: Vec<usize> = Vec::new();
    for (i, genome) in superset_genomes.iter().enumerate() {
        if subset_genomes.contains(&genome) { memberships.push(i); }
    }
    let mut indices_map: IDXMap = HashMap::default();
    let mut subset_scores = ScoreList::new();
    let mut score_to_idx: ScoreToIDX = HashMap::default();
    for (key, score) in superset_scores.iter().enumerate() {
        let expanded_score: Vec<usize> = score_byte_to_blist(&score, n_superset_genomes)?;
        let mut compressed_score: Score = vec![0; n_subset_bytes];
        for (i, j) in memberships.iter().enumerate() {
            if expanded_score[*j] == 1 {
                let (byte_idx, bit_mask) = genome_index_to_byte_idx_and_bit_mask(i, n_subset_bytes);
                compressed_score[byte_idx] = compressed_score[byte_idx] | bit_mask;
            }
        }
        for compressed_byte in compressed_score.iter() {
            if compressed_byte > &0u8 {
                match score_to_idx.get(&compressed_score){
                    Some(idx) => { indices_map.insert(key as u64, *idx); },
                    None => {
                        indices_map.insert(key as u64, subset_scores.len());
                        score_to_idx.insert(compressed_score.clone(), subset_scores.len());
                        subset_scores.push(compressed_score);
                    }
                };
                break
            }
        }
    }
    Ok((subset_scores, indices_map))
}

/// Compress scores, exclusive
/// 
/// Extract a subset of genomes from a score list and generate a new score list
/// matching the genome subset. Exclude scores referencing genomes not in the
/// genome subset.
/// 
/// Parameters
/// ----------
/// supserset_scores : list
///     score list of the superset index
/// superset_genomes : list
///     genome list of the superset index
/// subset_genomes : list
///     genome list of the subset index
/// 
/// Returns
/// -------
/// list, dict
///     score list of the subset index, map from superset indices to subset
///     indices
#[pyfunction]
pub fn compress_scores_exclusive(superset_scores: ScoreList, superset_genomes: PKGenomes, subset_genomes: PKGenomes) -> PyResult<(ScoreList, IDXMap)> {
    let n_superset_genomes = superset_genomes.len();
    let n_subset_genomes = subset_genomes.len();
    let n_superset_bytes = (n_superset_genomes + 7) / 8;
    let n_subset_bytes = (n_subset_genomes + 7) / 8;
    let mut memberships: Vec<usize> = Vec::new();
    let mut exclusions: Vec<usize> = Vec::new();
    for (i, genome) in superset_genomes.iter().enumerate() {
        if subset_genomes.contains(&genome) {
            memberships.push(i);
        } else {
            exclusions.push(i);
        }
    }
    let mut indices_map: IDXMap = HashMap::default();
    let mut subset_scores = ScoreList::new();
    let mut score_to_idx: ScoreToIDX = HashMap::default();
    'sup_scores: for (key, score) in superset_scores.iter().enumerate() {
        let expanded_score: Vec<usize> = score_byte_to_blist(&score, n_superset_genomes)?;
        for j in exclusions.iter() {
            if expanded_score[*j] == 1 { continue 'sup_scores; }
        }
        let mut compressed_score: Score = vec![0; n_subset_bytes];
        for (i, j) in memberships.iter().enumerate() {
            if expanded_score[*j] == 1 {
                let (byte_idx, bit_mask) = genome_index_to_byte_idx_and_bit_mask(i, n_subset_bytes);
                compressed_score[byte_idx] = compressed_score[byte_idx] | bit_mask;
            }
        }
        for compressed_byte in compressed_score.iter() {
            if compressed_byte > &0u8 {
                match score_to_idx.get(&compressed_score){
                    Some(idx) => { indices_map.insert(key as u64, *idx); },
                    None => {
                        indices_map.insert(key as u64, subset_scores.len());
                        score_to_idx.insert(compressed_score.clone(), subset_scores.len());
                        subset_scores.push(compressed_score);
                    }
                };
                break
            }
        }
    }
    Ok((subset_scores, indices_map))
}

/// Subset scores to file
/// 
/// Given a superset index and a genome subset, generate a score list
/// (either inclusive or exclusive) for the subset index. Write the subsetted
/// scores to a file.
/// 
/// Parameters
/// ----------
/// idx_dir : str
///     path to directory or tarfile containing the superset index
/// tar_file: str
///     if the input index is a tar file, path to the file. Otherwise,
///     empty string
/// superset_genomes : list
///     genome list of the superset index
/// subset_genomes : list
///     genome list of the subset index
/// outpath : str
///     path to output file
/// exclusive : bool
///     if True, perform an exclusive subset
/// 
/// Returns
/// -------
/// dict
///     map from superset indices to subset indices
#[pyfunction]
pub fn subset_scores_to_file(idx_dir: &str, tar_file: &str,
                             superset_genomes: PKGenomes,
                             subset_genomes: PKGenomes,
                             outpath: &str,
                             exclusive: bool) -> PyResult<IDXMap> {
    let superset_scores = load_scores(idx_dir, tar_file)?;
    let (compressed_scores, idx_map) = match exclusive {
        false => compress_scores(superset_scores, superset_genomes, subset_genomes)?,
        true => compress_scores_exclusive(superset_scores, superset_genomes, subset_genomes)?
    };
    dump_scores(compressed_scores, &outpath)?;
    Ok(idx_map)
}

/// Subset scores to list
/// 
/// Given a superset index and a genome subset, generate a score list
/// (either inclusive or exclusive) for the subset index. Return the subsetted
/// score list
/// 
/// Parameters
/// ----------
/// idx_dir : str
///     path to directory or tarfile containing the superset index
/// tar_file: str
///     if the input index is a tar file, path to the file. Otherwise,
///     empty string
/// superset_genomes : list
///     genome list of the superset index
/// subset_genomes : list
///     genome list of the subset index
/// exclusive : bool
///     if True, perform an exclusive subset
/// 
/// Returns
/// -------
/// list, dict
///     score list, map from superset indices to subset indices
#[pyfunction]
pub fn subset_scores_to_list(idx_dir: &str, tar_file: &str,
                             superset_genomes: PKGenomes,
                             subset_genomes: PKGenomes,
                             exclusive: bool) -> PyResult<(ScoreList, IDXMap)> {
    let superset_scores = load_scores(idx_dir, tar_file)?;
    let (compressed_scores, idx_map) = match exclusive {
        false => compress_scores(superset_scores, superset_genomes, subset_genomes)?,
        true => compress_scores_exclusive(superset_scores, superset_genomes, subset_genomes)?
    };
    Ok((compressed_scores, idx_map))
}