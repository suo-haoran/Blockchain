// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract BasicNft is ERC721 {
    // Dont use https links for nfts, use ipfs://, 
    // this also applies to that token image in this TOKEN_URI. 
    // Bad: "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png"
    // Good: "ipfs://QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png"
    // NOTE: ipfs:// requires ipfs gateway, readup on that.
    string public constant TOKEN_URI =
        "ipfs://bafybeig37ioir76s7mg5oobetncojcm3c3hxasyd4rvid4jqhy4gkaheg4/?filename=0-PUG.json";
    
    uint256 private s_tokenCounter;
    
    constructor() ERC721("Dogie", "DOG") {
        s_tokenCounter = 0;
    }

    function mintNft()
        public
        returns (uint256)
    {
        uint256 newTokenId = s_tokenCounter;
        _safeMint(msg.sender, newTokenId);
        s_tokenCounter = s_tokenCounter + 1;
        return newTokenId;
    }

    function getTokenCounter() public view returns(uint256) {
        return s_tokenCounter;
    }

    function tokenURI(uint256 /*tokenId*/) public pure override returns (string memory) {
        return TOKEN_URI;
    }
}
