# PathGenMap

**PathGenMap** is a comprehensive Python application designed to integrate pathway, annotation, and species abundance data. The program utilizes several modules, each with specific functions, to load, process, and integrate information from different sources.

## Dependencies

**PathGenMap** requires Python 3.7 or later and depends on the following Python libraries:

- pandas
- tqdm

## Installation

To install the necessary Python libraries, use the pip package manager and run the following command:

```
pip install pandas tqdm
```

## Usage

To execute the PathGenMap program, run the main script (PathGenMap.py) with the necessary files as arguments:

```
python PathGenMap.py pathways_file.csv eggnog_file.tab species_abundance.csv
```

Where:
- `pathways_file.csv` is a CSV file containing GO biological process pathways.
- `eggnog_file.tab` is a TAB file containing eggNOG annotations.
- `species_abundance.csv` is a CSV file containing species abundance.

## Functions

PathGenMap consists of several modules each containing specific classes and methods. Here are some key methods:

- `process_species_abundance(bracken_file: str)`: Method in the Manager class to process species abundance data.
- `populate_species_abundance(file: str)`: Method in the Phylum class to populate species abundance data from a bracken file.
