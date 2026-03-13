#%%
from transmission_rpc import Client

client = Client(host='localhost', port=9091)
torrents = client.get_torrents()
print(f"Connected OK. Active torrents: {len(torrents)}")

# %%
