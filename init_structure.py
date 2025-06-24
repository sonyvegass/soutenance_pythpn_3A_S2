import os

regions = ["Paris", "Marseille", "Rennes", "Grenoble"]
clients = ["Client1", "Client2"]

base_dir = "./New_Tech"

for region in regions:
    for client in clients:
        path = os.path.join(base_dir, region, client)
        os.makedirs(path, exist_ok=True)

print("Structure créée.")
