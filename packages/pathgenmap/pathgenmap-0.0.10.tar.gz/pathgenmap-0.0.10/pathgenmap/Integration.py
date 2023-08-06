import pandas as pd
from .PathAnalys import PathwaysList
from .EggAnnot import EggNOG
from .SpeciesAbundance import SpeciesAbundance
from tqdm import tqdm


class Manager:
    def __init__(self):
        self.abundance = None
        self.eggnog = None
        self.pathways = None
        self.pathway_gene_species_list = []
        self.id_path = 0

    def integrate_data(self, pathways_file: str, eggnog_file: str, species_abundance_file: str) -> None:
        for _ in tqdm(range(4), desc="Processing files..."):
            if _ == 0:
                self.process_pathways(pathways_file)
            elif _ == 1:
                self.process_eggnog(eggnog_file)
            elif _ == 2:
                self.process_species_abundance(species_abundance_file)
            else:
                self.integrate_all()
        self.to_csv()

    def process_pathways(self, pathways_file: str) -> None:
        self.pathways = PathwaysList()
        self.pathways.populate_from_file(pathways_file)

    def process_eggnog(self, eggnog_file: str) -> None:
        self.eggnog = EggNOG()
        self.eggnog.populate_from_file(eggnog_file)

    def process_species_abundance(self, species_abundance_file: str) -> None:
        self.abundance = SpeciesAbundance(species_abundance_file)

    def integrate_all(self) -> None:
        for pathway in self.pathways.pathways_list:
            for gene_string in pathway.genes_list:
                genes = gene_string.split()
                for gene in genes:
                    gene = gene.lower()  # Convert gene to lowercase
                    if gene in self.eggnog.data_dict:
                        for data in self.eggnog.data_dict[gene]:
                            phylum = data['phylum']
                            for phylum_dict in self.abundance.phylo.phylum_list:
                                if phylum == phylum_dict['phylum_name']:
                                    for species in phylum_dict['species_list']:
                                        self.id_path += 1
                                        self.pathway_gene_species_list.append({
                                            'id_path': self.id_path,
                                            'pathway': pathway.path_name,
                                            'fdr': pathway.fdr,
                                            'fe': pathway.fe,
                                            'gene': gene,
                                            'phylum': phylum,
                                            'top_species': species.species_name,
                                            'reads': species.num_reads
                                        })

    def to_csv(self) -> None:
        df = pd.DataFrame(self.pathway_gene_species_list)
        df.to_csv('pathway_gene_species.csv', index=False)
