import { useEffect, useState } from "react";
import { fetchDoctorTokens, updateTokenStatus } from "../api/doctor";
import { FaUserCircle } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import {
  connectWebSocket,
  addWebSocketListener,
  removeWebSocketListener,
} from "../api/websocket";

export default function DoctorDashboard() {
  const navigate = useNavigate();

  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionLoadingId, setActionLoadingId] = useState(null); // 🔒 button lock

  // ----------------------------
  // Load doctor tokens
  // ----------------------------
  const loadTokens = async () => {
    try {
      const res = await fetchDoctorTokens();
      setTokens(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // ----------------------------
  // Initial load + WebSocket
  // ----------------------------
  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      navigate("/login");
      return;
    }

    loadTokens();
    connectWebSocket();

    const onMessage = (data) => {
      if (
        data.event === "TOKEN_CREATED" ||
        data.event === "TOKEN_STATUS_UPDATED"
      ) {
        loadTokens();
      }
    };

    addWebSocketListener(onMessage);

    return () => removeWebSocketListener(onMessage);
  }, []);

  // ----------------------------
  // Start token
  // ----------------------------
  const handleStart = async (tokenId) => {
    try {
      setActionLoadingId(tokenId);
      await updateTokenStatus(tokenId, "in_progress");
    } catch (err) {
      console.error(err.response?.data || err.message);
    } finally {
      setActionLoadingId(null);
    }
  };

  // ----------------------------
  // Complete token
  // ----------------------------
  const handleComplete = async (tokenId) => {
    try {
      setActionLoadingId(tokenId);
      await updateTokenStatus(tokenId, "completed");
    } catch (err) {
      console.error(err.response?.data || err.message);
    } finally {
      setActionLoadingId(null);
    }
  };

  // ----------------------------
  // Sort tokens: in_progress → waiting → completed
  // ----------------------------
  const sortedTokens = [...tokens].sort((a, b) => {
    const order = { in_progress: 0, waiting: 1, completed: 2 };
    return order[a.status] - order[b.status];
  });

  // ----------------------------
  // Loading screen
  // ----------------------------
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
        <p className="text-gray-200 text-lg animate-pulse">
          Loading patient queue...
        </p>
      </div>
    );
  }

  // ----------------------------
  // UI
  // ----------------------------
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-800 to-gray-500 p-6">
      <div className="max-w-5xl mx-auto space-y-6">

        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-white">Doctor Dashboard</h1>
          <p className="text-gray-300 mt-1">Today's patient token queue</p>
          <button
        onClick={() => navigate("/assistant")}
        className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded"
      >
        Ask Assistant
</button>
        </div>

        {/* Tokens Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {sortedTokens.length === 0 ? (
            <div className="col-span-full bg-gray-700 rounded-2xl p-6 text-center text-gray-300 font-medium">
              No active tokens.
            </div>
          ) : (
            sortedTokens.map((t) => (
              <div
                key={t.id}
                className="bg-white rounded-2xl p-5 shadow-md flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 hover:shadow-lg transition"
              >
                {/* Left: Patient Info */}
                <div className="space-y-1 flex-1">
                  <div className="flex items-center gap-3">
                    <FaUserCircle className="text-blue-500 text-2xl" />
                    <span className="text-lg font-semibold text-gray-800">
                      Token #{t.token_number}
                    </span>

                    {/* Status badge */}
                    <span
                      className={`text-xs px-3 py-1 rounded-full font-semibold ${
                        t.status === "waiting"
                          ? "bg-yellow-100 text-yellow-800"
                          : t.status === "in_progress"
                          ? "bg-blue-100 text-blue-800"
                          : "bg-gray-200 text-gray-700"
                      }`}
                    >
                      {t.status.toUpperCase()}
                    </span>
                  </div>

                  <p className="text-gray-700">
                    <b>Patient:</b> {t.patient?.name}
                  </p>
                  <p className="text-gray-700">
                    <b>Email:</b> {t.patient?.email}
                  </p>
                  <p className="text-gray-700">
                    <b>Patient ID:</b> {t.patient_id}
                  </p>
                  <p className="text-gray-500 text-xs">
                    Created at {new Date(t.created_at).toLocaleString()}
                  </p>
                </div>

                {/* Right: Actions */}
                {t.status === "waiting" && (
                  <button
                    disabled={actionLoadingId === t.id}
                    onClick={() => handleStart(t.id)}
                    className={`self-start sm:self-center px-6 py-2 rounded-xl font-medium transition ${
                      actionLoadingId === t.id
                        ? "bg-gray-400 cursor-not-allowed"
                        : "bg-green-600 hover:bg-green-700 text-white"
                    }`}
                  >
                    {actionLoadingId === t.id ? "Starting..." : "Start"}
                  </button>
                )}

                {t.status === "in_progress" && (
                  <button
                    disabled={actionLoadingId === t.id}
                    onClick={() => handleComplete(t.id)}
                    className={`self-start sm:self-center px-6 py-2 rounded-xl font-medium transition ${
                      actionLoadingId === t.id
                        ? "bg-gray-400 cursor-not-allowed"
                        : "bg-blue-600 hover:bg-blue-700 text-white"
                    }`}
                  >
                    {actionLoadingId === t.id
                      ? "Completing..."
                      : "Complete"}
                  </button>
                )}
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
