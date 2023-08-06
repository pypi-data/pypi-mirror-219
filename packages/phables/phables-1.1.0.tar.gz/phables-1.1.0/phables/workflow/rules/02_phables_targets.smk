
preprocessTargets = []
phablesTargets = []


"""PREPROCESSING TARGETS"""
EDGES_FILE = os.path.join(OUTDIR, "edges.fasta")
preprocessTargets.append(EDGES_FILE)

BAM_PATH = os.path.join(OUTDIR, 'temp')
preprocessTargets.append(expand(os.path.join(BAM_PATH, "{sample}.bam"), sample=SAMPLE_NAMES))
preprocessTargets.append(expand(os.path.join(BAM_PATH, "{sample}.bam.bai"), sample=SAMPLE_NAMES))

COVERAGE_PATH = os.path.join(OUTDIR, 'coverage_rpkm/')
# preprocessTargets.append(expand(os.path.join(COVERAGE_PATH, "{sample}_rpkm.tsv"), sample=SAMPLE_NAMES))
preprocessTargets.append(os.path.join(OUTDIR, "coverage.tsv"))
preprocessTargets.append(os.path.join(OUTDIR, "edges.fasta.hmmout"))

preprocessTargets.append(os.path.join(OUTDIR, "phrogs_annotations.tsv"))


"""MISC"""
COVERAGE_FILE = os.path.join(OUTDIR, 'coverage.tsv')
PHROG_ANNOT = os.path.join(OUTDIR, 'phrogs_annotations.tsv')
SMG_FILE = os.path.join(OUTDIR, 'edges.fasta.hmmout')
GRAPH_FILE = INPUT


"""PHABLES TARGETS"""
phablesTargets.append(os.path.join(OUTDIR, "resolved_genome_info.txt"))
phablesTargets.append(os.path.join(OUTDIR, "resolved_component_info.txt"))
phablesTargets.append(os.path.join(OUTDIR, "component_phrogs.txt"))
