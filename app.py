import streamlit as st
from clash_client import ClashRoyaleClient
from translations import TEXTS

idioma = st.sidebar.radio("🌐 Idioma / Language", ["es", "en"])
t = TEXTS[idioma]
cliente = ClashRoyaleClient()

st.set_page_config(page_title=t["title"], page_icon="👑", layout="wide")

st.title(t["title"])
st.markdown("---")

clan_buscado = st.text_input(t["search_label"], value="#GPV00L2R")
st.write("")

if clan_buscado:
    try:
        miembros = cliente.get_clan_members(clan_buscado)
        miembros_limpios = cliente.extract_clan_members(miembros, t)
        col1, col2, col3 = st.columns(3)
        total_miembros = len(miembros_limpios)

        suma_copas = 0
        for miembro in miembros_limpios:
            suma_copas += miembro[t["col_trophies"]]

        with col1:
            st.metric(t["total_members"], f"{total_miembros} / 50")
        with col2:
            st.metric(t["avg_trophies"], f"🏆 {int(suma_copas / total_miembros) if total_miembros > 0 else 0}")
        with col3:
            st.metric(t["total_trophies"], f"🏆 {suma_copas:,}")
            
        st.markdown("---")

        st.subheader(t["player_list"])
        st.dataframe(miembros_limpios, use_container_width=True, height=400, width=300, hide_index=True)
    except Exception as e:
        st.error(f"Error al buscar el clan: {str(e)}")

    try:
        participantes = cliente.get_clan_war_participantion(clan_buscado)
        participantes_limpios = cliente.extract_war_participants(participantes, t)
        st.subheader(t["war_list"])
        st.dataframe(participantes_limpios, use_container_width=True, height=400, width=300, hide_index=True)
    except Exception as e:
        st.error(f"Error al buscar la guerra del clan: {str(e)}")
    
st.markdown("---")
st.write(t["footer"])