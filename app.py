import streamlit as st

st.set_page_config(page_title="Clash Royale - Stats Tracker ⚔️", page_icon="👑", layout="wide")

from clash_client import ClashRoyaleClient
from translations import TEXTS

# Initialize defaults so we can translate the title FIRST
idioma = st.session_state.get('lang', 'es')
t = TEXTS[idioma]
cliente = ClashRoyaleClient()

st.title(t["title"])
st.markdown("---")

# The radio button actually goes here
nuevo_idioma = st.radio("🌐 Idioma / Language", ["es", "en"], index=0 if idioma == 'es' else 1, horizontal=True)

if nuevo_idioma != idioma:
    st.session_state['lang'] = nuevo_idioma
    st.rerun()

tag_buscado = st.text_input(t["search_label"], value="#VY9P8JLLR")
st.write("")

if tag_buscado:
    try:
        modo = st.radio(t["search_mode"], [t["mode_player"], t["mode_clan"]], horizontal=True)

        if modo == t["mode_player"]:
            # ===== MODO JUGADOR =====
            player_data = cliente.get_player_data(tag_buscado)
            
            if "reason" in player_data and player_data["reason"] == "notFound":
                st.warning(t["not_found_player"])
                st.stop()
            
            clan_data = player_data.get("clan", None)
            has_clan = clan_data is not None
            clan_tag = clan_data.get("tag", "") if has_clan else ""

            tab1, tab2, tab3 = st.tabs([t["tab_player_overview"], t["tab_members"], t["tab_war"]])

            # ========== TAB 1: PERFIL DEL JUGADOR ==========
            with tab1:
                player_name = player_data.get("name", "")
                player_trophies = player_data.get("trophies", 0)
                player_level = player_data.get("expLevel", 0)
                player_clan_name = clan_data.get("name", "") if has_clan else t["no_clan_short"]

                st.subheader(f"👤 {t['player_overview']}: {player_name}")

                p1, p2, p3 = st.columns(3)
                with p1:
                    st.metric(t["current_trophies"], f"🏆 {player_trophies:,}")
                with p2:
                    st.metric(t["exp_level"], f"⭐ {player_level}")
                with p3:
                    st.metric(t["player_clan"], f"🛡️ {player_clan_name}" if has_clan else f"{player_clan_name}")

                st.markdown("---")

                # Stats de combate del jugador
                stats = cliente.get_player_stats(player_data, t)
                st.subheader(t["combat_stats"])
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

                # Si tiene clan, mostrar resumen del clan también
                if has_clan:
                    st.markdown("---")
                    clan_info = cliente.get_clan_info(clan_tag)

                    st.subheader(t["clan_overview"])
                    co1, co2, co3 = st.columns(3)
                    
                    members_count = clan_info.get("members", 0)
                    clan_score = clan_info.get("clanScore", 0)
                    war_trophies = clan_info.get("clanWarTrophies", 0)
                    donations_pw = clan_info.get("donationsPerWeek", 0)
                    req_trophies = clan_info.get("requiredTrophies", 0)
                    clan_type_raw = clan_info.get("type", "")

                    with co1:
                        st.metric(t["total_members"], f"{members_count} / 50")
                    with co2:
                        st.metric(t["clan_score"], f"🏆 {clan_score:,}")
                    with co3:
                        st.metric(t["war_trophies"], f"⚔️ {war_trophies:,}")

                    co4, co5, co6 = st.columns(3)
                    with co4:
                        st.metric(t["donations_week"], f"🎁 {donations_pw:,}")
                    with co5:
                        st.metric(t["required_trophies"], f"🔒 {req_trophies:,}")
                    with co6:
                        clan_type = t.get("type_" + clan_type_raw, clan_type_raw)
                        st.metric(t["clan_type"], f"📋 {clan_type}")

            # ========== TAB 2: MIEMBROS DEL CLAN ==========
            with tab2:
                if has_clan:
                    miembros = cliente.get_clan_members(clan_tag)
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
                            member_data = cliente.get_player_data(nombre_tag[jugador_elegido])
                            member_stats = cliente.get_player_stats(member_data, t)

                        st.subheader(f"{t['player_stats']}: {jugador_elegido}")
                        c1, c2, c3, c4 = st.columns(4)
                        keys = list(member_stats.keys())
                        vals = list(member_stats.values())
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
                else:
                    st.info(t["no_clan"])

            # ========== TAB 3: GUERRA ==========
            with tab3:
                if has_clan:
                    participantes = cliente.get_clan_war_participation(clan_tag)
                    participantes_limpios = cliente.extract_war_participants(participantes, t)
                    st.subheader(t["war_list"])
                    st.dataframe(participantes_limpios, width='stretch', height=400, hide_index=True)

                    # Stats de guerra del clan
                    war_log = cliente.get_clan_war_log(clan_tag)
                    if war_log:
                        st.markdown("---")
                        total_wars = len(war_log)
                        first_places = sum(1 for w in war_log if w["rank"] == 1)
                        avg_fame = int(sum(w["fame"] for w in war_log) / total_wars)
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
                else:
                    st.info(t["no_clan"])

        else:
            # ===== MODO CLAN =====
            clan_tag = tag_buscado

            clan_info = cliente.get_clan_info(clan_tag)
            
            if "reason" in clan_info and clan_info["reason"] == "notFound":
                st.warning(t["not_found_clan"])
                st.stop()

            tab1, tab2, tab3 = st.tabs([t["tab_overview"], t["tab_members"], t["tab_war"]])

            with tab1:
                st.subheader(t["clan_overview"])
                co1, co2, co3 = st.columns(3)
                
                members_count = clan_info.get("members", 0)
                clan_score = clan_info.get("clanScore", 0)
                war_trophies = clan_info.get("clanWarTrophies", 0)
                donations_pw = clan_info.get("donationsPerWeek", 0)
                req_trophies = clan_info.get("requiredTrophies", 0)
                clan_type_raw = clan_info.get("type", "")

                with co1:
                    st.metric(t["total_members"], f"{members_count} / 50")
                with co2:
                    st.metric(t["clan_score"], f"🏆 {clan_score:,}")
                with co3:
                    st.metric(t["war_trophies"], f"⚔️ {war_trophies:,}")

                co4, co5, co6 = st.columns(3)
                with co4:
                    st.metric(t["donations_week"], f"🎁 {donations_pw:,}")
                with co5:
                    st.metric(t["required_trophies"], f"🔒 {req_trophies:,}")
                with co6:
                    clan_type = t.get("type_" + clan_type_raw, clan_type_raw)
                    st.metric(t["clan_type"], f"📋 {clan_type}")

                war_log = cliente.get_clan_war_log(clan_tag)
                if war_log:
                    st.markdown("---")
                    total_wars = len(war_log)
                    first_places = sum(1 for w in war_log if w["rank"] == 1)
                    avg_fame = int(sum(w["fame"] for w in war_log) / total_wars)
                    win_rate_clan = round((first_places / total_wars) * 100, 1)

                    st.subheader(t["clan_war_stats"])
                    cw1, cw2, cw3, cw4 = st.columns(4)
                    with cw1:
                        st.metric(t["wars_played"], f"⚔️ {total_wars}")
                    with cw2:
                        st.metric(t["wars_won"], f"🥇 {first_places}")
                    with cw3:
                        st.metric(t["clan_win_rate"], f"📈 {win_rate_clan}%")
                    with cw4:
                        st.metric(t["avg_fame"], f"🔥 {avg_fame:,}")

            with tab2:
                miembros = cliente.get_clan_members(clan_tag)
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
                nombres = [m[t["col_name"]] for m in miembros_limpios]
                tags_raw = [m["tag"] for m in miembros.get("items", [])]
                nombre_tag = dict(zip(nombres, tags_raw))

                jugador_elegido = st.selectbox(t["select_player"], nombres, key="clan_select")
                if jugador_elegido:
                    with st.spinner("⏳"):
                        member_data = cliente.get_player_data(nombre_tag[jugador_elegido])
                        member_stats = cliente.get_player_stats(member_data, t)

                    st.subheader(f"{t['player_stats']}: {jugador_elegido}")
                    c1, c2, c3, c4 = st.columns(4)
                    keys = list(member_stats.keys())
                    vals = list(member_stats.values())
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

            with tab3:
                participantes = cliente.get_clan_war_participation(clan_tag)
                participantes_limpios = cliente.extract_war_participants(participantes, t)
                st.subheader(t["war_list"])
                st.dataframe(participantes_limpios, width='stretch', height=400, hide_index=True)

                # Stats de guerra del clan
                war_log = cliente.get_clan_war_log(clan_tag)
                if war_log:
                    st.markdown("---")
                    total_wars = len(war_log)
                    first_places = sum(1 for w in war_log if w["rank"] == 1)
                    avg_fame = int(sum(w["fame"] for w in war_log) / total_wars)
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