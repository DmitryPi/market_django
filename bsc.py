import requests

BSC_API_KEY = "72NV81F5MZ3PSNNBMISUE4RBFY341Y5FAN"
# API_URL = "https://api.bscscan.com/api"
API_URL = "https://api-testnet.bscscan.com/api"

# "https://api-testnet.bscscan.com/api?module=contract&action=getabi&address=0xC40c6eD98C389B9aCe25C7B264aaff748FC72c30&apikey=72NV81F5MZ3PSNNBMISUE4RBFY341Y5FAN"

"https://api-testnet.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash=0xeed430cf4c8b9d0641a1b7912b70bbf3609f19a67889e6c9aa0c635c79b01094&apikey=72NV81F5MZ3PSNNBMISUE4RBFY341Y5FAN"

params = {
    "module": "proxy",
    "action": "eth_getTransactionByHash",
    "txhash": "0xeed430cf4c8b9d0641a1b7912b70bbf3609f19a67889e6c9aa0c635c79b01094",
    "apikey": BSC_API_KEY,
}

response = requests.post(
    "https://api-testnet.bscscan.com/api?module=proxy&action=eth_getTransactionByHash&txhash=0xeed430cf4c8b9d0641a1b7912b70bbf3609f19a67889e6c9aa0c635c79b01094&apikey=72NV81F5MZ3PSNNBMISUE4RBFY341Y5FAN"
)
print(response)
# transaction = response.json()["result"]
