import { SignerWithAddress } from '@nomiclabs/hardhat-ethers/signers';
import { assert } from 'chai';
import { ethers, deployments, network } from 'hardhat';
import { developmentChains } from '../../helper-hardhat-config';
import { FundMe } from '../../typechain';

developmentChains.includes(network.name)
    ? describe.skip
    : describe('FundMe', function () {
          let fundMe: FundMe;
          let deployer: SignerWithAddress;
          const sendValue = ethers.utils.parseEther('1');
          this.beforeEach(async () => {
              deployer = (await ethers.getSigners())[0];
              await deployments.fixture(['all']);
              fundMe = await ethers.getContract('FundMe', deployer);
          });

          it('allows people to fund and withdraw', async () => {
              await fundMe.fund({ value: sendValue });
              await fundMe.withdraw();
              const endingFundMeBalance = await fundMe.provider.getBalance(
                  fundMe.address
              );
              assert.equal(endingFundMeBalance.toString(), '0');
          });
      });
