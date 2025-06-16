import React, { useEffect, useRef, useState } from "react";
import { marked } from "marked";

const USER_AVATAR = "/assets/samson.jpg";
const SIDEKICK_AVATAR = "https://ui-avatars.com/api/?name=SK&background=059669&color=fff";
const LLM_MODEL = "GPT-4o";

function MessageBubble({ content, type }) {
  const isUser = type === "user";
  const isAssistant = type === "assistant";
  const isFeedback = type === "feedback";

  let bubbleClass =
    "max-w-[75%] mb-4 px-5 py-3 rounded-3xl text-base leading-relaxed shadow-lg break-words";
  if (isUser) {
    bubbleClass +=
      " bg-gradient-to-br from-green-900 to-green-600 text-white ml-auto text-left";
  } else if (isAssistant) {
    bubbleClass +=
      " bg-gradient-to-br from-green-800 to-green-900 text-gray-100 mr-auto text-left";
  } else if (isFeedback) {
    bubbleClass +=
      " bg-gray-800 text-yellow-300 italic mr-auto text-left";
  }

  return (
    <div className={bubbleClass}>
      {isUser ? (
        <span>{content}</span>
      ) : (
        <span
          dangerouslySetInnerHTML={{ __html: marked.parse(content) }}
        />
      )}
    </div>
  );
}

function ChatApp() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const ws = useRef(null);
  const chatRef = useRef(null);

  useEffect(() => {
    ws.current = new WebSocket("ws://localhost:8000/ws");
    ws.current.onopen = () => {
      setMessages((msgs) => [
        ...msgs,
        { content: "Connected to Sidekick. You can start chatting!", type: "system" },
      ]);
    };
    ws.current.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.type === "response") {
        const data = response.data;
        setMessages(data.map((msg) => ({
          content: msg.content,
          type:
            msg.role === "assistant" && msg.content.startsWith("Evaluator feedback")
              ? "feedback"
              : msg.role,
        })));
      }
    };
    ws.current.onclose = () => {
      setMessages((msgs) => [
        ...msgs,
        { content: "Disconnected from server. Please refresh the page.", type: "system" },
      ]);
    };
    ws.current.onerror = () => {
      setMessages((msgs) => [
        ...msgs,
        { content: "Error connecting to server. Please refresh the page.", type: "system" },
      ]);
    };
    return () => ws.current && ws.current.close();
  }, []);

  useEffect(() => {
    if (chatRef.current) {
      chatRef.current.scrollTop = chatRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    const newMessages = [
      ...messages,
      { content: input, type: "user" },
    ];
    setMessages(newMessages);
    ws.current.send(
      JSON.stringify({
        message: input,
        history: newMessages.map((m) => ({
          role: m.type === "user" ? "user" : "assistant",
          content: m.content,
        })),
      })
    );
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSend();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-green-900 via-black to-gray-900 font-sans">
      <div className="w-full max-w-2xl mx-auto py-8">
        <div className="bg-black/80 rounded-2xl shadow-2xl overflow-hidden border border-gray-800">
          <div className="p-8 text-center border-b border-gray-800">
            <h1 className="text-4xl font-bold tracking-wide text-white">Personnel Sidekick</h1>
            <p className="mt-2 text-gray-400">Your AI Assistant</p>
          </div>
          <div
            ref={chatRef}
            className="h-96 overflow-y-auto p-6 space-y-4 bg-transparent"
            id="chat-container"
          >
            {messages.map((msg, idx) => {
              if (msg.type === "system") {
                return (
                  <div key={idx} className="text-center text-gray-400 text-sm">
                    {msg.content}
                  </div>
                );
              }
              const isUser = msg.type === "user";
              const avatar = isUser ? USER_AVATAR : SIDEKICK_AVATAR;
              return (
                <div
                  key={idx}
                  className={`flex items-start mb-6 ${
                    isUser ? "flex-row-reverse justify-end" : "flex-row justify-start"
                  }`}
                >
                  <img
                    src={avatar}
                    alt={isUser ? "You" : "Sidekick"}
                    className="w-10 h-10 rounded-full object-cover mx-3 border-2 border-gray-800 bg-gray-900 shadow"
                  />
                  <div className="flex flex-col" style={{ alignItems: isUser ? "flex-end" : "flex-start" }}>
                    <span
                      className={`font-semibold mb-1 flex items-center gap-2 ${
                        isUser ? "text-blue-400" : msg.type === "assistant" ? "text-cyan-300" : "text-yellow-400"
                      }`}
                    >
                      {isUser
                        ? "You"
                        : msg.type === "assistant"
                        ? <>
                            Sidekick
                            <span className="bg-gray-900 text-lime-400 text-xs font-bold rounded px-2 py-0.5 border border-gray-700 ml-1">
                              {LLM_MODEL}
                            </span>
                          </>
                        : "Evaluator"}
                    </span>
                    <MessageBubble content={msg.content} type={msg.type} />
                  </div>
                </div>
              );
            })}
          </div>
          <div className="p-4 border-t border-gray-800 bg-black/90">
            <div className="flex space-x-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                className="flex-1 px-4 py-3 bg-gray-800 text-white border border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-gray-400"
                placeholder="Type your message..."
              />
              <button
                onClick={handleSend}
                type="button"
                className="bg-green-500 hover:bg-green-600 transition-colors w-12 h-12 rounded-lg flex items-center justify-center shadow"
              >
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="#fff" className="w-7 h-7">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M13 6l6 6-6 6" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatApp; 