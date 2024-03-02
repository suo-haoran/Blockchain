// SPDX-License-Identifier: MIT

// Smart contract that lets anyone deposit ETH into the contract
// Only the owner of the contract can withdraw the ETH
pragma solidity ^0.8.7;

contract FallbackExample {
    uint256 public result;

    // Special function, don't add function keyword infront.
    // If you send money to this contract without any data, it will automatically call the receive function
    // In remix, deploy this contract and change Value to 1 Wei and
    // click on low level transactions, leave the Calldata empty and click transact.
    // In the logs you can see the To field is FallbackExample.(receive)!
    receive() external payable {
        result = 1;
    }

    // Same as receive but allows data.
    // Put some data in the Calldata. 
    // As long as it doesn't match function signature, it will call the fallback function.
    fallback() external payable {
        result = 2;
    }
}

    // Explainer from: https://solidity-by-example.org/fallback/
    // Ether is sent to contract
    //      is msg.data empty?
    //          /           \ 
    //         yes          no
    //         /             \
    //    receive() exists?  fallback() 
    //     /   \ 
    //   yes   no
    //  /        \
    //receive()  fallback()