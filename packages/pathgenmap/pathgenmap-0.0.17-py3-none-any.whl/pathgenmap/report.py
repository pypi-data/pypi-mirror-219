# Modulo: report.py
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.sankey import Sankey

class ReportGenerator:
    """Class to generate reports from the integrated data."""

    def __init__(self, species_abundance_file, pathway_file):
        """
        Constructor method.

        Args:
            species_abundance_file (str): Path to the .csv file containing species abundance.
            pathway_file (str): Path to the .csv file containing pathway, gene and species.
        """
        self.species_abundance_file = species_abundance_file
        self.pathway_file = pathway_file

    def generate_report(self, report_type):
        """
        Method to generate the report.

        Args:
            report_type (str): Type of report to generate, can be "-b" or "-s".
        """
        if report_type == "-b":
            self.generate_stacked_bar_chart()
        elif report_type == "-s":
            self.generate_sankey_diagram()
        else:
            raise ValueError(f"Invalid report type: {report_type}")

    def generate_stacked_bar_chart(self):
        """Method to generate a stacked bar chart."""
        df = pd.read_csv(self.species_abundance_file)
        df = df[df['reads'] > 0]  # Filter out rows with reads <= 0
        df_grouped = df.groupby('phylum').agg({'reads': 'sum'}).reset_index()
        df_grouped = df_grouped.sort_values(by='reads', ascending=False)

        # Add a 'Others Phyla' group for those not in top 5
        top_5 = df_grouped.iloc[:5].copy()
        others = df_grouped.iloc[5:].copy()
        others_sum = others['reads'].sum()
        others = pd.DataFrame([{'phylum': 'Other Phyla', 'reads': others_sum}])
        df_final = pd.concat([top_5, others])

        # Plot
        df_final.plot(kind='barh', x='phylum', y='reads', stacked=True, legend=False)
        plt.xlabel('Number of Reads')
        plt.ylabel('Phylum')
        plt.title('Relative Abundance of Organisms')
        plt.gca().invert_yaxis()
        plt.savefig('stacked_bar_chart.png', format='png')

    def generate_sankey_diagram(self):
        """Method to generate a Sankey diagram."""
        df = pd.read_csv(self.pathway_file)

        # Create Sankey instance
        sankey = Sankey()

        # Add flows for each pathway, gene, phylum, and species
        for index, row in df.iterrows():
            sankey.add(flows=[row['reads'], -row['reads']],
                       labels=[row['pathway'], row['gene']],
                       orientations=[-1, 1])
            sankey.add(flows=[row['reads'], -row['reads']],
                       labels=[row['gene'], row['phylum']],
                       orientations=[-1, 1])
            sankey.add(flows=[row['reads'], -row['reads']],
                       labels=[row['phylum'], row['top_species']],
                       orientations=[-1, 1])

        sankey.finish()
        plt.title('Sankey Diagram of Pathway, Gene, Phylum, and Species')
        plt.savefig('sankey_diagram.png', format='png')
