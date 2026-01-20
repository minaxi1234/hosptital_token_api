// src/pages/AssistantPage.jsx
import { useState } from "react";
import AssistantChat from "../assistant/AssistantChat";
import { askAssistant } from "../assistant/assistant";

export default function AssistantPage() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (question) => {
    setMessages((prev) => [...prev, { sender: "user", text: question }]);
    setLoading(true);

    try {
      const res = await askAssistant(question);
      setMessages((prev) => [
        ...prev,
        { sender: "assistant", text: res.answer },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: "assistant", text: "Assistant unavailable. Try again." },
      ]);
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleClearChat = () => {
    setMessages([]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 flex items-center justify-center px-4">
      <div className="w-full max-w-5xl">
        
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-4xl font-bold text-white">
              Hospital Assistant
            </h1>
            <p className="text-gray-400 text-sm mt-1">
              AI-powered hospital inquiries
            </p>
          </div>

          <button
            onClick={handleClearChat}
            className="bg-gray-700 hover:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm"
          >
            New Chat
          </button>
        </div>

        <AssistantChat
          messages={messages}
          onSend={handleSend}
          loading={loading}
        />
      </div>
    </div>
  );
}
