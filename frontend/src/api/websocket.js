let socket = null;
let listeners = [];

export const connectWebSocket = () => {
  if (socket) return;

  socket = new WebSocket("ws://127.0.0.1:8000/ws/tokens");

  socket.onopen = () => {
    console.log("WebSocket connected");
  };

  socket.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      listeners.forEach((cb) => cb(data));
    } catch (e) {
      console.error("WebSocket parse error", e);
    }
  };

  socket.onclose = () => {
    socket = null;
    console.log("WebSocket disconnected");
  };

  socket.onerror = (e) => {
    console.error("WebSocket error", e);
  };
};

export const addWebSocketListener = (cb) => {
  listeners.push(cb);
};

export const removeWebSocketListener = (cb) => {
  listeners = listeners.filter((l) => l !== cb);
};
