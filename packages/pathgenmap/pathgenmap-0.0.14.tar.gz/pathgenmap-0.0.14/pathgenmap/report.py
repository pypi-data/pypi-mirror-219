import pandas as pd
import matplotlib.pyplot as plt


class ReportGenerator:
    def __init__(self, file):
        self.file = file
        self.data = None

    def read_data(self):
        self.data = pd.read_csv(self.file)
        self.data = self.data[self.data['reads'] > 0]

    def generate_report(self):
        self.read_data()
        grouped = self.data.groupby('phylum')['reads'].sum().sort_values(ascending=False)
        top_five = grouped[:5]
        other = grouped[5:].sum()
        report_data = pd.concat([top_five, pd.Series({'Other': other})])

        plt.figure(figsize=(10, 8))
        report_data.plot(kind='bar', color=['b', 'g', 'r', 'c', 'm', 'y'])
        plt.xlabel('Phylum')
        plt.ylabel('Reads')
        plt.title('Relative abundance of top five phyla')
        for i, v in enumerate(report_data):
            plt.text(i, v + 0.2, str(v), ha='center', va='bottom',
                     fontweight='bold')
        plt.tight_layout()
        plt.savefig('relative_abundance.png')
