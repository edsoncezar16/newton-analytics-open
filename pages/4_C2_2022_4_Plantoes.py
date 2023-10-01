import streamlit as st
import pandas as pd
import plotly.express as px
import newton_helpers.lists_exams_helpers as nh
from newton_helpers import peer_helpers

from newton_helpers.constants import DATA_ROOT
from newton_helpers.peer_helpers import TSpecPeer

data = nh.get_processed_LEN_data(
    filepath=DATA_ROOT / "2022-4" / "lists_exams" / "C1-2022-4.csv",
    lists_indices=list(range(7, 19)),
    exams_indices=[19, 20, 24, 25],
    first_name_index=0,
    surname_index=1,
)

peer_data_morning = peer_helpers.get_peer_data(
    [
        TSpecPeer(
            DATA_ROOT
            / "2022-4"
            / "peer_tutoring"
            / "Plantões - 2022-4 - Até 06_10_2022.xlsx",
            2,
            "Manhã",
            6,
        ),
        TSpecPeer(
            DATA_ROOT
            / "2022-4"
            / "peer_tutoring"
            / "Plantões - 2022-4 - de 13_10 a 15_12.xlsx",
            2,
            "Manhã",
            3,
        ),
    ]
)

peer_data_afternoon = peer_helpers.get_peer_data(
    [
        TSpecPeer(
            DATA_ROOT
            / "2022-4"
            / "peer_tutoring"
            / "Plantões - 2022-4 - Até 06_10_2022.xlsx",
            2,
            "Tarde",
            6,
        ),
        TSpecPeer(
            DATA_ROOT
            / "2022-4"
            / "peer_tutoring"
            / "Plantões - 2022-4 - de 13_10 a 15_12.xlsx",
            2,
            "Tarde",
            3,
        ),
    ]
)

peer_data = pd.concat([peer_data_morning, peer_data_afternoon], ignore_index=True)

full_data_peer = data.merge(peer_data, on="Nome_Completo", how="left").fillna(
    {"Plantoes_Presente": 0}
)
full_data_peer["Grupo_Plantoes"] = (full_data_peer["Plantoes_Presente"] > 1).map(
    {False: "B", True: "A"}
)

st.title("Plantões - C2 - 2022/4")

st.header("Presença dos Estudantes em Plantões")

st.plotly_chart(
    px.bar(
        full_data_peer[["Plantoes_Presente", "Nota_Final"]]
        .groupby("Plantoes_Presente")
        .count()
        .reset_index()
        .rename(columns={"Nota_Final": "Qtd_Alunos"}),
        x="Plantoes_Presente",
        y="Qtd_Alunos",
    )
)

st.header("Média das Notas Finais por Presença em Plantões")

st.plotly_chart(
    px.bar(
        full_data_peer[["Plantoes_Presente", "Nota_Final"]]
        .groupby("Plantoes_Presente")
        .mean()
        .reset_index()
        .rename(columns={"Nota_Final": "Media_Notas_Finais"}),
        x="Plantoes_Presente",
        y="Media_Notas_Finais",
    )
)

st.header("Média das Notas Finais por Presença em Plantões: Grupo*")

st.plotly_chart(
    px.bar(
        full_data_peer[["Grupo_Plantoes", "Nota_Final"]]
        .groupby("Grupo_Plantoes")
        .mean()
        .reset_index()
        .rename(columns={"Nota_Final": "Media_Notas_Finais"}),
        x="Grupo_Plantoes",
        y="Media_Notas_Finais",
    )
)

st.write("\* Definição dos grupos:")
st.write("- Grupo A: Estudantes que compareceram duas vezes ou mais aos plantões")
st.write("- Grupo B: Estudantes que compareceram menos de duas vezes aos plantões.")