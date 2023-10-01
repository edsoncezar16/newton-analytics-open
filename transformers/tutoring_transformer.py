import pandas as pd
from functools import reduce


class TutoringTransformer:
    def __init__(self, filepath, n_sheets) -> None:
        self.filepath = filepath
        self.n_sheets = n_sheets

    def _load_raw_data(self):
        try:
            raw_sheets = [
                pd.read_excel(self.filepath, sheet_name=f"Sala{i}")
                for i in range(1, self.n_sheets + 1)
            ]
            return pd.concat(raw_sheets, ignore_index=True)
        except Exception as e:
            print("Failed to load raw data: ", e)

    def process_data(self):
        tutoring_data = self._load_raw_data()
        tutoring_data["Sextas_Presente"] = tutoring_data.iloc[:, 3:].count(axis=1)
        tutoring_data.rename(columns={"Unnamed: 0": "Nome_Completo"}, inplace=True)
        tutoring_data.dropna(subset="Nome_Completo", inplace=True)
        self.processed_data = tutoring_data[["Nome_Completo", "Sextas_Presente"]]
