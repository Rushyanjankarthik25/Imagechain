from web3 import Web3
import cv2
from steganography import showData
from utils import connect_to_ipfs, upload_to_ipfs

def connect_to_blockchain():
    try:
        ganache_url = "http://127.0.0.1:7545"
        web3 = Web3(Web3.HTTPProvider(ganache_url))
        if web3.is_connected():
            print("Connected to blockchain")
            return web3
        else:
            print("Failed to connect to blockchain")
            return None
    except Exception as e:
        print(f"Error connecting to blockchain: {e}")
        return None

def load_contract(web3, contract_address, abi):
    try:
        contract = web3.eth.contract(address=contract_address, abi=abi)
        return contract
    except Exception as e:
        print(f"Error loading contract: {e}")
        return None

def add_image_to_blockchain(web3, contract, ipfs_hash, selected_account):
    title = input("Enter image title: ")
    description = input("Enter image description: ")
    
    try:
        tx = contract.functions.addImage(ipfs_hash, title, description).transact({
            'from': selected_account,
            'gas': 2000000
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx)

        print(f"Image metadata added to blockchain. Transaction hash: {receipt.transactionHash.hex()}")

        logs = contract.events.ImageCreated().process_receipt(receipt)
        
        if logs:
            image_id = logs[0]['args']['id']
            print(f"Image metadata added successfully! Image ID: {image_id}")
            return image_id
        else:
            print("Image metadata added, but no event logs found.")
            return None
    except Exception as e:
        print(f"Error adding image to blockchain: {e}")

def decode_and_retrieve(contract):
    image_name = input("Enter the name of the steganographed image (with extension): ")
    
    try:
        image = cv2.imread(image_name)
        if image is None:
            raise FileNotFoundError(f"Image file not found: {image_name}")

        text = showData(image)
        print("\nDecoded message:", text)

        image_id = int(input("Enter the image ID to retrieve metadata: "))
        metadata = contract.functions.getImage(image_id).call()

        if metadata[3] == "0x0000000000000000000000000000000000000000":
            print("Image not found in blockchain.")
        else:
            print("\nImage Metadata:")
            print(f"IPFS Hash: {metadata[0]}\nTitle: {metadata[1]}\nDescription: {metadata[2]}\nOwner: {metadata[3]}\nTimestamp: {metadata[4]}")
    except Exception as e:
        print(f"Error retrieving metadata: {e}")

def transfer_image_ownership(web3, contract, selected_account):
    try:
        image_id = int(input("Enter the image ID to transfer ownership: "))
        new_owner = input("Enter the new owner's address: ")
        
        if not web3.is_address(new_owner):
            print("Invalid Ethereum address.")
            return

        tx = contract.functions.transferOwnership(image_id, new_owner).transact({
            'from': selected_account,
            'gas': 2000000
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        print(f"Ownership transferred successfully. Transaction hash: {receipt.transactionHash.hex()}")
    except Exception as e:
        print(f"Error transferring ownership: {e}")

def update_image_metadata(web3, contract, selected_account):
    try:
        image_id = int(input("Enter the image ID to update metadata: "))
        new_title = input("Enter the new title: ")
        new_description = input("Enter the new description: ")

        tx = contract.functions.updateImageMetadata(image_id, new_title, new_description).transact({
            'from': selected_account,
            'gas': 2000000
        })
        receipt = web3.eth.wait_for_transaction_receipt(tx)
        print(f"Metadata updated successfully. Transaction hash: {receipt.transactionHash.hex()}")
    except Exception as e:
        print(f"Error updating metadata: {e}")
