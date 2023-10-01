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

tutoring_data = tutoring_helpers.get_tutoring_data(
    [
        TSpec(
            DATA_ROOT
            / "2022-4"
            / "friday_tutoring"
            / "Sextas - 2022-4 - C2 - Manhã.xlsx",
            6,
        ),
        TSpec(
            DATA_ROOT
            / "2022-4"
            / "friday_tutoring"
            / "Sextas - 2022-4 - C2 - Tarde.xlsx",
            3,
        ),
    ]
)

full_data_tutoring = data.merge(tutoring_data, on="Nome_Completo", how="left").fillna(
    {"Sextas_Presente": 0}
)
full_data_tutoring["Grupo_Sexta"] = (full_data_tutoring["Sextas_Presente"] > 1).map(
    {False: "B", True: "A"}
)


st.title("Monitorias - C2 - 2022/4")

st.header("Presença dos Estudantes em Monitorias de Sexta")

st.plotly_chart(
    px.bar(
        full_data_tutoring[["Sextas_Presente", "Nota_Final"]]
        .groupby("Sextas_Presente")
        .count()
        .reset_index()
        .rename(columns={"Nota_Final": "Qtd_Alunos"}),
        x="Sextas_Presente",
        y="Qtd_Alunos",
    )
)

st.header("Média das Notas Finais por Presença em Monitorias de Sexta")

st.plotly_chart(
    px.bar(
        full_data_tutoring[["Sextas_Presente", "Nota_Final"]]
        .groupby("Sextas_Presente")
        .mean()
        .reset_index()
        .rename(columns={"Nota_Final": "Media_Notas_Finais"}),
        x="Sextas_Presente",
        y="Media_Notas_Finais",
    )
)

st.header("Média das Notas Finais por Presença em Sextas: Grupo*")

st.plotly_chart(
    px.bar(
        full_data_tutoring[["Grupo_Sexta", "Nota_Final"]]
        .groupby("Grupo_Sexta")
        .mean()
        .reset_index()
        .rename(columns={"Nota_Final": "Media_Notas_Finais"}),
        x="Grupo_Sexta",
        y="Media_Notas_Finais",
    )
)

st.write("\* Definição dos grupos:")
st.write(
    "- Grupo A: Estudantes que compareceram duas vezes ou mais às monitorias de sexta."
)
st.write(
    "- Grupo B: Estudantes que compareceram menos de duas vezes às monitorias de sexta."
)
