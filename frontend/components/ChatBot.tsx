"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { MessageCircle, X, ChevronLeft } from "lucide-react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function ChatBot() {
  const [isOpen, setIsOpen] = useState(true);
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm Dingkang's AI assistant. Feel free to ask me anything about his work, projects, or experience in AI and autonomous driving.",
    },
  ]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [sessionId] = useState(() => {
    return `session_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`;
  });
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = { role: "user", content };
    setMessages((prev) => [...prev, userMessage]);
    setIsStreaming(true);

    const assistantMessage: Message = { role: "assistant", content: "" };
    setMessages((prev) => [...prev, assistantMessage]);

    try {
      const apiUrl =
        process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: content,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) throw new Error("No response body");

      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split("\n\n");
        buffer = events.pop() || "";

        for (const event of events) {
          const lines = event.split("\n");
          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const data = JSON.parse(line.slice(6));
                if (data.type === "text" && data.content) {
                  setMessages((prev) => {
                    const updated = [...prev];
                    const lastMsg = updated[updated.length - 1];
                    if (lastMsg.role === "assistant") {
                      updated[updated.length - 1] = {
                        ...lastMsg,
                        content: lastMsg.content + data.content,
                      };
                    }
                    return updated;
                  });
                } else if (data.type === "done") {
                  setIsStreaming(false);
                }
              } catch {
                // Skip malformed JSON
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Chat error:", error);
      setMessages((prev) => {
        const updated = [...prev];
        const lastMsg = updated[updated.length - 1];
        if (lastMsg.role === "assistant" && lastMsg.content === "") {
          updated[updated.length - 1] = {
            ...lastMsg,
            content:
              "Sorry, I'm having trouble connecting right now. Please try again later.",
          };
        }
        return updated;
      });
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <>
      {/* Floating chat panel */}
      <div
        className={`fixed top-4 right-4 bottom-4 z-50 w-[480px] flex flex-col bg-dark-950/95 backdrop-blur-xl border border-dark-700 rounded-2xl shadow-[0_0_60px_rgba(0,0,0,0.5)] transition-transform duration-300 ease-in-out ${
          isOpen ? "translate-x-0" : "translate-x-[calc(100%+2rem)]"
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-3.5 border-b border-dark-800 rounded-t-2xl">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            <h3 className="text-sm font-semibold text-dark-100">
              Chat with AI
            </h3>
          </div>
          <button
            onClick={() => setIsOpen(false)}
            className="p-1.5 rounded-lg hover:bg-dark-800 transition-colors"
            aria-label="Close chat"
          >
            <X className="w-4 h-4 text-dark-400" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto chat-scrollbar p-5 space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          {isStreaming && (
            <div className="flex items-center gap-1 px-3 py-2">
              <span className="typing-dot w-1.5 h-1.5 bg-accent rounded-full" />
              <span className="typing-dot w-1.5 h-1.5 bg-accent rounded-full" />
              <span className="typing-dot w-1.5 h-1.5 bg-accent rounded-full" />
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="border-t border-dark-800 rounded-b-2xl p-4">
          <ChatInput onSend={handleSendMessage} disabled={isStreaming} />
        </div>
      </div>

      {/* Re-open tab (visible when chat is closed) */}
      <button
        onClick={() => setIsOpen(true)}
        className={`fixed right-0 top-1/2 -translate-y-1/2 z-50 flex items-center gap-1.5 px-2.5 py-3 bg-dark-900 border border-dark-700 border-r-0 rounded-l-xl shadow-lg shadow-black/30 hover:bg-dark-800 transition-all duration-300 ${
          isOpen
            ? "opacity-0 pointer-events-none translate-x-full"
            : "opacity-100 translate-x-0"
        }`}
        aria-label="Open chat"
      >
        <ChevronLeft className="w-4 h-4 text-accent" />
        <MessageCircle className="w-4 h-4 text-accent" />
      </button>
    </>
  );
}
