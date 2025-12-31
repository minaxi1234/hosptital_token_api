import { useEffect, useState } from "react";
import {
  connectWebSocket,
  addWebSocketListener,
  removeWebSocketListener,
} from "../api/websocket";

import { fetchPublicTodayTokens } from "../api/public";

export default function TokenDisplay() {
  const [tokens, setTokens] = useState([]);

  useEffect(() => {
    // 1️⃣ Initial fetch
    fetchPublicTodayTokens()
      .then((res) => {
        setTokens(res.data.filter(t => t.status !== "completed"));
      })
      .catch(console.error);

    // 2️⃣ Connect WebSocket
    connectWebSocket();

    const onMessage = (data) => {
      console.log("WS EVENT:", data);

      if (
        data.event === "TOKEN_CREATED" ||
        data.event === "TOKEN_STATUS_UPDATED"
      ) {
        fetchPublicTodayTokens()
          .then((res) => {
            setTokens(res.data.filter(t => t.status !== "completed"));
          })
          .catch(console.error);
      }
    };

    addWebSocketListener(onMessage);

    return () => {
      removeWebSocketListener(onMessage);
    };
  }, []);

  const nowServing = tokens.filter(t => t.status === "in_progress");
  const waiting = tokens.filter(t => t.status === "waiting");


  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center p-10">
      <h1 className="text-5xl font-bold mb-10">Now Serving</h1>
      {tokens.length === 0 && (
  <div className="text-3xl text-gray-400 mt-20">
    No tokens right now
  </div>
)}


{/* NOW SERVING SECTION */}
{nowServing.length > 0 && (
  <div className="mb-20 text-center">
    <h2 className="text-4xl mb-8 text-green-400 font-semibold">
      Now Serving
    </h2>

    <div className="flex justify-center gap-20">
      {nowServing.map((t) => (
        <div
          key={t.id}
          className="bg-green-600 px-24 py-16 rounded-3xl shadow-2xl animate-pulse"
        >
          <div className="text-9xl font-extrabold">
            {t.token_number}
          </div>
        </div>
      ))}
    </div>
  </div>
)}

{/* WAITING SECTION */}
{waiting.length > 0 && (
  <>
    <h2 className="text-3xl mb-8 text-gray-400">
      Waiting
    </h2>

    <div className="grid grid-cols-4 gap-12 text-center opacity-80">
      {waiting.map((t) => (
        <div key={t.id}>
          <div className="text-6xl font-bold">
            {t.token_number}
          </div>
          <div className="text-lg text-gray-400">
            Waiting
          </div>
        </div>
      ))}
    </div>
  </>
)}

    </div>
  );
}
