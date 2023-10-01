import pandas as pd


class BridgeTransformer:
    def __init__(self, filepath) -> None:
        self.filepath = filepath

    def _load_raw_data(self):
        try:
            morning_data = pd.read_excel(self.filepath, sheet_name="Manhã", header=None)
            afternoon_data = pd.read_excel(
                self.filepath, sheet_name="Tarde", header=None
            )
            return pd.concat([morning_data, afternoon_data], ignore_index=True)
        except Exception as e:
            print("Failed to load raw data: ", e)

    def process_data(self):
        raw_data = self._load_raw_data()
        relevant_data = raw_data.iloc[:, :2]
        relevant_data.iloc[:, 1] = relevant_data.iloc[:, 1].str.upper()
        relevant_data.rename(
            columns={0: "Oficinas_Presente", 1: "Nome_Completo"}, inplace=True
        )
        self.processed_data = relevant_data


class ModernBridgeTransformer:
    def __init__(self, filepath) -> None:
        self.filepath = filepath

    def _load_raw_data(self):
        try:
            return pd.read_excel(self.filepath)
        except Exception as e:
            print("Failed to load raw data: ", e)

    def process_data(self):
        raw_data = self._load_raw_data()
        bridge_data = raw_data[raw_data["Nome"] != "Nome"].dropna(subset="Nome")
        bridge_data["Oficinas_Presente"] = bridge_data.iloc[:, 4:].count(axis=1)
        bridge_data.rename(
            columns={"Nome": "Nome_Completo"}, inplace=True
        )
        self.processed_data = bridge_data[["Nome_Completo", "Oficinas_Presente"]]
