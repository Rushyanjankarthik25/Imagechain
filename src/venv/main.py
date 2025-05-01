from steganography import encode_and_upload, showData
from blockchain import *

def main():
    # Connect to blockchain
    web3 = connect_to_blockchain()
    if not web3:
        return

    # Select Ethereum account
    accounts = web3.eth.accounts
    print("\nAvailable Ethereum Accounts:")
    for i, acc in enumerate(accounts):
        print(f"{i + 1}. {acc}")
    acc_index = int(input("Select an account (number): ")) - 1
    selected_account = accounts[acc_index]
    print(f"Using Ethereum account: {selected_account}")

    # Load contract
    contract_address = "0xd4D75a2849569C5538E318e6F06fA75F62EeD00e"  # Replace with your contract address
    contract_abi = [
      {
        "anonymous": False,
        "inputs": [
          {
            "indexed": True,
            "internalType": "uint256",
            "name": "id",
            "type": "uint256"
          },
          {
            "indexed": False,
            "internalType": "string",
            "name": "ipfsHash",
            "type": "string"
          },
          {
            "indexed": False,
            "internalType": "string",
            "name": "title",
            "type": "string"
          },
          {
            "indexed": False,
            "internalType": "string",
            "name": "description",
            "type": "string"
          },
          {
            "indexed": True,
            "internalType": "address",
            "name": "owner",
            "type": "address"
          },
          {
            "indexed": False,
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "name": "ImageCreated",
        "type": "event"
      },
      {
        "anonymous": False,
        "inputs": [
          {
            "indexed": True,
            "internalType": "uint256",
            "name": "id",
            "type": "uint256"
          },
          {
            "indexed": False,
            "internalType": "string",
            "name": "title",
            "type": "string"
          },
          {
            "indexed": False,
            "internalType": "string",
            "name": "description",
            "type": "string"
          }
        ],
        "name": "MetadataUpdated",
        "type": "event"
      },
      {
        "anonymous": False,
        "inputs": [
          {
            "indexed": True,
            "internalType": "uint256",
            "name": "id",
            "type": "uint256"
          },
          {
            "indexed": True,
            "internalType": "address",
            "name": "previousOwner",
            "type": "address"
          },
          {
            "indexed": True,
            "internalType": "address",
            "name": "newOwner",
            "type": "address"
          }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
      },
      {
        "inputs": [],
        "name": "imageCounter",
        "outputs": [
          {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
          }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
      },
      {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "",
            "type": "uint256"
          }
        ],
        "name": "images",
        "outputs": [
          {
            "internalType": "string",
            "name": "ipfsHash",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "title",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "description",
            "type": "string"
          },
          {
            "internalType": "address",
            "name": "owner",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
      },
      {
        "inputs": [
          {
            "internalType": "string",
            "name": "_ipfsHash",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "_title",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "_description",
            "type": "string"
          }
        ],
        "name": "addImage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "id",
            "type": "uint256"
          },
          {
            "internalType": "address",
            "name": "newOwner",
            "type": "address"
          }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "id",
            "type": "uint256"
          },
          {
            "internalType": "string",
            "name": "_title",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "_description",
            "type": "string"
          }
        ],
        "name": "updateImageMetadata",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
      },
      {
        "inputs": [
          {
            "internalType": "uint256",
            "name": "id",
            "type": "uint256"
          }
        ],
        "name": "getImage",
        "outputs": [
          {
            "internalType": "string",
            "name": "ipfsHash",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "title",
            "type": "string"
          },
          {
            "internalType": "string",
            "name": "description",
            "type": "string"
          },
          {
            "internalType": "address",
            "name": "owner",
            "type": "address"
          },
          {
            "internalType": "uint256",
            "name": "timestamp",
            "type": "uint256"
          }
        ],
        "stateMutability": "view",
        "type": "function",
        "constant": True
      }
    ]  # Same ABI as before (keep unchanged)

    contract = load_contract(web3, contract_address, contract_abi)
    if not contract:
        return

    # Console menu
    while True:
        print("\n1. Encode and Upload")
        print("2. Decode and Retrieve")
        print("3. Transfer Ownership")
        print("4. Update Metadata")
        print("5. Exit")
        choice = input("Your choice: ")

        if choice == "1":
            ipfs_hash = encode_and_upload()
            if ipfs_hash:
                image_id = add_image_to_blockchain(web3, contract, ipfs_hash, selected_account)
                if image_id:
                    print(f"Use this Image ID to retrieve metadata later: {image_id}")
        elif choice == "2":
            decode_and_retrieve(contract)
        elif choice == "3":
            transfer_image_ownership(web3, contract, selected_account)
        elif choice == "4":
            update_image_metadata(web3, contract, selected_account)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
