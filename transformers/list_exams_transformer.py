import pandas as pd
import numpy as np


class ListsExamsTransformer:
    def __init__(self, filepath, lists_indices, exams_indices) -> None:
        self.filepath = filepath
        self.lists_indices = lists_indices
        self.exams_indices = exams_indices

    def _load_raw_data(self):
        try:
            return pd.read_csv(self.filepath)
        except Exception as e:
            print("Failed to load raw data: ", e)

    def _count_appearances(self, row):
        count = 0
        for index in range(len(row)):
            if row.iloc[index] != "-":
                count += 1
        return count

    def _mean_with_sub(self, row):
        grades = row.sort_values(ascending=False)[:3]
        return np.mean(grades)

    def process_data(self):
        raw_data = self._load_raw_data()
        exams_data = raw_data.iloc[:, self.exams_indices]
        exams_appearances = exams_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        grades_data = exams_data.replace("-", 0).apply(pd.to_numeric)
        final_grade = grades_data.apply(np.mean, axis=1, result_type="reduce")
        approval_status = (
            grades_data.apply(self._mean_with_sub, axis=1, result_type="reduce") >= 5.0
        )
        lists_data = raw_data.iloc[:, self.lists_indices]
        lists_submissions = lists_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        exam_group = exams_appearances.map({0: "A", 1: "A", 2: "B", 3: "C", 4: "C"})
        approval_group = approval_status.map({False: "E", True: "D"})
        self.processed_data = pd.DataFrame(
            {
                "Grupo_Avaliacao": exam_group,
                "Grupo_Aprovado": approval_group,
                "Listas_Entregues": lists_submissions,
                "Nota_Final": final_grade,
            }
        )


class LENTransformer(ListsExamsTransformer):
    """Include name info to enable joins with other project activities data."""

    def __init__(
        self, filepath, lists_indices, exams_indices, first_name_index, surname_index
    ) -> None:
        self.filepath = filepath
        self.lists_indices = lists_indices
        self.exams_indices = exams_indices
        self.first_name_index = first_name_index
        self.surname_index = surname_index

    def process_data(self):
        raw_data = self._load_raw_data()
        exams_data = raw_data.iloc[:, self.exams_indices]
        exams_appearances = exams_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        grades_data = exams_data.replace("-", 0).apply(pd.to_numeric)
        final_grade = grades_data.apply(np.mean, axis=1, result_type="reduce")
        approval_status = (
            grades_data.apply(self._mean_with_sub, axis=1, result_type="reduce") >= 5.0
        )
        lists_data = raw_data.iloc[:, self.lists_indices]
        lists_submissions = lists_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        exam_group = exams_appearances.map({0: "A", 1: "A", 2: "B", 3: "C", 4: "C"})
        approval_group = approval_status.map({False: "E", True: "D"})
        name = (
            raw_data.iloc[:, self.first_name_index]
            + " "
            + raw_data.iloc[:, self.surname_index]
        ).str.upper()
        self.processed_data = pd.DataFrame(
            {
                "Grupo_Avaliacao": exam_group,
                "Grupo_Aprovado": approval_group,
                "Listas_Entregues": lists_submissions,
                "Nota_Final": final_grade,
                "Nome_Completo": name,
            }
        )


class ModernListsExamsTransformer(ListsExamsTransformer):
    def __init__(self, filepath, lists_indices, exams_indices, grades_indices) -> None:
        self.filepath = filepath
        self.lists_indices = lists_indices
        self.exams_indices = exams_indices
        self.grades_indices = grades_indices

    def _assing_group(self, number):
        if number < 5:
            return "A"
        elif number < 9:
            return "B"
        else:
            return "C"

    def process_data(self):
        raw_data = self._load_raw_data()
        exams_data = raw_data.iloc[:, self.exams_indices]
        exams_appearances = exams_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        grades_data = (
            raw_data.iloc[:, self.grades_indices].replace("-", 0).apply(pd.to_numeric)
        )
        final_grade = grades_data.apply(np.mean, axis=1, result_type="reduce")
        approval_status = (
            grades_data.apply(self._mean_with_sub, axis=1, result_type="reduce") >= 5.0
        )
        lists_data = raw_data.iloc[:, self.lists_indices]
        lists_submissions = lists_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        exam_group = exams_appearances.map(self._assing_group)
        approval_group = approval_status.map({False: "E", True: "D"})
        self.processed_data = pd.DataFrame(
            {
                "Grupo_Avaliacao": exam_group,
                "Grupo_Aprovado": approval_group,
                "Listas_Entregues": lists_submissions,
                "Nota_Final": final_grade,
            }
        )


class ModernLENTransformer(ModernListsExamsTransformer):
    """Include name info to enable joins with other project activities data."""

    def __init__(
        self,
        filepath,
        lists_indices,
        exams_indices,
        grades_indices,
        first_name_index,
        surname_index,
    ) -> None:
        self.filepath = filepath
        self.lists_indices = lists_indices
        self.exams_indices = exams_indices
        self.grades_indices = grades_indices
        self.first_name_index = first_name_index
        self.surname_index = surname_index

    def process_data(self):
        raw_data = self._load_raw_data()
        exams_data = raw_data.iloc[:, self.exams_indices]
        exams_appearances = exams_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        grades_data = exams_data.replace("-", 0).apply(pd.to_numeric)
        final_grade = grades_data.apply(np.mean, axis=1, result_type="reduce")
        approval_status = (
            grades_data.apply(self._mean_with_sub, axis=1, result_type="reduce") >= 5.0
        )
        lists_data = raw_data.iloc[:, self.lists_indices]
        lists_submissions = lists_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        exam_group = exams_appearances.map({0: "A", 1: "A", 2: "B", 3: "C", 4: "C"})
        approval_group = approval_status.map({False: "E", True: "D"})
        name = (
            raw_data.iloc[:, self.first_name_index]
            + " "
            + raw_data.iloc[:, self.surname_index]
        ).str.upper()
        self.processed_data = pd.DataFrame(
            {
                "Grupo_Avaliacao": exam_group,
                "Grupo_Aprovado": approval_group,
                "Listas_Entregues": lists_submissions,
                "Nota_Final": final_grade,
                "Nome_Completo": name,
            }
        )

    def process_data(self):
        raw_data = self._load_raw_data()
        exams_data = raw_data.iloc[:, self.exams_indices]
        exams_appearances = exams_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        grades_data = (
            raw_data.iloc[:, self.grades_indices].replace("-", 0).apply(pd.to_numeric)
        )
        final_grade = grades_data.apply(np.mean, axis=1, result_type="reduce")
        approval_status = (
            grades_data.apply(self._mean_with_sub, axis=1, result_type="reduce") >= 5.0
        )
        lists_data = raw_data.iloc[:, self.lists_indices]
        lists_submissions = lists_data.apply(
            self._count_appearances, axis=1, result_type="reduce"
        )
        exam_group = exams_appearances.map(self._assing_group)
        approval_group = approval_status.map({False: "E", True: "D"})
        name = (
            raw_data.iloc[:, self.first_name_index]
            + " "
            + raw_data.iloc[:, self.surname_index]
        ).str.upper()
        self.processed_data = pd.DataFrame(
            {
                "Grupo_Avaliacao": exam_group,
                "Grupo_Aprovado": approval_group,
                "Listas_Entregues": lists_submissions,
                "Nota_Final": final_grade,
                "Nome_Completo": name,
            }
        )
