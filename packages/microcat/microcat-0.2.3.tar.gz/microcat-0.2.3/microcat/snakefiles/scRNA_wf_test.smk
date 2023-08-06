#!/usr/bin/env snakemake

import sys
from snakemake.utils import min_version
import os
import numpy as np
import pandas as pd

import microcat
MICROCAT_DIR = microcat.__path__[0]

wildcard_constraints:
    # Patient = "[a-zA-Z0-9_]+", # Any alphanumeric characters and underscore
    # tissue = "S[0-9]+",  # S followed by any number
    lane = "L[0-9]{3}",  # L followed by exactly 3 numbers
    plate = "P[0-9]{3}",  # L followed by exactly 3 numbers
    library = "[0-9]{3}"  # Exactly 3 numbers


min_version("7.0")
shell.executable("bash")

class ansitxt:
    RED = '\033[31m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def warning(msg):
    print(f"\n{ansitxt.BOLD}{ansitxt.RED}{msg}{ansitxt.ENDC}\n",file=sys.stderr)

def parse_samples_test(sample_tsv, platform):
    samples_df = pd.read_csv(sample_tsv, sep="\t")
    
    # Check if id, fq1, fq2 columns exist
    if not set(['id', 'fq1', 'fq2']).issubset(samples_df.columns):
        raise ValueError("Columns 'id', 'fq1', 'fq2' must exist in the sample.tsv")
    
    # Extract library, lane, and plate from id
    samples_df[['patient_tissue_lane_plate', 'library']] = samples_df['id'].str.rsplit("_", n=1, expand=True)
    
    # Determine the platform and parse accordingly
    if platform == 'plate':
        samples_df['is_lane'] = samples_df['patient_tissue_lane_plate'].apply(lambda x: x.split('_')[-1].startswith("L"))
        samples_df.loc[samples_df['is_lane'], 'lane'] = samples_df['patient_tissue_lane_plate'].apply(lambda x: x.split('_')[-1])
        # Extract patient and tissue, using the fact that tissue is always "S" followed by a number
        # and is always the last part in patient_tissue
        samples_df['patient_tissue'] = samples_df['patient_tissue_lane_plate'].apply(lambda x: '_'.join(x.split('_')[:-1]))
        samples_df['tissue'] = samples_df['patient_tissue'].apply(lambda x: x.split('_')[-1])
        samples_df['patient'] = samples_df['patient_tissue'].apply(lambda x: '_'.join(x.split('_')[:-1]))
        samples_df = samples_df.drop(columns=['patient_tissue_lane_plate'])
    elif platform == 'plate':
        samples_df['is_plate'] = samples_df['patient_tissue_lane_plate'].apply(lambda x: x.split('_')[-1].startswith("P"))
        samples_df.loc[samples_df['is_plate'], 'plate'] = samples_df['patient_tissue_lane_plate'].apply(lambda x: x.split('_')[-1])
        samples_df['patient_tissue_cell'] = samples_df['patient_tissue_lane_plate'].apply(lambda x: '_'.join(x.split('_')[:-1]))
        # Extract patient and tissue, using the fact that tissue is always "S" followed by a number
        # and is always the last part in patient_tissue
        samples_df['tissue'] = samples_df['patient_tissue_cell'].str.extract(r'(S\d+)_')
        # 提取patient和cell
        samples_df[['patient', 'cell']] = samples_df['patient_tissue_cell'].str.extract(r'(.+)_S\d+_(.+)')
        samples_df = samples_df.drop(columns=['patient_tissue_lane_plate'])
        samples_df = samples_df.drop(columns=['patient_tissue_cell'])
        samples_df['patient_tissue'] = samples_df['patient'] + '_' + samples_df['tissue']
    else:
        raise ValueError("Platform must be either 'lane' or 'plate'")


    if samples_df[['patient_tissue', 'library']].isnull().values.any():
        raise ValueError(f"id column must follow the format '{{Patient}}_{{tissue}}_{{lane or plate}}_{{library}}' for platform {platform}")
    
    # Create sample identifier
    samples_df['sample_id'] = samples_df['patient_tissue']
    
    # Check if sample names contain "."
    if samples_df['sample_id'].str.contains("\\.").any():
        raise ValueError("Sample names must not contain '.', please remove '.'")
    
    # Determine if the sequencing is paired-end or single-end
    samples_df['seq_type'] = 'single-end'
    samples_df.loc[samples_df['fq2'].notnull(), 'seq_type'] = 'paired-end'
    
    # Create a 'fastqs_dir' column that contains the directory of the fastq files
    samples_df['fastqs_dir'] = samples_df['fq1'].apply(lambda x: '/'.join(x.split('/')[:-1]))
    
    # Set index
    if platform == 'tenX':
        samples_df = samples_df.set_index(["sample_id","patient", "tissue", "lane", "library"])
    elif platform == 'smartseq':
        samples_df = samples_df.set_index(["sample_id","patient", "cell","tissue", "plate", "library"])

    return samples_df

def get_SAMattrRGline_by_plate(samples_df, plate):
    # Filter samples based on the plate value
    samples_plate = samples_df.loc[samples_df['plate'] == plate]

    # Get the sample IDs for the filtered samples
    sample_ids = samples_plate.index.get_level_values("sample_id").unique()

    # Generate the --outSAMattrRGline input format
    rgline = " , ".join([f"ID:{sample_id}" for sample_id in sample_ids])
    return rgline

# def get_SAMattrRGline_by_sample(samples_df, wildcards):
#     sample_id = wildcards.sample
#     # Filter samples based on the plate value
#     samples_cells = samples_df.loc[samples_df['sample_id'] == sample_id]

#     # Get the sample IDs for the filtered samples
#     cell_ids = samples_cells.index.get_level_values("cell").unique()

#     # Generate the --outSAMattrRGline input format
#     rgline = " , ".join([f"ID:{cell_id}" for cell_id in cell_ids])
#     return rgline
def get_SAMattrRGline_by_sample(samples_df, wildcards):
    sample_id = wildcards.sample

    # Filter samples based on sample_id and plate
    samples_filtered = samples_df.loc[(samples_df.index.get_level_values("sample_id") == sample_id)]

    # samples_filtered = samples_df.loc[(samples_df.index.get_level_values("sample_id") == sample_id) &
    #                                 (samples_df.index.get_level_values("plate") == plate)]

    # Get the cell IDs for the filtered samples
    cell_ids = samples_filtered.index.get_level_values("cell").unique()

    # Generate the --outSAMattrRGline input format
    rgline = " , ".join([f"ID:{cell_id}" for cell_id in cell_ids])
    return rgline


PLATFORM = None

if config["params"]["host"]["starsolo"]["do"]:
    if  config["params"]["host"]["starsolo"]["soloType"]=="CB_UMI_Simple":
        PLATFORM = "lane"
    elif config["params"]["host"]["starsolo"]["soloType"]=="SmartSeq":
        PLATFORM = "plate"
    elif config["params"]["host"]["starsolo"]["soloType"]=="CB_UMI_Complex":
        PLATFORM = "lane"
    else:
        raise ValueError("Platform must be either 'CB_UMI' or 'smartseq'")
elif config["params"]["host"]["cellranger"]["do"]:
    PLATFORM = "lane"
else:
    raise ValueError("Platform must be either 'lane' or 'plate'")




try:
    SAMPLES = parse_samples_test(config["params"]["samples"],platform = PLATFORM)
    SAMPLES_ID_LIST = SAMPLES.index.get_level_values("sample_id").unique()
    # CELL_LIST = SAMPLES.index.get_level_values("cell").unique()
    # PLATE_LIST = SAMPLES.index.get_level_values("plate").unique()
    print(SAMPLES)
except FileNotFoundError:
    warning(f"ERROR: the samples file does not exist. Please see the README file for details. Quitting now.")
    sys.exit(1)

rule all:
    input:
        # expand(os.path.join(config["output"]["host"],"unmapped_host/{sample}_{plate}/{cell}/Aligned_sortedByName_unmapped_out.bam"),sample=SAMPLES_ID_LIST,plate=PLATE_LIST,cell=CELL_LIST)
        expand(os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/Aligned_sortedByName_unmapped_out.bam"),sample=SAMPLES_ID_LIST)
        # os.path.join(
        #             config["output"]["host"],
        #             "starsolo_count/Aligned_out_unmapped_RGsorted.bam")

rule generate_pe_manifest_file:
    input:
        config["params"]["samples"],
    output:
        PE_MANIFEST_FILE = os.path.join("data", "{sample}-pe-manifest.tsv")
    script:
        "/data/project/host-microbiome/microcat/microcat/scripts/generate_PE_manifest_file.py"            

# rule starsolo_test:
#     # Input files
#     input:
#         # Path to the input manifest file
#         manifest = os.path.join("data", "manifest.tsv"),
#     output:
#         test = os.path.join("data", "test.txt"),
#     shell:
#         '''
#         cat {input.manifest} > {output.test}
#         '''
# rule starsolo_SmartSeq_count:
#     # Input files
#     input:
#         # Path to the input manifest file
#         manifest = os.path.join("data", "manifest.tsv"),
#     output:
#         # Path to the output features.tsv file
#         features_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/features.tsv"),
#         # Path to the output matrix.mtx file
#         matrix_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/matrix.mtx"),
#         # Path to the output barcodes.tsv file
#         barcodes_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/barcodes.tsv"),
#         # Path to the output unmapped fastq file for read1
#         # ummapped_fastq_1 = os.path.join(
#         #     config["output"]["host"],
#         #     "starsolo_count/Unmapped.out.mate1"),
#         # # Path to the output unmapped fastq file for read2
#         # ummapped_fastq_2 = os.path.join(
#         #     config["output"]["host"],
#         #     "starsolo_count/Unmapped.out.mate2"),
#         mapped_bam_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/Aligned_out.bam")
#     params:
#         # Path to the output directory
#         starsolo_out = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/"),
#         # Path to the STAR index directory
#         reference = config["params"]["host"]["starsolo"]["reference"],
#         # Type of sequencing library
#         soloType = config["params"]["host"]["starsolo"]["soloType"],
#         # SAMattrRGline = microcat.get_SAMattrRGline_from_manifest(config["params"]["host"]["starsolo"]["manifest"]),
#         # Additional parameters for STAR
#         variousParams = config["params"]["host"]["starsolo"]["variousParams"],
#         # Number of threads for STAR
#         threads = config["params"]["host"]["starsolo"]["threads"]
#     log:
#         os.path.join(config["logs"]["host"],
#                     "starsolo/starsolo_count_smartseq2.log")
#     benchmark:
#         os.path.join(config["benchmarks"]["host"],
#                     "starsolo/starsolo_count_smartseq2.benchmark")
#     conda:
#         config["envs"]["star"]
#     shell:
#         '''
#         mkdir -p {params.starsolo_out}; 
#         cd {params.starsolo_out} ;
#         STAR \
#         --soloType SmartSeq \
#         --genomeDir {params.reference} \
#         --readFilesManifest {input.manifest} \
#         --runThreadN {params.threads} \
#         --soloUMIdedup Exact \
#         --soloStrand Unstranded \
#         --outSAMtype BAM Unsorted\
#         --readFilesCommand zcat \
#         --outSAMunmapped Within \
#         --quantMode GeneCounts \
#         {params.variousParams}  \
#         2>&1 | tee ../.
#         ./../{log} ;
#         pwd ;\
#         cd ../../../;\
#         ln -sr "{params.starsolo_out}/Solo.out/Gene/filtered/features.tsv" "{output.features_file}" ;\
#         ln -sr "{params.starsolo_out}/Solo.out/Gene/filtered/matrix.mtx" "{output.matrix_file}" ; \
#         ln -sr "{params.starsolo_out}/Solo.out/Gene/filtered/barcodes.tsv" "{output.barcodes_file}" ;\
#         mv "{params.starsolo_out}/Aligned.out.bam" "{output.mapped_bam_file}";\
#         '''
# rule starsolo_SmartSeq_unmapped_extracted_sorted:
#     input:
#         mapped_bam_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/Aligned_out.bam")
#     output:
#         unmapped_bam_unsorted_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/Aligned_out_unmapped.bam")
#     params:
#         threads=16
#     conda:
#         config["envs"]["star"]
#     shell:
#         '''
#         samtools view --threads  {params.threads}  -b -f 4   {input.mapped_bam_file}  >  {output.unmapped_bam_unsorted_file};\
#         '''

# rule starsolo_SmartSeq_unmapped_sorted_bam:
#     input:
#         unmapped_bam_unsorted_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/Aligned_out_unmapped.bam")
#     output:
#         unmapped_sorted_bam = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/Aligned_out_unmapped_RGsorted.bam"),
#     params:
#         threads=40,
#         tag="RG"
#     log:
#         os.path.join(config["logs"]["host"],
#                     "starsolo/unmapped_sorted_bam.log")
#     benchmark:
#         os.path.join(config["benchmarks"]["host"],
#                     "starsolo/unmapped_sorted_bam.benchmark")
#     conda:
#         config["envs"]["star"]
#     shell:
#         '''
#         samtools sort -@ {params.threads} -t {params.tag} -o {output.unmapped_sorted_bam}  {input.unmapped_bam_unsorted_file};
#         '''

# checkpoint starsolo_smartseq_demultiplex_bam_by_read_group:
#     input:
#         unmapped_sorted_bam = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/Aligned_out_unmapped_RGsorted.bam")
#     output:
#         unmapped_bam_demultiplex_dir = directory(os.path.join(
#             config["output"]["host"],
#             "unmapped_host/"))
#     params:
#         threads = 40, # Number of threads
#         tag="RG"
#     conda:
#         config["envs"]["star"]
#     log:
#         os.path.join(
#             config["logs"]["host"],
#             "starsolo_count/demultiplex_bam_by_read_group.log")
#     benchmark:
#         os.path.join(
#             config["benchmarks"]["host"], 
#             "starsolo_count/demultiplex_bam_by_read_group.benchmark")
#     shell:
#         """
#         python /data/project/host-microbiome/microcat/microcat/scripts/spilt_bam_by_tag.py --tag {params.tag} --bam_path {input.unmapped_sorted_bam} --output_dir {output.unmapped_bam_demultiplex_dir}  --log_file {log}
#         """
# split the PathSeq BAM into one BAM per cell barcode
# rule split_starsolo_BAM_by_RG:
#     input:
#         unmapped_sorted_bam = os.path.join(
#                 config["output"]["host"],
#                 "starsolo_count/Aligned_out_unmapped_RGsorted.bam")
#     output:
#         unmapped_bam_sorted_file =os.path.join(
#             config["output"]["host"],
#             "unmapped_host/{sample}/Aligned_sortedByName_unmapped_out.bam")
#     params:
#         SampleID="{sample}",
#     shell:
#         '''
#         python /data/project/host-microbiome/microcat/microcat/scripts/split_Starsolo_BAM_by_RG.py \
#         --bam_path {input.unmapped_sorted_bam} \
#         --tag {params.SampleID} \
#         --output_bam {output.unmapped_bam_sorted_file} 
#         '''
rule starsolo_smartseq_count:
    # Input files
    input:
        # Path to the input manifest file
        manifest = os.path.join("data", "{sample}-pe-manifest.tsv"),
    output:
        # Path to the output features.tsv file
        features_file = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/features.tsv"),
        # Path to the output matrix.mtx file
        matrix_file = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/matrix.mtx"),
        # Path to the output barcodes.tsv file
        barcodes_file = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/barcodes.tsv"),
        mapped_bam_file = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/Aligned_out.bam")
    params:
        # Path to the output directory
        starsolo_out = os.path.join(
            config["output"]["host"],
            "starsolo_count/"),
        # Path to the STAR index directory
        reference = config["params"]["host"]["starsolo"]["reference"],
        SAMattrRGline = lambda wildcards: get_SAMattrRGline_by_sample(SAMPLES, wildcards),
        # Additional parameters for STAR
        variousParams = config["params"]["host"]["starsolo"]["variousParams"],
        # Number of threads for STAR
        threads = config["params"]["host"]["starsolo"]["threads"]
    log:
        os.path.join(config["logs"]["host"],
                    "starsolo/{sample}/starsolo_count_smartseq2.log")
    benchmark:
        os.path.join(config["benchmarks"]["host"],
                    "starsolo/{sample}/starsolo_count_smartseq2.benchmark")
    conda:
        config["envs"]["star"]
    shell:
        '''
        mkdir -p {params.starsolo_out}; 
        cd {params.starsolo_out} ;
        STAR \
        --soloType SmartSeq \
        --genomeDir {params.reference} \
        --readFilesManifest ../../../{input.manifest} \
        --runThreadN {params.threads} \
        --soloUMIdedup Exact \
        --soloStrand Unstranded \
        --outSAMtype BAM Unsorted\
        --outSAMattrRGline {params.SAMattrRGline} \
        --readFilesCommand zcat \
        --outSAMunmapped Within \
        --quantMode GeneCounts \
        {params.variousParams}  \
        2>&1 | tee ../../../{log} ;
        pwd ;\
        cd ../../../;\
        ln -sr "{params.starsolo_out}/Solo.out/Gene/filtered/features.tsv" "{output.features_file}" ;\
        ln -sr "{params.starsolo_out}/Solo.out/Gene/filtered/matrix.mtx" "{output.matrix_file}" ; \
        ln -sr "{params.starsolo_out}/Solo.out/Gene/filtered/barcodes.tsv" "{output.barcodes_file}" ;\
        mv "{params.starsolo_out}/Aligned.out.bam" "{output.mapped_bam_file}";\
        '''


rule starsolo_smartseq_extracted:
    input:
        mapped_bam_file = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/Aligned_out.bam")
    output:
        unmapped_bam_unsorted_file = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/Aligned_out_unmapped.bam")
    params:
        threads=16
    conda:
        config["envs"]["star"]
    shell:
        '''
        samtools view --threads  {params.threads}  -b -f 4   {input.mapped_bam_file}  >  {output.unmapped_bam_unsorted_file}
        '''

# rule starsolo_smartseq_unmapped_sorted_bam:
#     input:
#         unmapped_bam_unsorted_file = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/{sample}/Aligned_out_unmapped.bam")
#     output:
#         unmapped_sorted_bam = os.path.join(
#             config["output"]["host"],
#             "starsolo_count/{sample}/Aligned_out_unmapped_RGsorted.bam"),
#     params:
#         threads=40,
#         tag="RG"
#     log:
#         os.path.join(config["logs"]["host"],
#                     "starsolo/{sample}/unmapped_sorted_bam.log")
#     benchmark:
#         os.path.join(config["benchmarks"]["host"],
#                     "starsolo/{sample}/unmapped_sorted_bam.benchmark")
#     conda:
#         config["envs"]["star"]
#     shell:
#         '''
#         samtools sort -@ {params.threads} -t {params.tag} -o {output.unmapped_sorted_bam}  {input.unmapped_bam_unsorted_file};
#         '''
rule starsolo_smartseq_unmapped_sorted_bam:
    input:
        unmapped_bam_unsorted_file = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/Aligned_out_unmapped.bam")
    output:
        unmapped_sorted_bam = os.path.join(
            config["output"]["host"],
            "starsolo_count/{sample}/Aligned_sortedByName_unmapped_out.bam"),
    params:
        threads=40,
        tag="RG"
    log:
        os.path.join(config["logs"]["host"],
                    "starsolo/{sample}/unmapped_sorted_bam.log")
    benchmark:
        os.path.join(config["benchmarks"]["host"],
                    "starsolo/{sample}/unmapped_sorted_bam.benchmark")
    conda:
        config["envs"]["star"]
    shell:
        '''
        samtools sort -n  --threads  {params.threads} {input.unmapped_bam_unsorted_file} -o {output.unmapped_sorted_bam}
        '''
# rule split_starsolo_BAM_by_RG:
#     input:
#         unmapped_sorted_bam = os.path.join(
#                 config["output"]["host"],
#                 "starsolo_count/{sample}_{plate}/Aligned_out.bam"),
#     output:
#         unmapped_bam_sorted_file =os.path.join(
#             config["output"]["host"],
#             "unmapped_host/{sample}_{plate}/{cell}/Aligned_sortedByName_unmapped_out.bam")
#     # params:
#     #     SampleID="{sample}",
#     # shell:
#     #     '''
#     #     python /data/project/host-microbiome/microcat/microcat/scripts/split_Starsolo_BAM_by_RG.py \
#     #     --bam_path {input.unmapped_sorted_bam} \
#     #     --tag {params.SampleID} \
#     #     --output_bam {output.unmapped_bam_sorted_file} 
#     #     '''
#     script:
#         "../src/split_PathSeq_BAM_by_CB_UB.py"


# rule all:
#     input:
#         # os.path.join(
#         #     config["output"]["host"],
#         #     "starsolo_count/Aligned_out.bam")
#         expand(os.path.join(
#             config["output"]["host"],
#             "unmapped_host/{sample}/Aligned_sortedByName_unmapped_out.bam"),sample=SAMPLES_ID_LIST)




