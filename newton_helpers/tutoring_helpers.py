import streamlit as st
import pandas as pd
from collections import namedtuple
from transformers.tutoring_transformer import TutoringTransformer

TSpec = namedtuple("TSpec", "filepath n_sheets")

@st.cache_data
def get_tutoring_data(t_specs):
    tutoring_data = []
    for spec in t_specs:
        transformer = TutoringTransformer(spec.filepath, spec.n_sheets)
        transformer.process_data()
        tutoring_data.append(transformer.processed_data)
    return pd.concat(tutoring_data, ignore_index=True)
