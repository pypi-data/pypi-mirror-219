import pandas as pd


class Species:
    def __init__(self, species_name: str, num_reads: int):
        self.species_name = species_name
        self.num_reads = num_reads


class Phylum:
    def __init__(self):
        self.phylum_list = []

    def populate_species_abundance(self, file: str) -> None:
        df = pd.read_csv(file)
        for index, row in df.iterrows():
            if row['reads'] > 0 and not pd.isna(row['phylum']) and not pd.isna(row['species']):
                phylum_name = row['phylum'].replace('p__', '')
                species_name = row['species'].replace('s__', '')
                num_reads = row['reads']

                phylum_dict = next((item for item in self.phylum_list if item["phylum_name"] == phylum_name), None)
                if not phylum_dict:
                    phylum_dict = {"phylum_name": phylum_name, "species_list": []}
                    self.phylum_list.append(phylum_dict)

                species_obj = Species(species_name, num_reads)
                phylum_dict['species_list'].append(species_obj)


class SpeciesAbundance:
    def __init__(self, file: str):
        self.phylo = Phylum()
        self.phylo.populate_species_abundance(file)
