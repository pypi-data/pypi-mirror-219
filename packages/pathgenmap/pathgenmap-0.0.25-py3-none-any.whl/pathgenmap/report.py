import matplotlib.pyplot as plt
import pandas as pd


class ReportGenerator:
    """Class to generate reports from the integrated data."""

    def __init__(self, species_abundance_file, top_filo, absolute):
        """
        Constructor method.

        Args:
            species_abundance_file (str): Path to the .csv file containing species abundance.
            top_filo (int): Top N filos to be considered for the bar chart.
            absolute (bool): Use absolute abundance for the bar chart. If False, relative abundance is used.
        """
        self.species_abundance_file = species_abundance_file
        self.top_filo = top_filo
        self.absolute = absolute

    def generate_report(self):
        """
        Method to generate the report.
        """
        self.generate_stacked_bar_chart()

    def generate_stacked_bar_chart(self):
        """Method to generate a stacked bar chart."""
        df = pd.read_csv(self.species_abundance_file)
        df = df[df['reads'] > 0]  # Filter out rows with reads <= 0
        df_grouped = df.groupby('phylum').agg({'reads': 'sum'}).reset_index()
        df_grouped = df_grouped.sort_values(by='reads', ascending=False)

        if not self.absolute:
            df_grouped['reads'] = df_grouped['reads'] / df_grouped['reads'].sum() * 100

        # Add a 'Others Phyla' group for those not in top N
        top_filos = df_grouped.iloc[:self.top_filo].copy()
        others = df_grouped.iloc[self.top_filo:].copy()
        others_sum = others['reads'].sum()
        others = pd.DataFrame([{'phylum': 'Other Phyla', 'reads': others_sum}])
        df_final = pd.concat([top_filos, others])

        # Generate the chart
        fig, ax = plt.subplots()
        df_final.plot(kind='barh', stacked=True, ax=ax, color='blue')
        ax.set_xlabel('Reads')
        ax.set_ylabel('Phylum')
        ax.set_title('Phylum Abundance')

        # Save the figure
        fig.savefig('PhylumAbundance.png')