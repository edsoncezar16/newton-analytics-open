import streamlit as st
import plotly.express as px
import newton_helpers.lists_exams_helpers as nh
from newton_helpers import tutoring_helpers

from newton_helpers.constants import DATA_ROOT
from newton_helpers.tutoring_helpers import TSpec

data = nh.get_processed_LEN_data(
    filepath=DATA_ROOT / "2022-4" / "lists_exams" / "C2-2022-4.csv",
    lists_indices=list(range(7, 11)) + list(range(12, 20)),
    exams_indices=[11, 20, 26, 27],
    first_name_index=0,
    surname_index=1
)

M, A, B, C, D = nh.compute_quantitatives(data)

st.title("Análises de C2 do período 2022/4")


st.header("Informações Quantivativas do Período")

st.write("Total de matriculados (M): ", M)
st.write("Alunos que fizeram no máximo 1 avaliação (A): ", A)
st.write("Alunos que fizeram 2 avaliações (B): ", B)
st.write("Alunos que fizeram 3 ou mais avaliações (C): ", C)
st.write("Alunos aprovados (D): ", D)

st.header("Entregas de Listas por Estudantes")

group = st.radio(
    "Selecione um grupo para filtrar os resultados",
    ["Total", "A", "B", "C", "D"],
    index=0,
    horizontal=True,
)

normalize = st.checkbox("Exibir resultados em porcentagem")

list_submission_data = nh.get_list_submission_data(group, data)

st.plotly_chart(
    px.bar(
        nh.transform_list_submission_data(list_submission_data, normalize),
        x="Listas_Entregues",
        y="Porcentagem_Alunos" if normalize else "Quantidade_Alunos",
    )
)

st.header("Média das Notas Finais por Listas Entregues")

st.plotly_chart(
    px.bar(
        data[["Listas_Entregues", "Nota_Final"]]
        .groupby("Listas_Entregues")
        .mean()
        .reset_index()
        .rename(columns={"Nota_Final": "Media_Notas_Finais"}),
        x="Listas_Entregues",
        y="Media_Notas_Finais",
    )
)

st.header("Alunos Aprovados por Listas Entregues")

st.plotly_chart(
    px.bar(
        nh.get_approved_proportion_data(data),
        x="Listas_Entregues",
        y="Porcentagem_Aprovados",
    )
)