import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timezone

class ClashRoyaleClient:
    def __init__(self):
        """
        El constructor. Aquí inicializamos lo necesario para que 
        nuestro cliente funcione apenas se cree.
        """
        load_dotenv()
        
        # Intenta leer de .env (local) o de st.secrets (Streamlit Cloud)
        self.token = os.getenv("CLASH_TOKEN")
        
        if not self.token:
            try:
                import streamlit as st
                self.token = st.secrets["CLASH_TOKEN"]
            except Exception:
                pass
        
        if not self.token:
            raise ValueError("No se encontró el CLASH_TOKEN. Revisa tu .env o los Secrets de Streamlit Cloud.")
        
        self.base_url = "https://api.clashroyale.com/v1/"
        self.headers = {
            'Authorization': "Bearer " + self.token
        }

    def _format_tag(self, tag: str) -> str:
        """Formatea el tag del jugador o clan para la API."""
        if tag.startswith('#'):
            return "%23" + tag[1:]
        return "%23" + tag

    def _format_date(self, iso_date_str: str, t: dict) -> str:
        if not iso_date_str:
            return t["not_available"]
        
        try:
            dt = datetime.strptime(iso_date_str, "%Y%m%dT%H%M%S.%fZ")
            dt = dt.replace(tzinfo=timezone.utc)
            ahora = datetime.now(timezone.utc)
            diferencia = ahora - dt
            dias = diferencia.days
            
            if dias >= 1:
                return t["days_ago"].format(dias, t["plural_s"] if dias > 1 else "")
            
            horas = diferencia.seconds // 3600
            if horas >= 1:
                return t["hours_ago"].format(horas, t["plural_s"] if horas > 1 else "")
                
            minutos = (diferencia.seconds % 3600) // 60
            if minutos <= 5:
                return t["online"]
            else:
                return t["minutes_ago"].format(minutos)
                
        except Exception:
            return iso_date_str


    def get_player_data(self, player_tag: str) -> dict:
        """
        Obtiene los datos crudos de un jugador desde la API.
        """
        formatted_tag = self._format_tag(player_tag)
        url = self.base_url + "players/" + formatted_tag
        response = requests.request("GET", url, headers=self.headers)
        return response.json()


    def extract_relevant_info(self, raw_data: dict, t: dict) -> dict:
        """
        Toma el JSON gigante de la API y devuelve nuestro diccionario limpio.
        """
        limpio = {
            t["col_name"]: raw_data["name"],
            t["col_clan"]: raw_data.get("clan", {}).get("name", "Sin Clan"), 
            t["col_trophies"]: raw_data["trophies"],
            t["col_level"]: raw_data["expLevel"]
        }
        return limpio

    def get_player_stats(self, raw_data: dict, t: dict) -> dict:
        """
        Toma los datos crudos de un jugador y extrae sus estadísticas de combate.
        Calcula el win rate a partir de victorias y batallas totales.
        """
        wins = raw_data.get("wins", 0)
        losses = raw_data.get("losses", 0)
        battle_count = raw_data.get("battleCount", 0)
        three_crown_wins = raw_data.get("threeCrownWins", 0)
        best_trophies = raw_data.get("bestTrophies", 0)
        challenge_max_wins = raw_data.get("challengeMaxWins", 0)
        war_day_wins = raw_data.get("warDayWins", 0)
        
        win_rate = round((wins / battle_count) * 100, 1) if battle_count > 0 else 0
        
        return {
            t["stat_wins"]: wins,
            t["stat_losses"]: losses,
            t["stat_battles"]: battle_count,
            t["stat_win_rate"]: f"{win_rate}%",
            t["stat_three_crowns"]: three_crown_wins,
            t["stat_best_trophies"]: best_trophies,
            t["stat_challenge_max"]: challenge_max_wins,
            t["stat_war_wins"]: war_day_wins,
        }

    def get_clan_info(self, clan_tag: str) -> dict:
        """
        Obtiene la información general del clan desde la API.
        Endpoint: /clans/{clanTag}
        """
        formatted_tag = self._format_tag(clan_tag)
        url = self.base_url + "clans/" + formatted_tag
        response = requests.request("GET", url, headers=self.headers)
        data = response.json()
        
        return data

    def get_clan_war_log(self, clan_tag: str) -> list:
        """
        Obtiene el historial de guerras (River Race) del clan.
        Endpoint: /clans/{clanTag}/riverracelog
        Devuelve una lista con rank, fame y trophy_change por guerra.
        """
        formatted_tag = self._format_tag(clan_tag)
        url = self.base_url + "clans/" + formatted_tag + "/riverracelog"
        response = requests.request("GET", url, headers=self.headers)
        data = response.json()
        
        wars = []
        for war in data.get("items", []):
            for standing in war.get("standings", []):
                if standing["clan"]["tag"] == clan_tag.upper():
                    wars.append({
                        "rank": standing["rank"],
                        "fame": standing["clan"].get("fame", 0),
                        "trophy_change": standing.get("trophyChange", 0),
                    })
        return wars

    def get_clan_members(self, clan_tag: str) -> dict:
        """
        Obtiene la lista cruda de miembros de un clan desde la API.
        Endpoint: /clans/{clanTag}/members
        """
        formatted_tag = self._format_tag(clan_tag)
        url = self.base_url + "clans/" + formatted_tag + "/members"
        response = requests.request("GET", url, headers=self.headers)
        return response.json()

    def extract_clan_members(self, raw_members_data: dict, t: dict) -> list:
        """
        Toma el JSON de miembros del clan y devuelve una lista de diccionarios limpios.
        """        
        miembros_limpios = []
        
        for miembro in raw_members_data.get("items", []):
            miembros_limpios.append({
                t["col_name"]: miembro["name"],
                t["col_role"]: miembro["role"],
                t["col_trophies"]: miembro["trophies"],
                t["col_donations"]: miembro.get("donations", 0),
                t["col_donations_received"]: miembro.get("donationsReceived", 0),
                t["col_last_seen"]: self._format_date(miembro.get("lastSeen", ""), t)
            })
        
        miembros_limpios.sort(key=lambda x: x[t["col_donations"]], reverse=True)
        return miembros_limpios

    def get_clan_war_participation(self, clan_tag: str) -> list:
        """
        Obtiene la lista cruda de participantes de una guerra de clan desde la API.
        Endpoint: /clans/{clanTag}/currentriverrace
        """
        formatted_tag = self._format_tag(clan_tag)
        url = self.base_url + "clans/" + formatted_tag + "/currentriverrace"
        response = requests.request("GET", url, headers=self.headers)
        datos = response.json()
        participantes = datos.get("clan", {}).get("participants", [])
        estado = datos.get("state", "Desconocido")
        return participantes, estado

    def extract_war_participants(self, raw_participants: list, t: dict) -> list:
        """
        Toma la lista cruda de participantes de guerra y devuelve una lista con llaves traducidas.
        """
        participantes_limpios = []

        for p in raw_participants:
            participantes_limpios.append({
                t["col_name"]: p.get("name", ""),
                t["col_fame"]: p.get("fame", 0),
                t["col_boat_attacks"]: p.get("boatAttacks", 0),
                t["col_decks_used"]: p.get("decksUsed", 0),
                t["col_decks_today"]: p.get("decksUsedToday", 0),
            })

        participantes_limpios.sort(key=lambda x: x[t["col_fame"]], reverse=True)
        return participantes_limpios