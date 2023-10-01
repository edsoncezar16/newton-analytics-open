import streamlit as st
from transformers.list_exams_transformer import (
    ModernListsExamsTransformer,
    ListsExamsTransformer,
    LENTransformer,
    ModernLENTransformer
)


@st.cache_data
def get_processed_data(filepath, lists_indices, exams_indices):
    transformer = ListsExamsTransformer(filepath, lists_indices, exams_indices)
    transformer.process_data()
    return transformer.processed_data


@st.cache_data
def get_processed_LEN_data(
    filepath, lists_indices, exams_indices, first_name_index, surname_index
):
    transformer = LENTransformer(
        filepath, lists_indices, exams_indices, first_name_index, surname_index
    )
    transformer.process_data()
    return transformer.processed_data


@st.cache_data
def modern_get_processed_data(filepath, lists_indices, exams_indices, grades_indices):
    transformer = ModernListsExamsTransformer(
        filepath, lists_indices, exams_indices, grades_indices
    )
    transformer.process_data()
    return transformer.processed_data


@st.cache_data
def modern_get_processed_LEN_data(
    filepath, lists_indices, exams_indices, grades_indices, first_name_index, surname_index
):
    transformer = ModernLENTransformer(
        filepath, lists_indices, exams_indices, grades_indices, first_name_index, surname_index
    )
    transformer.process_data()
    return transformer.processed_data


@st.cache_data
def compute_quantitatives(data):
    M = data.shape[0]
    [A, B, C] = [
        data[data["Grupo_Avaliacao"] == group].shape[0] for group in ("A", "B", "C")
    ]
    D = data[data["Grupo_Aprovado"] == "D"].shape[0]
    return M, A, B, C, D


@st.cache_data
def get_list_submission_data(group, data):
    if group == "Total":
        return data
    elif group == "D":
        return data[data["Grupo_Aprovado"] == group]
    else:
        return data[data["Grupo_Avaliacao"] == group]


@st.cache_data
def transform_list_submission_data(list_submission_data, normalize):
    return (
        list_submission_data["Listas_Entregues"]
        .value_counts(normalize=normalize)
        .reset_index()
        .rename(
            columns={"proportion": "Porcentagem_Alunos", "count": "Quantidade_Alunos"}
        )
    )


@st.cache_data
def count_Ds(series):
    if len(series) == 0:
        return 0
    else:
        return sum(series == "D") / len(series)


@st.cache_data
def get_approved_proportion_data(data):
    return (
        data[["Listas_Entregues", "Grupo_Aprovado"]]
        .groupby("Listas_Entregues")
        .agg(count_Ds)
        .reset_index()
        .rename(columns={"Grupo_Aprovado": "Porcentagem_Aprovados"})
    )
