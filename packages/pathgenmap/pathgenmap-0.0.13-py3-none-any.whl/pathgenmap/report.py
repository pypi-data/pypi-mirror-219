# Módulo: report.py
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
        self.read_data()  # Não esqueça de ler os dados primeiro
        grouped = self.data.groupby('phylum')['reads'].sum().sort_values(ascending=False)
        top_ten = grouped[:10]
        other = grouped[10:].sum()
        report_data = pd.concat([top_ten, pd.Series({'Other': other})])

        plt.figure(figsize=(10, 8))
        plt.pie(report_data, labels=report_data.index, autopct='%1.1f%%')
        plt.title('Relative abundance of organisms')
        plt.savefig('relative_abundance.png')
