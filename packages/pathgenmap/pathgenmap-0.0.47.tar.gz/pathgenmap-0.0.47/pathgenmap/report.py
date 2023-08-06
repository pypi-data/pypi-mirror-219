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
            df_grouped['reads'] = df_grouped['reads'] / df_grouped['reads'].sum() * 100  # Convert to percentage if not absolute

        if self.absolute:
            df_final = df_grouped
        else:
            top_filos = df_grouped.iloc[:self.top_filo].copy()
            others = df_grouped.iloc[self.top_filo:].copy()
            others['phylum'] = 'Other Phyla'
            df_final = pd.concat([top_filos, others]).groupby('phylum').sum().reset_index()

        df_final.rename(columns={'reads': 'Sample'}, inplace=True)

        fig, ax = plt.subplots()

        # Reorder the dataframe based on abundance to get the legend in correct order
        df_final.sort_values(by='Sample', ascending=False, inplace=True)
        df_final.set_index('phylum', inplace=True)
        df_final.T.plot(kind='bar', stacked=True, ax=ax)

        ax.set_ylabel('Abundance' if self.absolute else 'Percentage (%)')
        ax.set_title('Absolute abundance' if self.absolute else 'Relative abundance')

        # Edit legend to include the abundance percentage or absolute values
        labels = [f'{label} ({value:.2f}%)' if not self.absolute else f'{label} ({value})'
                  for label, value in zip(df_final.index, df_final['Sample'].values)]
        ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5))

        fig.savefig('PhylumAbundance.png', bbox_inches='tight')
