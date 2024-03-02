// Need to declare provider in _app.js
import { useMoralis } from "react-moralis";
import { useEffect } from "react";

export default function ManualHeader() {
  const { enableWeb3, account, isWeb3Enabled, isWeb3EnableLoading, Moralis, deactivateWeb3 } = useMoralis();

  // It runs twice because of strict mode.
  // If there's no dependency array, it will run anytime something re-renders.
  // CAREFUL with this!! Because you can get circular render.
  // Empty dependency array -> update on load once(if strict mode enabled: twice).
  useEffect(() => {
    if (isWeb3Enabled) return;
    if (typeof window !== "undefined" && window.localStorage.getItem("connected")) 
      enableWeb3();
    console.log("Hi!");
    console.log(isWeb3Enabled);
  }, [isWeb3Enabled]);

  useEffect(() => {
    Moralis.onAccountChanged((acc) => {
      console.log(`Account changed to ${acc}`);
      if (acc == null) {
        window.localStorage.removeItem("connected");
        deactivateWeb3();
        console.log("Null account found!");
      }
    })
  }, [])

  return (
    <div>
      {account ? (
        <div>
          Connected to {account.slice(0, 6)}...
          {account.slice(account.length - 4)}
        </div>
      ) : (
        <button
          onClick={async () => {
            await enableWeb3();
            if (typeof window !== "undefined") {
              window.localStorage.setItem("connected", "inject");
            }
          }}
          disabled={isWeb3EnableLoading}
        >
          Connect
        </button>
      )}
    </div>
  );
}
