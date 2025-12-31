import { useEffect, useState } from "react";
import { fetchDoctorTokens, updateTokenStatus } from "../api/doctor";
import { FaUserCircle } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
import { connectWebSocket, addWebSocketListener, removeWebSocketListener } from "../api/websocket";

export default function DoctorDashboard() {
  const navigate = useNavigate();
  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(true);

  
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

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) navigate("/login");
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


  const handleComplete = async (tokenId) => {
    try {
      await updateTokenStatus(tokenId, "completed");
      loadTokens();
    } catch (err) {
      console.error(err.response?.data || err.message);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-800 to-gray-900">
        <p className="text-gray-200 text-lg animate-pulse">
          Loading patient queue...
        </p>
      </div>
    );
  }
  const handleStart = async (tokenId) => {
  await updateTokenStatus(tokenId, "in_progress");
  loadTokens();
};


  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-800 to-gray-500 p-6">
      <div className="max-w-5xl mx-auto space-y-6">

        {/* Header */}
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-white">Doctor Dashboard</h1>
          <p className="text-gray-300 mt-1">Today's patient token queue</p>
        </div>

        {/* Tokens Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {tokens.length === 0 ? (
            <div className="col-span-full bg-gray-700 rounded-2xl p-6 text-center text-gray-300 font-medium">
              No active tokens.
            </div>
          ) : (
            tokens.map((t) => (
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
                    <span
                      className={`text-xs px-3 py-1 rounded-full font-semibold ${
                        t.status === "waiting"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-green-100 text-green-800"
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

                {/* Right: Action */}
                {t.status === "waiting" && (
                  <button
                    onClick={() => handleStart(t.id)}
                    className="self-start sm:self-center bg-green-600 text-white px-6 py-2 rounded-xl font-medium hover:bg-green-700 transition"
                  >
                    Start
                  </button>
                )}
                {t.status === "in_progress" && (
            <button onClick={() => handleComplete(t.id)}className="self-start sm:self-center bg-green-600 text-white px-6 py-2 rounded-xl font-medium hover:bg-green-700 transition">Complete</button>
          )}

              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
