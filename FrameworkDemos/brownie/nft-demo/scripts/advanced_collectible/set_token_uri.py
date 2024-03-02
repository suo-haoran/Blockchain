from brownie import network, AdvancedCollectible
from scripts.utils import OPENSEA_URL, get_account, get_breed


dog_metadata_dict = {
    "PUG": "https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.json",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmdryoExpgEQQQgJPoruwGJyZmz6SqV4FRTX1i73CT3iXn?filename=1-SHIBA_INU.json",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmbBnUjyHHN7Ytq9xDsYF9sucZdDJLRkWz7vnZfrjMXMxs?filename=2-ST_BERNARD.json",
}


def main():
    print(f"Working on {network.show_active()}")
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        if not str(advanced_collectible.tokenURI(token_id)).startswith("https://"):
            print(f"Setting tokenURI of {token_id}")
            set_token_uri(token_id, advanced_collectible, dog_metadata_dict[breed])


def set_token_uri(token_id, nft_contract, token_uri):
    acc = get_account()
    txn = nft_contract.setTokenURI(token_id, token_uri, {"from": acc})
    txn.wait(1)
    print(f"AWESOME! YOU CAN VIEW YOUR NFT AT {OPENSEA_URL.format(nft_contract.address, token_id)}")
    print("Please wait up to 20 mins, and hit the refresh metadata button")