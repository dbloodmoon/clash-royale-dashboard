from clash_client import ClashRoyaleClient

client = ClashRoyaleClient()

player_data = client.get_player_data("#V08J9VG88")
clan_data = client.get_clan_members("#GPV00L2R")

info = client.extract_relevant_info(player_data)
miembros = client.extract_clan_members(clan_data)

print(miembros[0])