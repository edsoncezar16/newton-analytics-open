import streamlit as st
from transformers.bridge_transformer import BridgeTransformer, ModernBridgeTransformer


@st.cache_data
def get_bridge_data(filepath):
    transformer = BridgeTransformer(filepath)
    transformer.process_data()
    return transformer.processed_data


@st.cache_data
def modern_get_bridge_data(filepath):
    transformer = ModernBridgeTransformer(filepath)
    transformer.process_data()
    return transformer.processed_data
