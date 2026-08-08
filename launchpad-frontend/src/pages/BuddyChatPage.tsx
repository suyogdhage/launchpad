import { useState, useRef, useEffect } from "react";
import { Input, Button, Typography, Spin, Avatar } from "antd";
import { SendOutlined, RobotOutlined, UserOutlined } from "@ant-design/icons";
import { useChat, useChatHistory } from "../hooks/useBuddy";
import { LaunchpadLogo } from "../components/illustrations/LaunchpadLogo";

interface Message {
  role: "user" | "assistant";
  content: string;
}

export default function BuddyChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm your Onboarding Buddy. I can help you check your pending tasks or submit requests. What would you like to do?",
    },
  ]);
  const [input, setInput] = useState("");
  const [historyLoaded, setHistoryLoaded] = useState(false);
  const chatMutation = useChat();
  const { data: history } = useChatHistory();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (history && !historyLoaded) {
      const prior = history.map((m) => ({ role: m.role, content: m.content }));
      if (prior.length) {
        setMessages(prior);
      }
      setHistoryLoaded(true);
    }
  }, [history, historyLoaded]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    const userMsg: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    chatMutation.mutate(
      { message: input },
      {
        onSuccess: (data) => {
          setMessages((prev) => [
            ...prev,
            { role: "assistant", content: data.reply },
          ]);
        },
        onError: () => {
          setMessages((prev) => [
            ...prev,
            {
              role: "assistant",
              content: "Sorry, I encountered an error. Please try again.",
            },
          ]);
        },
      }
    );
  };

  return (
    <div style={{ maxWidth: 700, margin: "0 auto" }}>
      <div
        className="brand-gradient"
        style={{ borderRadius: 16, padding: "18px 24px", display: "flex", alignItems: "center", gap: 14, marginBottom: 16 }}
      >
        <LaunchpadLogo size={40} variant="white" />
        <div>
          <Typography.Title level={4} style={{ color: "#fff", margin: 0 }}>
            <RobotOutlined /> Onboarding Buddy
          </Typography.Title>
          <Typography.Text style={{ color: "rgba(255,255,255,0.85)", fontSize: 13 }}>
            Your AI assistant for onboarding questions
          </Typography.Text>
        </div>
      </div>
      <div
        style={{
          height: 420,
          overflowY: "auto",
          border: "1px solid #ece9f6",
          borderRadius: 14,
          padding: 20,
          marginBottom: 16,
          background: "#fbfaff",
        }}
      >
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
              marginBottom: 16,
              gap: 10,
            }}
          >
            {msg.role === "assistant" && (
              <Avatar
                size={32}
                icon={<RobotOutlined />}
                style={{ background: "linear-gradient(135deg, #a855f7, #6a15e8)", flexShrink: 0 }}
              />
            )}
            <div
              style={{
                maxWidth: "75%",
                padding: "12px 16px",
                borderRadius: 14,
                background: msg.role === "user" ? "#863bff" : "#ffffff",
                color: msg.role === "user" ? "#fff" : "#1f2330",
                border: msg.role === "assistant" ? "1px solid #e6e1f5" : "none",
                boxShadow: "0 1px 3px rgba(16,24,40,0.06)",
              }}
            >
              <div style={{ marginBottom: 4, fontSize: 12, opacity: 0.75 }}>
                {msg.role === "user" ? "You" : "Buddy"}
              </div>
              {msg.content}
            </div>
            {msg.role === "user" && (
              <Avatar
                size={32}
                icon={<UserOutlined />}
                style={{ background: "#c4a8ff", flexShrink: 0 }}
              />
            )}
          </div>
        ))}
        {chatMutation.isPending && (
          <div style={{ textAlign: "center", padding: 8 }}>
            <Spin size="small" /> Buddy is thinking...
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div style={{ display: "flex", gap: 8 }}>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onPressEnter={handleSend}
          placeholder="Ask about your tasks or submit a request..."
          disabled={chatMutation.isPending}
          size="large"
          style={{ borderRadius: 10 }}
        />
        <Button
          type="primary"
          icon={<SendOutlined />}
          onClick={handleSend}
          loading={chatMutation.isPending}
          size="large"
          style={{ background: "linear-gradient(135deg, #a855f7, #6a15e8)", border: "none" }}
        >
          Send
        </Button>
      </div>
    </div>
  );
}
