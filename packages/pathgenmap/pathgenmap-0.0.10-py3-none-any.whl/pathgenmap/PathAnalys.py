import pandas as pd


class Pathway:
    """Class to represent a single pathway."""

    def __init__(self, fdr: float, ng: int, pg: int, fe: float, path_name: str, url: str, genes_list: str):
        """
        Constructor method.

        Args:
            fdr (float): False Discovery Rate for the pathway.
            ng (int): Number of genes for the pathway.
            pg (int): Total genes in the pathway.
            fe (float): Fold enrichment for the pathway.
            path_name (str): The name of the pathway.
            url (str): The URL of the pathway.
            genes_list (str): A comma-separated string of genes in the pathway.
        """
        self.fdr = fdr
        self.ng = ng
        self.pg = pg
        self.fe = fe
        self.path_name = path_name
        self.url = url
        self.genes_list = genes_list.split(",")  # Transforming the string of genes into a list.


class PathwaysList:
    """Class to handle a list of pathways."""

    def __init__(self):
        """Constructor method."""
        self.pathways_list = []

    def populate_from_file(self, file: str) -> None:
        """
        Method to populate the pathways list from a CSV file.

        Args:
            file (str): Path to the CSV file.
        """
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            if not pd.isna(row['Enrichment FDR']) and not pd.isna(row['nGenes']) and not pd.isna(
                    row['Pathway Genes']) and not pd.isna(row['Fold Enrichment']) and not pd.isna(
                    row['Pathway']) and not pd.isna(row['URL']) and not pd.isna(row['Genes']):
                pathway_obj = Pathway(row['Enrichment FDR'], row['nGenes'], row['Pathway Genes'],
                                      row['Fold Enrichment'], row['Pathway'], row['URL'], row['Genes'])
                self.pathways_list.append(pathway_obj)

