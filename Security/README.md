# Most Common Attacks
- Reentrancy
- Oracle Manipulation

# Before Deploying ANYTHING
- Run slither
- Look Manually for oracle manipulation examples or reentrancy attack


# Slither Setup
Run it in Security Toolbox OR Setup manually.
CD to work directory and run:
```shell
conda activate blockchain
pip3 install solc-select slither-analyzer
```

In package.json, add script
```json
"scripts": {
    "slither": "slither . --solc-remaps '@openzeppelin=node_modules/@openzeppelin @chainlink=node_modules/@chainlink' --exclude naming-convention,external-function,low-level-calls"
}
```

To run slither:
```shell
yarn slither
```

# Security Toolbox Setup
Requires docker, go install [docker](https://docs.docker.com/engine/install/ubuntu/)

```shell
docker pull trailofbits/eth-security-toolbox
```

In package.json, add script
```json
"scripts": {
    "toolbox": "docker run -it --rm -v $PWD:/src trailofbits/eth-security-toolbox"
}
```

Run `sudo yarn toolbox` to start the interactive terminal.

To run Echidna, See `test/fuzzing`. We specify a `config.yaml` for it. In security toolbox terminal, enter this command:
```shell
echidna-test /src/contracts/test/fuzzing/VaultFuzzTest.sol --contract VaultFuzzTest --config /src/contracts/test/fuzzing/config.yaml
```
