import os
import gzip
import shutil
import urllib.request
from ftplib import FTP
from urllib.parse import urlparse

from Bio import Entrez

Entrez.email = os.getenv('ENTREZ_EMAIL')

def _ftp_file_exists(ftp_url: str, file_name: str):
    url_parts = urlparse(ftp_url)
    server_address = url_parts.netloc
    file_path = url_parts.path
    try:
        ftp = FTP(server_address)
        ftp.login()

        ftp.cwd(file_path)
        file_list = ftp.nlst()
        file_exists = file_name in file_list

        ftp.quit()

        return file_exists

    except Exception as e:
        print(f'Error checking FTP file existence: {str(e)}')
        return False

def _create_folder_if_not_exist(acession_number:str):
    temp_genomes_path = os.path.join(
        os.getcwd(), 'temp_genomes', f'results_{acession_number}'
    )

    if not os.path.exists(temp_genomes_path):
        os.makedirs(temp_genomes_path)
    
    return temp_genomes_path

def _get_id_by_acession_number(acession_number, database = 'assembly'):
    handle = Entrez.esearch(
        db=database,
        term=f'{acession_number}[Assembly Accession]',
        retmax=1,
    )

    record = Entrez.read(handle)
    handle.close()

    if not record['IdList']:
        raise ValueError(
            'Assembly not found for the given accession number.'
        )

    assembly_id = record['IdList'][0]

    return assembly_id

def _get_summary_by_id(organism_id):
    handle = Entrez.esummary(db='assembly', id=organism_id)
    record = Entrez.read(handle)

    handle.close()

    return record

def _get_full_organims_name(summary):
    return summary['DocumentSummarySet']['DocumentSummary'][
            0
        ]['SpeciesName']

def _get_ftp_url(summary):
    ftp_url = summary['DocumentSummarySet']['DocumentSummary'][0].get(
            'FtpPath_RefSeq'
    )
    
    if not ftp_url:
        ftp_url = summary['DocumentSummarySet']['DocumentSummary'][0].get(
            'FtpPath_GenBank'
        )

        if not ftp_url:
            raise ValueError(
                'No FTP path found for the given accession number.'
            )
    
    return ftp_url

def download_fasta_sequence_by_id(acession_number: str):
    try:
        assembly_id = _get_id_by_acession_number(acession_number, database='assembly')

        record = _get_summary_by_id(assembly_id)

        full_organism_name = _get_full_organims_name(record)

        ftp_url = _get_ftp_url(record)

        fasta_file = ftp_url.split('/')[-1] + '_protein.faa.gz'

        fasta_url = ftp_url + '/' + fasta_file

        if not _ftp_file_exists(ftp_url=ftp_url, file_name=fasta_file):
            raise ValueError(f'File {fasta_file} not found on the FTP server.')

        temp_genomes_path = _create_folder_if_not_exist(acession_number)

        fasta_folder_path = os.path.join(
            temp_genomes_path, f'{acession_number}.fasta.gz'
        )

        if not os.path.exists(fasta_folder_path):
            urllib.request.urlretrieve(fasta_url, fasta_folder_path)

        fasta_output_path = os.path.join(
            temp_genomes_path, f'{acession_number}.faa'
        )

        with gzip.open(fasta_folder_path, 'rb') as f_in:
            with open(fasta_output_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)


        return fasta_output_path, full_organism_name, False

    except Exception as error:
        return False, False, str(error)
