// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.0;

import "@openzeppelin/contracts/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract WallToken is ERC20, Ownable {

    using SafeMath for uint;

    struct User {
        address inviter;
        address self;
    }

    struct Post {
        string format;
        string post;
    }

    mapping(address => User) public tree;
    mapping(string => bool) public supported_formats;
    mapping(address => Post[]) public posts;

    uint public current_price;
    uint public invite_reward;
    uint public min_entry_stake;
    uint public reward_chain_length;
    uint public price_increase_amount;

    uint public post_price;

    modifier isRegister(address user) {
        require(tree[user].self == user, "Sender doesn't already register");
        _;
    }

    constructor() public ERC20("WallToken", "WAT") {
        tree[msg.sender] = User(msg.sender, msg.sender);

        current_price = 5 wei;
        invite_reward = 10;
        min_entry_stake = 100;
        reward_chain_length = 10;
        price_increase_amount = 1;

        post_price = 100;

        _mint(msg.sender, 100);
    }

    function mint(uint amount) external
        onlyOwner 
    {
        _mint(owner(), amount);
    }

    function mint(address to, uint amount) external 
        onlyOwner 
        isRegister(to) 
    {
        _mint(to, amount);
    }

    function buy() external payable isRegister(msg.sender) {
        _buy(msg.sender, msg.value);
    }

    function register(address inviter) external payable {
        require(min_entry_stake <= msg.value.div(current_price));
        require(tree[msg.sender].inviter == address(0), "Sender already exist");
        require(tree[inviter].self == inviter, "Inviter doesn't exist");

        tree[msg.sender] = User(inviter, msg.sender);
        _buy(msg.sender, msg.value);

        uint counter = 0;
        User memory current = tree[msg.sender];
        while (current.self != current.inviter) {
            _mint(current.inviter, invite_reward);
            current = tree[current.inviter];
            counter++;
            if (counter >= reward_chain_length) {
                break;
            }
        }

        current_price = current_price.add(price_increase_amount);
        emit UserRegistered(msg.sender);
    }

    function make_wall_post(string memory format, string memory post) external isRegister(msg.sender) {
        require(balanceOf(msg.sender) >= post_price, "Insufficient funds");
        require(supported_formats[format], "Format unsupported");

        _burn(msg.sender, post_price);
        posts[msg.sender].push(Post(format, post));

        emit PostCreated(msg.sender, format, post);
    }

    function withdraw(uint amount) external onlyOwner {
        require(address(this).balance >= amount, "Insufficient funds");
        msg.sender.transfer(amount);
    }

    function withdraw(address payable to, uint amount) external onlyOwner {
        require(address(this).balance >= amount, "Insufficient funds");
        to.transfer(amount);
    }

    function addFormat(string memory format) external onlyOwner {
        require(!supported_formats[format], "Format already added");
        supported_formats[format] = true;
    }

    function setCurrentPrice(uint price) external onlyOwner {
        current_price = price;
    }

    function setInviteReward(uint reward) external onlyOwner {
        invite_reward = reward;
    }

    function setMinEntryStake(uint stake) external onlyOwner {
        min_entry_stake = stake;
    }

    function setRewardChainLength(uint length) external onlyOwner {
        reward_chain_length = length;
    }

    function setPriceIncreaseAmount(uint amount) external onlyOwner {
        price_increase_amount = amount;
    }

    function _buy(address payable who, uint eth_amount) private {
        uint token_to_mint = eth_amount.div(current_price);
        uint remainder = eth_amount.sub(token_to_mint.mul(current_price));

        _mint(who, token_to_mint);
        who.transfer(remainder);
    }

    // Called when new user registered 
    event UserRegistered(address user);

    // Called when new post created
    event PostCreated(address user, string format, string post);
}