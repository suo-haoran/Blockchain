import { useWeb3Contract } from "react-moralis";
import { contractAddresses, abi } from "../constants";
// Need to declare provider in _app.js
import { useMoralis } from "react-moralis";
import { useEffect, useState } from "react";
import { ethers } from "ethers";
// Need to declare provider in _app.js
import { useNotification } from "web3uikit";

export default function LotteryEntrance() {
  const { chainId: chainIdHex, isWeb3Enabled } = useMoralis();
  const chainId = parseInt(chainIdHex);
  const lotteryAddress =
    chainId in contractAddresses ? contractAddresses[chainId][0] : null;

  // Trigger a re-render when variable updated.
  const [entranceFee, setEntranceFee] = useState("0");

  const dispatch = useNotification();

  const {
    runContractFunction: enterRaffle,
    data: enterTxResponse,
    isLoading,
    isFetching,
} = useWeb3Contract({
    abi: abi,
    contractAddress: raffleAddress,
    functionName: "enterRaffle",
    msgValue: entranceFee,
    params: {},
})

/* View Functions */

const { runContractFunction: getEntranceFee } = useWeb3Contract({
    abi: abi,
    contractAddress: raffleAddress, // specify the networkId
    functionName: "getEntranceFee",
    params: {},
})

const { runContractFunction: getPlayersNumber } = useWeb3Contract({
    abi: abi,
    contractAddress: raffleAddress,
    functionName: "getNumberOfPlayers",
    params: {},
})

const { runContractFunction: getRecentWinner } = useWeb3Contract({
    abi: abi,
    contractAddress: raffleAddress,
    functionName: "getRecentWinner",
    params: {},
})

async function updateUIValues() {
    // Another way we could make a contract call:
    // const options = { abi, contractAddress: raffleAddress }
    // const fee = await Moralis.executeFunction({
    //     functionName: "getEntranceFee",
    //     ...options,
    // })
    const entranceFeeFromCall = (await getEntranceFee()).toString()
    const numPlayersFromCall = (await getPlayersNumber()).toString()
    const recentWinnerFromCall = await getRecentWinner()
    setEntranceFee(entranceFeeFromCall)
    setNumberOfPlayers(numPlayersFromCall)
    setRecentWinner(recentWinnerFromCall)
}

useEffect(() => {
    if (isWeb3Enabled) {
        updateUIValues()
    }
}, [isWeb3Enabled])
// no list means it'll update everytime anything changes or happens
// empty list means it'll run once after the initial rendering
// and dependencies mean it'll run whenever those things in the list change

// An example filter for listening for events, we will learn more on this next Front end lesson
// const filter = {
//     address: raffleAddress,
//     topics: [
//         // the name of the event, parnetheses containing the data type of each event, no spaces
//         utils.id("RaffleEnter(address)"),
//     ],
// }

const handleNewNotification = () => {
    dispatch({
        type: "info",
        message: "Transaction Complete!",
        title: "Transaction Notification",
        position: "topR",
        icon: "bell",
    })
}

// Probably could add some error handling
const handleSuccess = async (tx) => {
    await tx.wait(1)
    updateUIValues()
    handleNewNotification(tx)
}

return (
    <div className="p-5">
        <h1 className="py-4 px-4 font-bold text-3xl">Lottery</h1>
        {raffleAddress ? (
            <>
                <button
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-auto"
                    onClick={async () =>
                        await enterRaffle({
                            // onComplete:
                            // onError:
                            onSuccess: handleSuccess,
                            onError: (error) => console.log(error),
                        })
                    }
                    disabled={isLoading || isFetching}
                >
                    {isLoading || isFetching ? (
                        <div className="animate-spin spinner-border h-8 w-8 border-b-2 rounded-full"></div>
                    ) : (
                        "Enter Raffle"
                    )}
                </button>
                <div>Entrance Fee: {ethers.utils.formatUnits(entranceFee, "ether")} ETH</div>
                <div>The current number of players is: {numberOfPlayers}</div>
                <div>The most previous winner was: {recentWinner}</div>
            </>
        ) : (
            <div>Please connect to a supported chain </div>
        )}
    </div>
)
}