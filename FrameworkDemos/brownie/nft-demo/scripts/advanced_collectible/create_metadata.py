import os
from brownie import AdvancedCollectible, network
import requests
from scripts.utils import get_breed
from metadata.sample_metadata import Metadata
from pathlib import Path

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        collectible_metadata = None
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else: 
            print(f"Creating Metadata file: {metadata_file_name}")
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            # Upload image to IPFS, or you can use pinata, checkout upload_to_pinata.py
            # Download IPFS Command-line at https://docs.ipfs.io/install/command-line/#official-distributions
            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]
            collectible_metadata = Metadata(breed, f"An adorable {breed} pup!", image_uri, [{"trait_type": "cuteness", "value": 100}])
            with open(metadata_file_name, "w") as file:
                file.write(str(collectible_metadata))
            
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(file_path):
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001" # Run `ipfs daemon` to checkout the url.
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()['Hash']
        filename = file_path.split("/")[-1]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri


