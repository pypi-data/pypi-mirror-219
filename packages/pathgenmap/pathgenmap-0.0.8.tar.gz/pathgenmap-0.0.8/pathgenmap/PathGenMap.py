import argparse
from tqdm import tqdm
from .Integration import Manager


def main():
    parser = argparse.ArgumentParser(
        description='PathGenMap: A program to integrate pathway, annotation and species abundance data.')
    parser.add_argument('pathways_file', type=str,
                        help='A .csv file containing GO biological process pathways.')
    parser.add_argument('eggnog_file', type=str,
                        help='A .tab file containing eggNOG annotations.')
    parser.add_argument('species_abundance_file', type=str,
                        help='A .csv file containing species abundance.')

    args = parser.parse_args()

    manager = Manager()

    with tqdm(total=100, desc="Processing files...") as pbar:
        manager.process_pathways(args.pathways_file)
        pbar.update(15)
        manager.process_eggnog(args.eggnog_file)
        pbar.update(30)
        manager.process_species_abundance(args.species_abundance_file)
        pbar.update(15)
        manager.integrate_all()
        pbar.update(15)
        manager.to_csv()
        pbar.update(25)


if __name__ == "__main__":
    main()





