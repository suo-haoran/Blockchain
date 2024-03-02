// SPDX-License-Identifier: SEE LICENSE IN LICENSE
pragma solidity 0.8.7;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "base64-sol/base64.sol";
import "hardhat/console.sol";

contract DynamicSvgNft is ERC721, Ownable {
  uint256 private s_tokenCounter;
  string private i_lowImageUri;
  string private i_highImageUri;
  string private constant SVG_URI_PREFIX = "data:image/svg+xml;base64,";
  AggregatorV3Interface internal immutable i_priceFeed;
  mapping(uint256 => int256) public s_tokenIdToHighValue;

  event CreatedNFT(uint256 indexed tokenId, int256 highValue);

  constructor(
    address priceFeedAddress,
    string memory lowSvg,
    string memory highSvg
  ) ERC721("Dynamic SVG NFT", "DSN") {
    s_tokenCounter = 0;
    i_lowImageUri = svgToImageUri(lowSvg);
    i_highImageUri = svgToImageUri(highSvg);
    i_priceFeed = AggregatorV3Interface(priceFeedAddress);
  }

  function mintNft(int256 highValue) public {
    s_tokenIdToHighValue[s_tokenCounter] = highValue;
    emit CreatedNFT(s_tokenCounter, highValue);
    _safeMint(msg.sender, s_tokenCounter);
    s_tokenCounter = s_tokenCounter + 1;
  }

  function svgToImageUri(string memory svg)
    public
    pure
    returns (string memory)
  {
    // encode SVG to Base64,
    // Go https://base64.guru/converter/encode/image/svg and encode some svgs
    // then in your browser address bar, "data:image/svg+xml;base64,<base64 encoding here>" <- copy the base64 encoding and place here
    string memory svgBase64Encoded = Base64.encode(
      bytes(string(abi.encodePacked(svg)))
    );
    return string(abi.encodePacked(SVG_URI_PREFIX, svgBase64Encoded));
  }

  function _baseURI() internal pure override returns (string memory) {
    return "data:application/json;base64,";
  }

  function tokenURI(uint256 tokenId)
    public
    view
    override
    returns (string memory)
  {
    require(_exists(tokenId), "URI Query for nonexistant token.");
    string memory imageURI = i_lowImageUri;
    (, int256 price, , , ) = i_priceFeed.latestRoundData();
    if (price >= s_tokenIdToHighValue[tokenId]) {
      imageURI = i_highImageUri;
    }
    bytes memory encodedMetadata = bytes(
      abi.encodePacked(
        '{"name":"',
        name(), // You can add whatever name here
        '", "description":"An NFT that changes based on the Chainlink Feed", ',
        '"attributes": [{"trait_type": "coolness", "value": 100}], "image":"',
        imageURI,
        '"}'
      )
    );
    string memory encodedMetadataInBase64 = Base64.encode(encodedMetadata);
    string memory encodedMetadataURI = string(
      abi.encodePacked(_baseURI(), encodedMetadataInBase64)
    );
    return encodedMetadataURI;
  }

  function getLowSVG() public view returns (string memory) {
    return i_lowImageUri;
  }

  function getHighSVG() public view returns (string memory) {
    return i_highImageUri;
  }

  function getPriceFeed() public view returns (AggregatorV3Interface) {
    return i_priceFeed;
  }

  function getTokenCounter() public view returns (uint256) {
    return s_tokenCounter;
  }
}
