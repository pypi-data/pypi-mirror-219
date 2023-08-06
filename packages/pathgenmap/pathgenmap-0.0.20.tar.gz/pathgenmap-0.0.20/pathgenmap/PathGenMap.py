# Modulo: pathgenmap.py
import argparse
from tqdm import tqdm
from .integration import Manager
from .report import ReportGenerator

def main():
    parser = argparse.ArgumentParser(
        description='PathGenMap: A program to integrate pathway, annotation and species abundance data.')
    parser.add_argument('pathways_file', type=str,
                        help='A .csv file containing GO biological process pathways.')
    parser.add_argument('eggnog_file', type=str,
                        help='A .tab file containing eggNOG annotations.')
    parser.add_argument('species_abundance_file', type=str,
                        help='A .csv file containing species abundance.')
    parser.add_argument('-r', '--report', action='store_true',
                        help='Generate a report of the relative abundance of organisms.')
    parser.add_argument('-b', '--bar_chart', action='store_true',
                        help='Generate a stacked bar chart based on phylum.')
    parser.add_argument('-s', '--sankey', action='store_true',
                        help='Generate a Sankey diagram based on pathway, gene, phylum, and species.')

    args = parser.parse_args()

    manager = Manager()

    with tqdm(total=100, desc="Processing files...") as pbar:
        manager.process_pathways(args.pathways_file)
        pbar.update(10)
        manager.process_eggnog(args.eggnog_file)
        pbar.update(30)
        manager.process_species_abundance(args.species_abundance_file)
        pbar.update(15)
        manager.integrate_all()
        pbar.update(15)
        manager.to_csv()
        pbar.update(30)

    if args.report:
        report_generator = ReportGenerator(args.species_abundance_file, args.bar_chart, args.sankey)
        report_generator.generate_report()


if __name__ == "__main__":
    main()

