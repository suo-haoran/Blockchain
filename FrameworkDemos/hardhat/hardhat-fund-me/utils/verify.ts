import { run } from 'hardhat';

export async function verify(contractAddress: String, args: any[]) {
    console.log('Verifying contract...');
    // verify task added by etherscan
    try {
        await run('verify:verify', {
            address: contractAddress,
            constructorArguments: args,
        });
    } catch (e: any) {
        if (e.message.toLowerCase().includes('already verified')) {
            console.log('Already verified!');
        } else {
            console.log(e);
        }
    }
}
