# curatedMetagenomicDataExtractor
Scripts for extracting raw CSV files from curatedMetagenomicData for use in other applications.

# Instructions

## Prerequisites

1) You must have R along with the [curatedMetagenomicData](https://github.com/waldronlab/curatedMetagenomicData) package installed. From within an R terminal, you can type:
            
            install.packages("BiocManager")
            BiocManager::install("curatedMetagenomicData")

2) Install additional R dependencies:
   
            install.packages("stringr")

3) Install python dependencies:
   
        pip install -r requirements.txt

## Extraction

To download the dataset, run

        Rscript curatedmetagenomicdataextractor/download/download_dataset.R path_to_download_folder
    
Where you replace `path_to_download_folder` with the path to the folder where you wish to download the extracted files.


## Upload to Cloud Storage


# Pre-extracted Data
Instead of running these scripts, you can also download the extracted data directly from a public GCS bucket that we made. The CSVs are located at `gs://curatedmetagenomicdatasvs`