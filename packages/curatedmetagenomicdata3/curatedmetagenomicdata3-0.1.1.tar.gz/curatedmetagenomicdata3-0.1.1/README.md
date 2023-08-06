# curatedMetagenomicData3-python

Python Wrapper for curatedMetagenomicData3

# Installation

    pip install curatedmetagenomicdata3

# Usage

## Pre-requisites

    # Decide on a folder to store files in
    # This package downloads files containing raw annotation data based on your queries

    import curatedmetagenomicdata3 as cmd3
    source_dir = "test"

## 1) Open Metadata

    # This function returns a DataFrame containing all sample metadata
    df = cmd3.get_metadata()

## 2) Decide What Samples You Want Annotations for

    # For example, let's say you want to download taxonomic relative 
    # abundances data for all samples for Type 2 Diabetes patients

    t2d = df[df['disease'] == 'T2D']

## 3) Compile OTU Data for Chosen Samples

    # Taxonomic Relative Abundances
    taxa = assemble_taxa_dataset(t2d, source_dir)

That's it! `taxa` will be a dataframe containing the relative abundances data for the samples you chose. All of the data for that will be downloaded and cached to `source_dir` automatically for future use.

You can also get pathway abundances as well

    # Pathway Relative Abundances
    pathways = assemble_pathways_dataset(t2d, source_dir)