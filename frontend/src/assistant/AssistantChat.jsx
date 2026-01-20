// src/assistant/AssistantChat.jsx
import { useState, useRef, useEffect } from "react";

export default function AssistantChat({ messages, onSend }) {
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  };

  return (
    <div className="flex flex-col h-[78vh] bg-[#0f172a] border border-gray-700 rounded-2xl shadow-2xl overflow-hidden">
      
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-6 py-6 space-y-5">
        {messages.length === 0 && (
          <div className="text-gray-400 text-center mt-32">
            <p className="text-lg font-medium">Hospital Assistant</p>
            <p className="text-sm mt-2">
              Ask anything about timings, doctors, departments, or services.
            </p>
          </div>
        )}

        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[72%] px-5 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-wrap ${
                msg.sender === "user"
                  ? "bg-blue-600 text-white rounded-br-md"
                  : "bg-[#1e293b] text-gray-100 rounded-bl-md"
              }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        <div ref={chatEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-700 bg-[#020617] px-4 py-4">
        <div className="flex gap-3 items-center">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask a question..."
            className="flex-1 bg-[#020617] text-white px-4 py-3 rounded-xl border border-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 placeholder-gray-400"
          />
          <button
            onClick={handleSend}
            className="bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white px-6 py-3 rounded-xl font-medium transition"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
