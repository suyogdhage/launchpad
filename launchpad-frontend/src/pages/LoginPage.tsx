import { Card, Form, Input, Button, Typography, Alert, Space, ConfigProvider, theme as antdTheme } from "antd";
import {
  LockOutlined,
  MailOutlined,
  RocketOutlined,
  TeamOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useLogin } from "../hooks/useAuth";
import { useState } from "react";
import { OnboardingIllustration } from "../components/illustrations/OnboardingIllustration";
import logo from "../assets/logo-text-cropped.png";

export default function LoginPage() {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { login } = useAuth();
  const loginMutation = useLogin();
  const [error, setError] = useState("");

  const onFinish = async (values: { email: string; password: string }) => {
    setError("");
    loginMutation.mutate(values, {
      onSuccess: (data) => {
        login(data.token);
        const role = JSON.parse(atob(data.token.split(".")[1])).role;
        if (role === "hr" || role === "superadmin") {
          navigate("/dashboard");
        } else {
          navigate("/tasks");
        }
      },
      onError: (err: any) => {
        setError(err.response?.data?.detail || "Login failed");
      },
    });
  };

  const features = [
    { icon: <RocketOutlined />, text: "Guided onboarding tasks from day one" },
    { icon: <TeamOutlined />, text: "A personal buddy to answer your questions" },
    { icon: <SafetyCertificateOutlined />, text: "Secure document uploads & approvals" },
  ];

  return (
    <ConfigProvider
      theme={{ algorithm: antdTheme.defaultAlgorithm, token: { colorPrimary: "#863bff", borderRadius: 10 } }}
    >
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: 24,
        position: "relative",
        overflow: "hidden",
        background: "linear-gradient(135deg, #6d28d9 0%, #7c3aed 45%, #a855f7 100%)",
      }}
    >
      <div
        style={{
          position: "absolute",
          width: 420,
          height: 420,
          borderRadius: "50%",
          top: -140,
          left: -120,
          background: "radial-gradient(circle, rgba(255,255,255,0.22), transparent 70%)",
        }}
      />
      <div
        style={{
          position: "absolute",
          width: 520,
          height: 520,
          borderRadius: "50%",
          bottom: -200,
          right: -160,
          background: "radial-gradient(circle, rgba(240,171,252,0.35), transparent 70%)",
        }}
      />

      <Card
        style={{
          width: 920,
          maxWidth: "100%",
          height: "min(540px, calc(100vh - 48px))",
          borderRadius: 24,
          overflow: "hidden",
          padding: 0,
        boxShadow: "0 24px 64px rgba(30,10,60,0.45)",
        position: "relative",
      }}
      styles={{ body: { padding: 0, height: "100%" } }}
    >
        <div style={{ display: "flex", flexWrap: "nowrap", height: "100%", minHeight: 0 }}>
          <div
            style={{
              flex: "1 1 460px",
              minWidth: 0,
              background: "linear-gradient(150deg, #574C91 0%, #6358A0 55%, #6D5DA6 100%)",
              color: "#fff",
              padding: "24px 28px",
              display: "flex",
              flexDirection: "column",
              position: "relative",
              overflow: "hidden",
            }}
          >
            <div
              style={{
                position: "absolute",
                inset: 0,
                background:
                  "radial-gradient(circle at 15% 12%, rgba(255,255,255,0.16), transparent 42%), radial-gradient(circle at 85% 90%, rgba(240,171,252,0.22), transparent 45%)",
              }}
            />
            <div style={{ position: "relative", display: "flex", justifyContent: "center", marginBottom: 12, width: "100%" }}>
              <img
                src={logo}
                alt="Launchpad"
                style={{
                  width: "100%",
                  maxWidth: 300,
                  height: "auto",
                  objectFit: "contain",
                }}
              />
            </div>

            <Typography.Title level={1} style={{ color: "#fff", margin: 0, marginBottom: 4, fontSize: 28 }}>
              Welcome to your new journey
            </Typography.Title>

            <div style={{ display: "flex", justifyContent: "center", margin: "2px 0", width: "100%", maxWidth: 240, alignSelf: "center" }}>
              <OnboardingIllustration width="100%" />
            </div>

            <Space direction="vertical" size={6} style={{ marginTop: "auto", width: "100%", paddingTop: 6 }}>
              {features.map((f) => (
                <div
                  key={f.text}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                    background: "rgba(255,255,255,0.14)",
                    border: "1px solid rgba(255,255,255,0.22)",
                    borderRadius: 10,
                    padding: "6px 12px",
                    fontSize: 12.5,
                  }}
                >
                  <span style={{ color: "#a5f3fc" }}>{f.icon}</span>
                  <span>{f.text}</span>
                </div>
              ))}
            </Space>
          </div>

          <div
            style={{
              flex: "1 1 380px",
              minWidth: 0,
              background: "#ffffff",
              padding: "32px 28px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              overflow: "hidden",
            }}
          >
            <Typography.Title level={3} style={{ margin: 0, marginBottom: 4 }}>
              Sign in
            </Typography.Title>
            <Typography.Text type="secondary" style={{ display: "block", marginBottom: 24 }}>
              Access your onboarding workspace
            </Typography.Text>

            {error && <Alert message={error} type="error" showIcon style={{ marginBottom: 16 }} />}

            <Form form={form} layout="vertical" onFinish={onFinish} autoComplete="off">
              <Form.Item
                name="email"
                label="Email"
                rules={[
                  { required: true, message: "Please enter your email" },
                  { type: "email", message: "Invalid email" },
                ]}
              >
                <Input prefix={<MailOutlined />} placeholder="you@company.com" size="large" />
              </Form.Item>
              <Form.Item
                name="password"
                label="Password"
                rules={[{ required: true, message: "Please enter your password" }]}
              >
                <Input.Password prefix={<LockOutlined />} placeholder="••••••••" size="large" />
              </Form.Item>
              <Form.Item style={{ marginBottom: 8 }}>
                <Button
                  type="primary"
                  htmlType="submit"
                  block
                  size="large"
                  loading={loginMutation.isPending}
                  style={{
                    background: "linear-gradient(135deg, #a855f7, #6d28d9)",
                    border: "none",
                    height: 44,
                    fontWeight: 600,
                  }}
                >
                  Log in
                </Button>
              </Form.Item>
            </Form>

            <div style={{ textAlign: "center", marginTop: 8 }}>
              <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                Secured by Launchpad
              </Typography.Text>
            </div>
          </div>
        </div>
      </Card>
    </div>
    </ConfigProvider>
  );
}
