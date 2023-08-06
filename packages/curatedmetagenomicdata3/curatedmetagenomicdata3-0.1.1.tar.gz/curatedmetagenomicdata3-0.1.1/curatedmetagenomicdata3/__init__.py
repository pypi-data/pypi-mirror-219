import pandas as pd
import pkg_resources
import os
from tqdm import tqdm
from multiprocessing import Pool
from more_itertools import divide
from functools import partial
from scipy import sparse
from google.cloud import storage

def get_metadata():
    """ Returns sample metadata. """
    stream = pkg_resources.resource_stream(__name__, 'assets/sampleMetadata.pickle')
    df = pd.read_pickle(stream)
    # Assign a unique ID
    df.index = [f"{row['study_name']}_{row['sample_id']}" for _, row in df.iterrows()]

    return df

def assemble_taxa_dataset(df: pd.DataFrame, source_dir: str, pool_size=6, redownload=False) -> pd.DataFrame:
    """
    Given a slice of the metadata dataframe, returns a dataset of the underlying annotations.
    """
    stream = pkg_resources.resource_stream(__name__, 'assets/taxa.txt')
    taxa = pd.read_csv(stream, encoding='utf-8', index_col=0, header=None).sort_index().index

    annotation_type = 'relative_abundance'
    filenames = df.apply(lambda row: os.path.join(source_dir, f"{row['study_name']}_{annotation_type}_{row['sample_id']}.csv"),axis=1).values

    # Download files that are missing as needed
    to_download = [f for f in filenames if not os.path.exists(f)]
    if redownload:
        to_download = filenames

    if len(to_download):
        print(f"Need to download {len(to_download)} annotation files to fulfill query...")
        for filename in tqdm(to_download):
            print(f"Downloading annotation for {filename}")
            download_annotation(source_dir, filename.split("/")[-1])
            
    with Pool(pool_size) as p:
        dataset = p.map(partial(pd.read_csv, index_col=0, header=None), filenames)

    dataset = pd.concat([d.reindex(taxa).fillna(0).sort_index() for d in dataset], axis=1)
    # Reset column names based on concatenated study_name + sample_id
    dataset.columns = [f"{row['study_name']}_{row['sample_id']}" for _, row in df.iterrows()]    
    return dataset

def parse_pathways(pathways: pd.Index):
    """
    Generates pathways.txt and pathways.csv
    """
    pathways = pd.DataFrame(index=pathways)
    pathways['Pathway'] = pathways.index.map(lambda x: x.split('|')[0])
    pathways['Taxa'] = pathways.index.map(lambda x: x.split('|')[1] if '|' in x else None)
    pathways.to_csv('pathways.csv')
    with open('pathways.txt', 'w') as f:
        f.writelines(f'{x}\n' for x in tqdm(pathways.index))

def assemble_pathway_dataset(df: pd.DataFrame, source_dir: str, pool_size=6, redownload=False) -> pd.DataFrame:
    """
    Given a slice of the metadata dataframe, returns a dataset of the underlying annotations.
    """

    stream = pkg_resources.resource_stream(__name__, 'assets/pathways.csv')
    pathways = pd.read_csv(stream,index_col=0, header=None).sort_index().index

    annotation_type = 'pathway_abundance'

    filenames = df.apply(lambda row: os.path.join(source_dir, f"{row['study_name']}_{annotation_type}_{row['sample_id']}.csv"),axis=1).values

    # Download files that are missing as needed
    to_download = [f for f in filenames if not os.path.exists(f)]
    if redownload:
        to_download = filenames

    if len(to_download):
        print(f"Need to download {len(to_download)} annotation files to fulfill query...")

        for filename in tqdm(to_download):
            print(f"Downloading annotation for {filename}")
            download_annotation(source_dir, filename.split("/")[-1])

    shape = (len(pathways), len(filenames))
    dataset = sparse.lil_matrix(shape)
    i = 0
    for f in tqdm(filenames):
        try:
            d = pd.read_csv(f,index_col=0)
            d = d.reindex(pathways).fillna(0).sort_index()
            # dataset = dataset.append(d)
            dataset[:,i] = d
            i += 1
        except:
            print(f"Error for {f}")
            pass

    # Reset column names based on concatenated study_name + sample_id
    dataset = pd.DataFrame.sparse.from_spmatrix(dataset)
    dataset.index = pathways
    dataset.columns = [f"{row['study_name']}_{row['sample_id']}" for _, row in df.iterrows()]
    dataset.index.name = 'Pathway'
    return dataset

def download_annotation(directory: str, filename: str):
    """
    Downloads a single annotation file to the chosen directory.
    """
    bucket_name = 'curatedmetagenomicdata3-python'
    destination_file_name = os.path.join(directory,filename)
    client = storage.Client.create_anonymous_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(f"cmd_11_02_22_normalized/{filename}")
    blob.download_to_filename(destination_file_name)