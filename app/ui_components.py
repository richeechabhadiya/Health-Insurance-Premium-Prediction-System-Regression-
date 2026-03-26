import streamlit as st

def render_header():
    st.markdown("""
    <div style='display:flex;align-items:center;gap:12px'>
      <div style='font-size:42px'>💰</div>
      <div style='font-size:32px;font-weight:700'>Insurance Premium Predictor</div>
    </div>
    """, unsafe_allow_html=True)

def two_column_layout():
    return st.columns([2, 3])

def result_card(title, value, unit=''):
    st.markdown(f"**{title}**")
    st.success(f"{value} {unit}")
