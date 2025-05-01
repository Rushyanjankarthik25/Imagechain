// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.0;

contract ImageChain {
    // Struct to store image metadata
    struct Image {
        string ipfsHash;       // IPFS hash of the image
        string title;           // Title of the image
        string description;     // Description of the image
        address owner;          // Owner of the image
        uint256 timestamp;      // Timestamp of creation
    }

    // Mapping to store images by their unique ID
    mapping(uint256 => Image) public images;

    // Counter for generating unique image IDs
    uint256 public imageCounter;

    // Events
    event ImageCreated(
        uint256 indexed id,
        string ipfsHash,
        string title,
        string description,
        address indexed owner,
        uint256 timestamp
    );

    event OwnershipTransferred(
        uint256 indexed id,
        address indexed previousOwner,
        address indexed newOwner
    );

    // Modifier to restrict access to the owner of an image
    modifier onlyOwner(uint256 id) {
        require(images[id].owner == msg.sender, "Not the owner");
        _;
    }

    // Add a new image with metadata
    function addImage(
        string memory _ipfsHash,
        string memory _title,
        string memory _description
    ) public {
        require(bytes(_ipfsHash).length > 0, "IPFS hash required");
        require(bytes(_title).length > 0, "Title required");
        require(bytes(_description).length > 0, "Description required");
        require(bytes(_ipfsHash).length <= 64, "IPFS hash too long");
        require(bytes(_title).length <= 128, "Title too long");
        require(bytes(_description).length <= 256, "Description too long");

        // Increment counter for unique IDs
        imageCounter++;

        // Store image metadata
        images[imageCounter] = Image({
            ipfsHash: _ipfsHash,
            title: _title,
            description: _description,
            owner: msg.sender,
            timestamp: block.timestamp
        });

        // Emit event
        emit ImageCreated(imageCounter, _ipfsHash, _title, _description, msg.sender, block.timestamp);
    }

    // Transfer ownership of an image to another address
    function transferOwnership(uint256 id, address newOwner) public onlyOwner(id) {
        require(newOwner != address(0), "Invalid address");
        require(images[id].owner != address(0), "Image does not exist");

        // Emit event before changing state
        emit OwnershipTransferred(id, images[id].owner, newOwner);

        // Transfer ownership
        images[id].owner = newOwner;
    }

    event MetadataUpdated(
    uint256 indexed id,
    string title,
    string description
);

    // Update image metadata (title and description)
    function updateImageMetadata(
        uint256 id,
        string memory _title,
        string memory _description
    ) public onlyOwner(id) {
        require(bytes(_title).length > 0, "Title required");
        require(bytes(_description).length > 0, "Description required");

        images[id].title = _title;
        images[id].description = _description;

        // Emit event
        emit MetadataUpdated(id, _title, _description);
    }

    // Get metadata of an image
    function getImage(uint256 id) public view returns (
        string memory ipfsHash,
        string memory title,
        string memory description,
        address owner,
        uint256 timestamp
    ) {
        Image memory image = images[id];
        if (image.owner == address(0)) {
                return ("", "", "", address(0), 0);
            }
        return (
            image.ipfsHash,
            image.title,
            image.description,
            image.owner,
            image.timestamp
        );
    }
}