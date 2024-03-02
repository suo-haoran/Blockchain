from brownie import FundMe, network, config, MockV3Aggregator
from scripts.utils import LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS, get_account, deploy_mocks

def deploy_fund_me():
    account = get_account()
    active_network = network.show_active()
    if active_network not in LOCAL_TEST_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config['networks'][active_network]['eth_usd_price_feed']
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    
    fund_me = FundMe.deploy(price_feed_address,{'from': account}, publish_source=config['networks'][active_network].get('verify'))
    
    print(f'Contract deployed to {fund_me.address}')
    return fund_me


# Run script: brownie run scripts/deploy.py --network ganache-local-test
# Remember to open ganache-ui for this.
def main():
    deploy_fund_me()