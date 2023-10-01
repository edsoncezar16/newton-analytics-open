import pandas as pd


class PeerTransformer:
    def __init__(self, filepath, calculus, period, skiprows) -> None:
        self.filepath = filepath
        self.calculus = calculus
        self.period = period
        self.skiprows = skiprows

    def _load_raw_data(self):
        try:
            return pd.read_excel(
                self.filepath,
                sheet_name=f"C{self.calculus}-{self.period}",
                skiprows=self.skiprows,
                header=None
            )
        except Exception as e:
            print("Failed to load raw data: ", e)

    def process_data(self):
        raw_data = self._load_raw_data()
        relevant_data = raw_data.iloc[:, :2]
        relevant_data.rename(columns={0: "Plantoes_Presente", 1: "Nome_Completo"}, inplace=True)
        self.processed_data = relevant_data
