import streamlit as st
import pandas as pd
from collections import namedtuple
from transformers.peer_transformer import PeerTransformer

TSpecPeer = namedtuple("TSpecPeer", "filepath calculus period skiprows")


@st.cache_data
def get_peer_data(t_specs):
    peer_data_blocks = []
    for spec in t_specs:
        transformer = PeerTransformer(
            spec.filepath, spec.calculus, spec.period, spec.skiprows
        )
        transformer.process_data()
        peer_data_blocks.append(transformer.processed_data)
    print(peer_data_blocks[0].columns)
    peer_data = peer_data_blocks[0].merge(peer_data_blocks[1], on="Nome_Completo")
    peer_data["Plantoes_Presente"] = (
        peer_data["Plantoes_Presente_x"] + peer_data["Plantoes_Presente_y"]
    )
    return peer_data[["Nome_Completo", "Plantoes_Presente"]]
