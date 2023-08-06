import pandas as pd
import warnings


class EggNOG:
    """Class to represent the eggNOG data."""

    def __init__(self):
        """
        Constructor method.
        """
        self.data_dict = {}  # { gene: [{id_gene: integer, gene: string, phylum: string}, ...] }

    def populate_from_file(self, file: str) -> None:
        """
        Method to populate the data from a tab-separated file.

        Args:
            file (str): Path to the file.
        """
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            df = pd.read_csv(file, sep="\t", header=None, low_memory=False)
        id_counter = 1
        for index, row in df.iterrows():
            gene = row[8].lower()  # Preferred_name
            eggnog = row[4]  # eggNOG_OGs
            if gene == '-' or 'unclassified Bacteria' in eggnog or eggnog.count('@') < 3 or eggnog.count('@1|root') > 1:
                continue
            phylum = eggnog.split(',')[2]  # Get content between second and third comma
            phylum = phylum.split('|')[-1]  # Get content after last '|'
            if gene not in self.data_dict:
                self.data_dict[gene] = []
            self.data_dict[gene].append({'id_gene': id_counter, 'gene': gene, 'phylum': phylum})
            id_counter += 1
