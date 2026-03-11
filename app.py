import streamlit as st

st.set_page_config(page_title="Clash Royale - Clan Stats Dashboard ⚔️", page_icon="👑", layout="wide")

from clash_client import ClashRoyaleClient
from translations import TEXTS

idioma = st.radio("🌐 Idioma / Language", ["es", "en"], horizontal=True)
t = TEXTS[idioma]
cliente = ClashRoyaleClient()

st.title(t["title"])
st.markdown("---")

clan_buscado = st.text_input(t["search_label"], value="#GPV00L2R")
st.write("")

if clan_buscado:
    tab1, tab2, tab3 = st.tabs([t["tab_overview"], t["tab_members"], t["tab_war"]])

    # ========== TAB 1: RESUMEN DEL CLAN ==========
    with tab1:
        try:
            clan_info = cliente.get_clan_info(clan_buscado)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t["total_members"], f"{clan_info['members_count']} / 50")
            with col2:
                st.metric(t["clan_score"], f"🏆 {clan_info['clan_score']:,}")
            with col3:
                st.metric(t["war_trophies"], f"⚔️ {clan_info['war_trophies']:,}")

            col4, col5, col6 = st.columns(3)
            with col4:
                st.metric(t["donations_week"], f"🎁 {clan_info['donations_per_week']:,}")
            with col5:
                st.metric(t["required_trophies"], f"🔒 {clan_info['required_trophies']:,}")
            with col6:
                clan_type = t.get("type_" + clan_info["type"], clan_info["type"])
                st.metric(t["clan_type"], f"📋 {clan_type}")
            st.markdown("---")

            # Estadísticas de Guerra del Clan
            war_log = cliente.get_clan_war_log(clan_buscado)
            
            if war_log:
                total_wars = len(war_log)
                first_places = sum(1 for w in war_log if w["rank"] == 1)
                avg_fame = int(sum(w["fame"] for w in war_log) / total_wars)
                total_trophy_change = sum(w["trophy_change"] for w in war_log)
                win_rate = round((first_places / total_wars) * 100, 1)

                st.subheader(t["clan_war_stats"])
                cw1, cw2, cw3, cw4 = st.columns(4)
                with cw1:
                    st.metric(t["wars_played"], f"⚔️ {total_wars}")
                with cw2:
                    st.metric(t["wars_won"], f"🥇 {first_places}")
                with cw3:
                    st.metric(t["clan_win_rate"], f"📈 {win_rate}%")
                with cw4:
                    st.metric(t["avg_fame"], f"🔥 {avg_fame:,}")


        except Exception as e:
            st.error(f"{t['search_error']}: {str(e)}")

    # ========== TAB 2: MIEMBROS ==========
    with tab2:
        try:
            miembros = cliente.get_clan_members(clan_buscado)
            miembros_limpios = cliente.extract_clan_members(miembros, t)
            total_miembros = len(miembros_limpios)

            suma_copas = 0
            for miembro in miembros_limpios:
                suma_copas += miembro[t["col_trophies"]]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(t["total_members"], f"{total_miembros} / 50")
            with col2:
                st.metric(t["avg_trophies"], f"🏆 {int(suma_copas / total_miembros) if total_miembros > 0 else 0}")
            with col3:
                st.metric(t["total_trophies"], f"🏆 {suma_copas:,}")

            st.markdown("---")
            st.subheader(t["player_list"])
            st.dataframe(miembros_limpios, width='stretch', height=400, hide_index=True)

            st.markdown("---")

            # Selector de jugador para ver stats individuales
            nombres = [m[t["col_name"]] for m in miembros_limpios]
            tags_raw = [m["tag"] for m in miembros.get("items", [])]
            nombre_tag = dict(zip(nombres, tags_raw))

            jugador_elegido = st.selectbox(t["select_player"], nombres)

            if jugador_elegido:
                with st.spinner("⏳"):
                    stats = cliente.get_player_stats(nombre_tag[jugador_elegido], t)

                st.subheader(f"{t['player_stats']}: {jugador_elegido}")
                c1, c2, c3, c4 = st.columns(4)
                keys = list(stats.keys())
                vals = list(stats.values())
                with c1:
                    st.metric(keys[0], vals[0])
                    st.metric(keys[4], vals[4])
                with c2:
                    st.metric(keys[1], vals[1])
                    st.metric(keys[5], vals[5])
                with c3:
                    st.metric(keys[2], vals[2])
                    st.metric(keys[6], vals[6])
                with c4:
                    st.metric(keys[3], vals[3])
                    st.metric(keys[7], vals[7])
        except Exception as e:
            st.error(f"{t['search_error']}: {str(e)}")

    # ========== TAB 3: GUERRA ==========
    with tab3:
        try:
            participantes = cliente.get_clan_war_participation(clan_buscado)
            participantes_limpios = cliente.extract_war_participants(participantes, t)
            st.subheader(t["war_list"])
            st.dataframe(participantes_limpios, width='stretch', height=400, hide_index=True)
        except Exception as e:
            st.error(f"{t['war_error']}: {str(e)}")

st.markdown("---")
st.write(t["footer"])
st.markdown(
    f'<div style="text-align:center;margin-top:10px;">'
    f'<a href="https://paypal.me/DMolinaInojosa" target="_blank" '
    f'style="display:inline-block;background:linear-gradient(135deg,#6366f1,#8b5cf6);'
    f'color:white;padding:10px 24px;border-radius:10px;text-decoration:none;font-weight:bold;'
    f'font-size:15px;">💜 {t["donate"]}</a></div>',
    unsafe_allow_html=True
)