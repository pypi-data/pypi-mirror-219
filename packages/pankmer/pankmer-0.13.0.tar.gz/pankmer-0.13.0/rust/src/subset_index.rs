use std::fs;
use std::io::{Read, Write, BufReader, BufWriter, ErrorKind};
use std::path::{Path, PathBuf};
use std::iter::zip;
use niffler;
use pyo3::prelude::*;
use crate::{K, VERSION, Kmer, PKGenomes, GZIP_LEVELS, IDXMap};
use crate::metadata::{PKMeta, load_metadata};
use crate::score_list_io::{subset_scores_to_file, load_scores};

#[pyfunction]
pub fn subset(idx_dir: &str, tar_file: &str, subset_genomes: PKGenomes,
              outdir: &str, gzip_level: usize, exclusive: bool) -> PyResult<()> {
    let mut metadata = PKMeta::new();
    let mut subset_genomes_ordered = Vec::new();
    const kmer_bitsize: usize =  (K * 2 + 7) / 8;
    const i_bitsize: usize = 8;
    let output_is_tar: bool = outdir.ends_with(".tar");
    match fs::create_dir(outdir) {
        Ok(_) => (),
        Err(_) => match Path::new(outdir).is_dir() {
            true => (),
            false => panic!("Could not create dir and dir does not exist")
        }
    };
    let superset_meta: PKMeta = load_metadata(idx_dir, tar_file)?;
    metadata.mem_blocks = superset_meta.mem_blocks;
    let n_superset_genomes = superset_meta.genomes.len();
    let mut superset_genomes: PKGenomes = Vec::new();
    for i in 0..n_superset_genomes {
        let genome = superset_meta.genomes.get(&i).expect("could not get genome name");
        superset_genomes.push(genome.to_string());
        if subset_genomes.contains(genome) {
            subset_genomes_ordered.push(genome.to_string());
        }
    }
    for (i, g) in subset_genomes_ordered.iter().enumerate() {
        let size = superset_meta.genome_sizes.get(g).expect("could not get genome size");
        metadata.genome_sizes.insert(g.to_string(), *size);
        metadata.genomes.insert(i, g.to_string());
    }
    let idx_map: IDXMap = subset_scores_to_file(&idx_dir, &tar_file,
        superset_genomes, subset_genomes, &format!("{outdir}/scores.pks"),
        exclusive)?;
    let mut kmers_out_path = PathBuf::from(&outdir);
    kmers_out_path.push("kmers.bgz");
    let mut indices_out_path = PathBuf::from(&outdir);
    indices_out_path.push(format!("indices.bgz"));
    const kmer_bufsize: usize = 1000*kmer_bitsize;
    const i_bufsize: usize = 8000;
    let mut kmers_out = BufWriter::with_capacity(kmer_bufsize, niffler::to_path(kmers_out_path, niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing"));
    let mut indices_out = BufWriter::with_capacity(i_bufsize, niffler::to_path(indices_out_path, niffler::compression::Format::Gzip, GZIP_LEVELS[gzip_level]).expect("Can't open file for writing"));
    let mut count = 0;
    let mut kmer_buf = [0; kmer_bitsize];
    let mut i_buf = [0; i_bitsize];
    let mut kmers_in_path: PathBuf = PathBuf::from(&idx_dir);
    kmers_in_path.push(format!("kmers.bgz"));
    let mut indices_in_path: PathBuf = PathBuf::from(&idx_dir);
    indices_in_path.push(format!("indices.bgz"));
    let (mut kmers_reader, _format) = niffler::from_path(&kmers_in_path).expect("File not found");
    let (mut i_reader, _format) = niffler::from_path(&indices_in_path).expect("File not found");
    let mut kmers_in = BufReader::with_capacity(kmer_bufsize, kmers_reader);
    let mut i_in = BufReader::with_capacity(i_bufsize, i_reader);
    loop {
        let kmers = match kmers_in.read_exact(&mut kmer_buf) {
            Ok(_) => kmer_buf.chunks(kmer_bitsize).map(|bytes| u64::from_be_bytes(bytes.try_into().unwrap())).collect::<Vec<u64>>(),
            Err(ref e) if e.kind() == ErrorKind::UnexpectedEof => break,
            // Err(ref e) if e.kind() == ErrorKind::Interrupted => continue,
            Err(e) => panic!("{:?}", e),
        };
        let idxs = match i_in.read_exact(&mut i_buf) {
            Ok(_) => i_buf.chunks(i_bitsize).map(|bytes| u64::from_be_bytes(bytes.try_into().unwrap())).collect::<Vec<u64>>(),
            Err(ref e) if e.kind() == ErrorKind::UnexpectedEof => break,
            // Err(ref e) if e.kind() == ErrorKind::Interrupted => continue,
            Err(e) => panic!("{:?}", e),
        };
        let iter = zip(kmers, idxs);
        for (kmer, idx) in iter{
            match idx_map.get(&idx) {
                Some(i) => {
                    kmers_out.write(&kmer.to_be_bytes()[8-kmer_bitsize..]).unwrap();
                    indices_out.write(&i.to_be_bytes()).unwrap();
                },
                None => { continue; }
            };
            if count % 10000000 == 0 && count != 0 {
                metadata.positions.insert(kmer.to_string(), count);
                count == 0;
            }
            count += 1;
        }
    }
    kmers_out.flush().unwrap();
    indices_out.flush().unwrap();
    let mut meta_out_path = PathBuf::from(&outdir);
    meta_out_path.push("metadata.json");
    let meta_out = fs::File::create(&meta_out_path).expect(
        "Can't open file for writing"
    );
    serde_json::to_writer(&meta_out, &metadata).expect(
        "Couldn't write PKMeta to file"
    );
    Ok(())
}
