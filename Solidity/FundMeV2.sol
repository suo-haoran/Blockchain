// SPDX-License-Identifier: MIT
// NOTE: Checkout solidity-by-example.org
// Another NOTE: Remember to use gas saving tricks
// Smart contract that lets anyone deposit ETH into the contract
// Only the owner of the contract can withdraw the ETH
pragma solidity ^0.8.8;

import "./PriceConverter.sol";

error NotOwner();

contract FundMe {
    using PriceConverter for uint256;
    // 18 digit number to be compared with donated amount 
    // adding constant saves gas: (23515 - 21415) * 141000000000 = (almost $1 USD.)
    uint256 public constant MINIMUM_USD = 50 * 1e18;
    //mapping to store which address depositeded how much ETH
    mapping(address => uint256) public addressToAmountFunded;
    // array of addresses who deposited
    address[] public funders;
    //address of the owner (who deployed the contract)
    // saves (23644 - 21508) gas
    address public immutable i_owner;
    
    // the first person to deploy the contract is
    // the owner
    constructor() public {
        i_owner = msg.sender;
    }
    
    function fund() public payable {
        //is the donated amount less than 50USD?
        // if this require fails, the remaining gas (gas required after this require statement) will be sent back to the sender.
        require(msg.value.getConversionRate() >= MINIMUM_USD, "You need to spend more ETH!");
        //if not, add to mapping and funders array
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
   
    
    //modifier: https://medium.com/coinmonks/solidity-tutorial-all-about-modifiers-a86cf81c14cb
    modifier onlyOwner {
    	//is the message sender owner of the contract?
        // require(msg.sender == i_owner, "Sender is not owner");
        // Gas saver: using revert + error declared at the top, we dont need to store err msg which saves gas.
        if (msg.sender != i_owner) {
            revert NotOwner();
        }
        _;
    }
    
    // onlyOwner modifer will first check the condition inside it 
    // and 
    // if true, withdraw function will be executed 
    function withdraw() payable onlyOwner public {
        //iterate through all the mappings and make them 0
        //since all the deposited amount has been withdrawn
        for (uint256 funderIndex=0; funderIndex < funders.length; funderIndex++){
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        //funders array will be initialized to 0
        funders = new address[](0);
    	
        // three different ways to send ether: transfer, send, call
        // transfer: throws error when fails
        // need to cast msg.sender address to payable address
        payable(msg.sender).transfer(address(this).balance);

        // send: returns a bool, won't throw error
        // bool sendSuccess = payable(msg.sender).send(address(this).balance);
        // require(sendSuccess, "Send failed.");

        // call (low-level): returns a bool, won't throw error
        (bool callSuccess,) = payable(msg.sender).call{value: address(this).balance}("");
        require(callSuccess, "Send failed.");
        // Checkout solidity by example send ether section.
    }

    // What happens if some funders send money to the contract straight away? 
    // It won't trigger the fund function. Then how can we keep track of them if we were to issue some rewards or something?
    // Checkout FallbackExample.sol for more info.
    receive() external payable {
        // Redirect the txn to fund().
        fund();
    }
      
    fallback() {
        // Redirect the txn to fund().
        fund();
    }
}
