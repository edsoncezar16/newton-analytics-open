import streamlit as st
import plotly.express as px
import newton_helpers.lists_exams_helpers as nh
from newton_helpers import bridge_helpers

from newton_helpers.constants import DATA_ROOT


data = nh.modern_get_processed_LEN_data(
    filepath=DATA_ROOT / "2023-2" / "lists_exams" / "C1-2023-2.csv",
    lists_indices=list(range(7, 13)) + list(range(18, 23)) + list(range(28, 33)),
    exams_indices=list(range(13, 17)) + list(range(23, 27)) + list(range(44, 48)),
    grades_indices=[17, 27, 48],
    first_name_index=0,
    surname_index=1,
)

M, A, B, C, D = nh.compute_quantitatives(data)

st.title("Análises de C1 do período 2023/2")


st.header("Informações Quantivativas do Período")

st.write("Total de matriculados (M): ", M)
st.write("Alunos que fizeram no máximo 4 avaliações (A): ", A)
st.write("Alunos que fizeram entre 5 e 8 avaliações (B): ", B)
st.write("Alunos que fizeram 9 ou mais avaliações (C): ", C)
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

bridge_data = bridge_helpers.modern_get_bridge_data(
    filepath=DATA_ROOT / "2023-2" / "bridge_program" / "Oficinas - 2023-2.xlsx"
)

full_data = data.merge(bridge_data, on="Nome_Completo", how="left").fillna(
    {"Oficinas_Presente": 0}
)
full_data["Grupo_Oficina"] = (full_data["Oficinas_Presente"] > 1).map(
    {False: "B", True: "A"}
)

st.header("Presença dos Estudantes em Oficinas")

st.plotly_chart(
    px.bar(
        full_data[["Oficinas_Presente", "Nota_Final"]]
        .groupby("Oficinas_Presente")
        .count()
        .reset_index()
        .rename(columns={"Nota_Final": "Qtd_Alunos"}),
        x="Oficinas_Presente",
        y="Qtd_Alunos",
    )
)

st.header("Média das Notas Finais por Presença em Oficinas")

st.plotly_chart(
    px.bar(
        full_data[["Oficinas_Presente", "Nota_Final"]]
        .groupby("Oficinas_Presente")
        .mean()
        .reset_index()
        .rename(columns={"Nota_Final": "Media_Notas_Finais"}),
        x="Oficinas_Presente",
        y="Media_Notas_Finais",
    )
)

st.header("Média das Notas Finais por Presença em Oficinas: Grupo*")

st.plotly_chart(
    px.bar(
        full_data[["Grupo_Oficina", "Nota_Final"]]
        .groupby("Grupo_Oficina")
        .mean()
        .reset_index()
        .rename(columns={"Nota_Final": "Media_Notas_Finais"}),
        x="Grupo_Oficina",
        y="Media_Notas_Finais",
    )
)

st.write("\* Definição dos grupos:")
st.write("- Grupo A: Estudantes que compareceram duas vezes ou mais às oficinas.")
st.write("- Grupo B: Estudantes que compareceram menos de duas vezes às oficinas.")
