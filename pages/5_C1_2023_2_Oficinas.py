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

bridge_data = bridge_helpers.modern_get_bridge_data(
    filepath=DATA_ROOT / "2023-2" / "bridge_program" / "Oficinas - 2023-2.xlsx"
)

full_data = data.merge(bridge_data, on="Nome_Completo", how="left").fillna(
    {"Oficinas_Presente": 0}
)
full_data["Grupo_Oficina"] = (full_data["Oficinas_Presente"] > 1).map(
    {False: "B", True: "A"}
)

st.title("Oficinas - C1 - 2023/2")

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
