import { useEffect, useState } from "react";
import {
  createPatient,
  fetchPatients,
  fetchDoctors,
  createToken,
  fetchTodayTokens,
} from "../api/staff";
import { connectWebSocket, addWebSocketListener, removeWebSocketListener } from "../api/websocket";


export default function StaffDashboard() {
  // --------------------
  // STATE
  // --------------------
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [tokens, setTokens] = useState([]);

  const [patientForm, setPatientForm] = useState({
    name: "",
    age: "",
    email: "",
    phone: "",
  });

  const [selectedPatient, setSelectedPatient] = useState("");
  const [selectedDoctor, setSelectedDoctor] = useState("");

  // --------------------
  // LOAD INITIAL DATA
  // --------------------
  useEffect(() => {
    loadAll();
    connectWebSocket();

    const onMessage = (data) => {
     if (
    data.event === "TOKEN_CREATED" ||
    data.event === "TOKEN_STATUS_UPDATED"
  ) {
    loadAll();
  }
};

    addWebSocketListener(onMessage);

    return () => {
      removeWebSocketListener(onMessage);
    };
  }, []);

  const loadAll = async () => {
    try {
      const [p, d, t] = await Promise.all([
        fetchPatients(),
        fetchDoctors(),
        fetchTodayTokens(),
      ]);

      setPatients(p.data);
      setDoctors(d.data);
      setTokens(t.data);
    } catch (err) {
      console.error(err);
    }
  };

  // --------------------
  // HANDLERS
  // --------------------
  const handlePatientSubmit = async (e) => {
    e.preventDefault();
    try {
      await createPatient({
        ...patientForm,
        age: Number(patientForm.age),
      });
      setPatientForm({ name: "", age: "", email: "", phone: "" });
      loadAll();
      alert("Patient registered");
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert("Patient already exists or error");
    }
  };

  const handleCreateToken = async () => {
    try {
      await createToken({
        patient_id: selectedPatient,
        doctor_id: selectedDoctor,
      });
      setSelectedPatient("");
      setSelectedDoctor("");
      loadAll();
      alert("Token generated");
    } catch (err) {
      console.error(err.response?.data || err.message);
      alert("Failed to create token");
    }
  };

  // --------------------
  // UI
  // --------------------
  return (
    <div className="min-h-screen bg-slate-300 p-6">
      <div className="max-w-7xl mx-auto space-y-10">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-slate-800">
            Staff Dashboard
          </h1>
          <p className="text-slate-500 mt-1">
            Manage patients and generate tokens for doctors
          </p>
        </div>

        {/* Top Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Register Patient */}
          <section className="bg-white/80 backdrop-blur-sm border border-slate-200 rounded-2xl p-6 shadow-lg space-y-4">
            <h2 className="text-xl font-semibold text-slate-800">
              Register Patient
            </h2>

            <form
              onSubmit={handlePatientSubmit}
              className="grid grid-cols-1 sm:grid-cols-2 gap-4"
            >
              <input
                placeholder="Full Name"
                value={patientForm.name}
                onChange={(e) =>
                  setPatientForm({ ...patientForm, name: e.target.value })
                }
                required
                className="border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />

              <input
                placeholder="Age"
                type="number"
                value={patientForm.age}
                onChange={(e) =>
                  setPatientForm({ ...patientForm, age: e.target.value })
                }
                required
                className="border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />

              <input
                placeholder="Email (optional)"
                value={patientForm.email}
                onChange={(e) =>
                  setPatientForm({ ...patientForm, email: e.target.value })
                }
                className="border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />

              <input
                placeholder="Phone (optional)"
                value={patientForm.phone}
                onChange={(e) =>
                  setPatientForm({ ...patientForm, phone: e.target.value })
                }
                className="border border-slate-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />

              <button className="sm:col-span-2 bg-emerald-600 text-white py-2.5 rounded-xl font-medium hover:bg-emerald-700 transition">
                Register Patient
              </button>
            </form>
          </section>

          {/* Generate Token */}
          <section className="bg-white/80 backdrop-blur-sm border border-slate-200 rounded-2xl p-6 shadow-lg space-y-4">
            <h2 className="text-xl font-semibold text-slate-800">
              Generate Token
            </h2>

            <select
              value={selectedPatient}
              onChange={(e) => setSelectedPatient(e.target.value)}
              className="border border-slate-300 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Select Patient</option>
              {patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name}
                </option>
              ))}
            </select>

            <select
              value={selectedDoctor}
              onChange={(e) => setSelectedDoctor(e.target.value)}
              className="border border-slate-300 rounded-lg px-4 py-2 w-full focus:outline-none focus:ring-2 focus:ring-emerald-500"
            >
              <option value="">Select Doctor</option>
              {doctors.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.email} — {d.specialty}
                </option>
              ))}
            </select>

            <button
              onClick={handleCreateToken}
              disabled={!selectedPatient || !selectedDoctor}
              className="bg-slate-300 text-black p-2.5 rounded-xl font-medium hover:bg-slate-500 transition disabled:opacity-50"
            >
              Create Token
            </button>
          </section>
        </div>

        {/* Today's Tokens */}
        <section className="space-y-4">
          <h2 className="text-xl font-semibold text-slate-800">
            Today's Tokens
          </h2>

          {tokens.length === 0 ? (
            <p className="text-slate-500 text-sm">No tokens generated yet.</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tokens.map((t) => (
                <div
                  key={t.id}
                  className="bg-white/90 backdrop-blur-sm border border-slate-200 rounded-2xl p-4 shadow hover:shadow-lg transition"
                >
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-bold text-emerald-700">
                      Token #{t.token_number}
                    </span>
                    <span
                      className={`px-2 py-1 rounded-full text-xs font-semibold ${
                        t.status === "waiting"
                          ? "bg-yellow-100 text-yellow-800"
                          : "bg-green-100 text-green-700"
                      }`}
                    >
                      {t.status.toUpperCase()}
                    </span>
                  </div>

                  <p className="text-sm text-slate-600">
                    <b>Patient:</b> {t.patient?.name}
                  </p>
                  <p className="text-sm text-slate-600">
                    <b>Email:</b> {t.patient?.email}
                  </p>
                  <p className="text-sm text-slate-600">
                    <b>Patient ID:</b> {t.patient_id}
                  </p>
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
