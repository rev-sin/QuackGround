import os
import requests
from web3 import Web3
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class NFTCreator:
    def __init__(self):
        self.pinata_api_key = os.getenv("PINATA_API_KEY")
        self.pinata_secret = os.getenv("PINATA_SECRET_API_KEY")
        self.private_key = os.getenv("WALLET_PRIVATE_KEY")
        self.contract_address = os.getenv("LAZAI_CONTRACT_ADDRESS")
        self.rpc_url = os.getenv("DUCKCHAIN_RPC_URL")

        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))

        # Load contract ABI (you'll need to get this from LazAi)
        self.contract_abi = self._get_contract_abi()

        # Set up account
        self.account = self.w3.eth.account.from_key(self.private_key)

    def _get_contract_abi(self):
        # You'll need to get the actual ABI from LazAi
        # This is a simplified example
        return [
            {
                "inputs": [
                    {"internalType": "address", "name": "to", "type": "address"},
                    {"internalType": "string", "name": "tokenURI", "type": "string"},
                ],
                "name": "mint",
                "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function",
            }
        ]

    def upload_to_pinata(self, file_path, metadata=None):
        """Upload file and metadata to Pinata"""
        headers = {
            "pinata_api_key": self.pinata_api_key,
            "pinata_secret_api_key": self.pinata_secret,
        }

        # Upload image
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(
                "https://api.pinata.cloud/pinning/pinFileToIPFS",
                headers=headers,
                files=files,
            )

        if response.status_code != 200:
            raise Exception(f"Failed to upload image: {response.text}")

        image_ipfs_hash = response.json()["IpfsHash"]
        image_url = f"ipfs://{image_ipfs_hash}"

        # Create and upload metadata
        if metadata is None:
            metadata = {
                "name": Path(file_path).stem,
                "description": "NFT created with LazAi on DuckChain",
                "image": image_url,
                "attributes": [],
            }
        else:
            metadata["image"] = image_url
            if "name" not in metadata or not metadata["name"]:
                metadata["name"] = Path(file_path).stem


        response = requests.post(
            "https://api.pinata.cloud/pinning/pinJSONToIPFS",
            headers=headers,
            json={"pinataContent": metadata},
        )

        if response.status_code != 200:
            raise Exception(f"Failed to upload metadata: {response.text}")

        metadata_ipfs_hash = response.json()["IpfsHash"]
        return f"ipfs://{metadata_ipfs_hash}"

    def mint_nft(self, to_address, token_uri):
        """Mint NFT on DuckChain using LazAi contract"""
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=self.contract_abi,
        )

        # Build transaction
        transaction = contract.functions.mint(
            Web3.to_checksum_address(to_address), token_uri
        ).build_transaction(
            {
                "from": self.account.address,
                "nonce": self.w3.eth.get_transaction_count(self.account.address),
                "gas": 200000,
                "gasPrice": self.w3.eth.gas_price,
            }
        )

        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)

        # Send transaction
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for transaction receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt

    def create_nft(self, image_path, metadata=None, recipient_address=None):
        """Complete NFT creation process"""
        if recipient_address is None:
            recipient_address = self.account.address

        print("Uploading to Pinata...")
        token_uri = self.upload_to_pinata(image_path, metadata)

        print("Minting NFT on DuckChain...")
        receipt = self.mint_nft(recipient_address, token_uri)

        print("NFT created successfully!")
        print(f"Transaction Hash: {receipt.transactionHash.hex()}")
        print(f"Token URI: {token_uri}")

        return receipt, token_uri


def main():
    # Initialize NFT creator
    nft_creator = NFTCreator()

    # Create NFT
    image_path = input("Enter path to your image file: ").strip()

    # Optional metadata
    custom_metadata = {
        "name": input("NFT name (press enter for default): ").strip() or None,
        "description": input("NFT description (press enter for default): ").strip()
        or None,
        "attributes": [
            {"trait_type": "Creator", "value": "LazAi User"},
            {"trait_type": "Blockchain", "value": "DuckChain Testnet"},
        ],
    }

    # Remove None values
    custom_metadata = {k: v for k, v in custom_metadata.items() if v is not None}

    # Create the NFT
    try:
        receipt, token_uri = nft_creator.create_nft(
            image_path=image_path, metadata=custom_metadata if custom_metadata else None
        )
        print("\nNFT Creation Complete!")
        print(
            f"View on explorer: https://www.oklink.com/duckchain-testnet/{receipt.transactionHash.hex()}"
        )
        print(f"Token URI: {token_uri}")

    except Exception as e:
        print(f"Error creating NFT: {e}")


if __name__ == "__main__":
    main()
