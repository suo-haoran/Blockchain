import {ConnectButton} from "web3uikit";

// Does everything that manualheader does. But FANCIER, BETTER.
export default function Header() {
    return (
        <div>
            <h1>Decentralized Lottery</h1>
            <ConnectButton moralisAuth={false}/>
        </div>
    )
}