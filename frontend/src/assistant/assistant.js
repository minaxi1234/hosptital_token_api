import api from "../api/axios";

// Send a question to the backend
export const askAssistant = async (question) => {
  try {
    const response = await api.post("/assistant/ask", { question });
    return response.data; // { question: "...", answer: "..." }
  } catch (error) {
    console.error("Assistant API error:", error);
    return { question, answer: "Assistant is temporarily unavailable." };
  }
};
