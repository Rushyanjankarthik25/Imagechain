# utils.py
import ipfshttpclient

def connect_to_ipfs():
    try:
        client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')  # Local IPFS node
        return client
    except Exception as e:
        print(f"Error connecting to IPFS: {e}")
        return None

def upload_to_ipfs(image_path):
    client = connect_to_ipfs()
    if client:
        try:
            res = client.add(image_path)
            return res['Hash']  # Return the IPFS hash
        except Exception as e:
            print(f"Error uploading to IPFS: {e}")
    return None