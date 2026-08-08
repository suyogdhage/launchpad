import {
  Row,
  Col,
  Card,
  Tag,
  Spin,
  Alert,
  Progress,
  Typography,
  theme,
} from "antd";
import {
  TeamOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  FileProtectOutlined,
  CheckOutlined,
  CloseCircleOutlined,
} from "@ant-design/icons";
import { useGetStats } from "../hooks/useDashboard";
import { useWebSocket } from "../hooks/useWebSocket";
import { useMe } from "../hooks/useUsers";
import { WelcomeIllustration } from "../components/illustrations/WelcomeIllustration";

const HERO_GRADIENT =
  "linear-gradient(135deg, #a855f7 0%, #863bff 55%, #6a15e8 100%)";

export default function DashboardPage() {
  const { data: initialStats, isLoading, error } = useGetStats();
  const { stats: liveStats } = useWebSocket();
  const { data: me } = useMe();
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  const stats = liveStats || initialStats;

  if (isLoading) return <Spin size="large" style={{ display: "block", margin: "100px auto" }} />;
  if (error) return <Alert message="Failed to load dashboard stats" type="error" />;
  if (!stats) return null;

  const totalTasks = stats.completed_tasks + stats.pending_tasks;
  const progress = totalTasks > 0 ? Math.round((stats.completed_tasks / totalTasks) * 100) : 0;

  const hour = new Date().getHours();
  const timeGreeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const firstName = me?.name?.split(" ")[0] || "there";

  const statCards = [
    {
      title: "Total New Hires",
      value: stats.total_new_hires,
      icon: <TeamOutlined />,
      accent: "#3b82f6",
    },
    {
      title: "Completed Tasks",
      value: stats.completed_tasks,
      icon: <CheckCircleOutlined />,
      accent: "#10b981",
    },
    {
      title: "Pending Tasks",
      value: stats.pending_tasks,
      icon: <ClockCircleOutlined />,
      accent: "#f59e0b",
    },
    {
      title: "Pending Reviews",
      value: stats.pending_document_reviews,
      icon: <FileProtectOutlined />,
      accent: "#ef4444",
    },
    {
      title: "Approved Documents",
      value: stats.approved_documents,
      icon: <CheckOutlined />,
      accent: "#22c55e",
    },
    {
      title: "Rejected Documents",
      value: stats.rejected_documents,
      icon: <CloseCircleOutlined />,
      accent: "#f43f5e",
    },
  ];

  const docSummary = [
    { label: "Approved", value: stats.approved_documents, color: "#22c55e" },
    { label: "Pending", value: stats.pending_document_reviews, color: "#f59e0b" },
    { label: "Rejected", value: stats.rejected_documents, color: "#ef4444" },
  ];

  return (
    <div>
      <div
        style={{
          borderRadius: 18,
          padding: "28px 32px",
          position: "relative",
          overflow: "hidden",
          marginBottom: 20,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: 24,
          flexWrap: "wrap",
          background: HERO_GRADIENT,
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              "radial-gradient(circle at 82% 12%, rgba(255,255,255,0.18), transparent 42%)",
          }}
        />
        <div style={{ position: "relative", color: "#fff", flex: "1 1 340px", minWidth: 0 }}>
          <Typography.Title
            level={2}
            style={{ color: "#fff", margin: 0 }}
          >
            {timeGreeting}, {firstName}!
          </Typography.Title>
        </div>
        <div style={{ position: "relative", flex: "0 0 auto" }}>
          <WelcomeIllustration width={210} />
        </div>
      </div>

      <Row gutter={[16, 16]}>
        {statCards.map((card) => (
          <Col xs={24} sm={12} xl={8} xxl={6} key={card.title}>
            <Card
              className="card-lift"
              style={{
                borderRadius: 14,
                boxShadow: "0 1px 3px rgba(16,24,40,0.06)",
                height: "100%",
                background: colorBgContainer,
              }}
              styles={{ body: { padding: 20 } }}
            >
              <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
                <div
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: 12,
                    background: `${card.accent}1f`,
                    color: card.accent,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: 22,
                    flexShrink: 0,
                  }}
                >
                  {card.icon}
                </div>
                <div style={{ minWidth: 0 }}>
                  <Typography.Text
                    type="secondary"
                    style={{ display: "block", fontSize: 13, lineHeight: 1.3 }}
                  >
                    {card.title}
                  </Typography.Text>
                  <Typography.Title level={3} style={{ margin: 0, lineHeight: 1.2 }}>
                    {card.value}
                  </Typography.Title>
                </div>
              </div>
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]} style={{ marginTop: 16 }}>
        <Col xs={24} lg={12}>
          <Card
            className="card-lift"
            style={{ borderRadius: 14, boxShadow: "0 1px 3px rgba(16,24,40,0.06)", height: "100%" }}
            styles={{ body: { padding: 22 } }}
          >
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6, flexWrap: "wrap", gap: 8 }}>
              <Typography.Title level={5} style={{ margin: 0 }}>
                Task Completion
              </Typography.Title>
              <Tag color="purple" style={{ borderRadius: 999 }}>
                {progress}%
              </Tag>
            </div>
            <Progress
              percent={progress}
              strokeColor={{ "0%": "#a855f7", "100%": "#6a15e8" }}
              status={progress === 100 ? "success" : undefined}
              style={{ marginBottom: 18 }}
            />
            <Row gutter={16}>
              <Col xs={12}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#10b981" }} />
                  <div>
                    <Typography.Text type="secondary" style={{ display: "block", fontSize: 12 }}>
                      Completed
                    </Typography.Text>
                    <Typography.Text strong style={{ fontSize: 16 }}>
                      {stats.completed_tasks}
                    </Typography.Text>
                  </div>
                </div>
              </Col>
              <Col xs={12}>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <div style={{ width: 8, height: 8, borderRadius: "50%", background: "#f59e0b" }} />
                  <div>
                    <Typography.Text type="secondary" style={{ display: "block", fontSize: 12 }}>
                      Pending
                    </Typography.Text>
                    <Typography.Text strong style={{ fontSize: 16 }}>
                      {stats.pending_tasks}
                    </Typography.Text>
                  </div>
                </div>
              </Col>
            </Row>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card
            className="card-lift"
            style={{ borderRadius: 14, boxShadow: "0 1px 3px rgba(16,24,40,0.06)", height: "100%" }}
            styles={{ body: { padding: 22 } }}
          >
            <Typography.Title level={5} style={{ margin: 0, marginBottom: 16 }}>
              Documents Overview
            </Typography.Title>
            <Row gutter={[16, 16]}>
              {docSummary.map((d) => (
                <Col xs={8} key={d.label}>
                  <div
                    style={{
                      borderRadius: 12,
                      padding: "14px 8px",
                      textAlign: "center",
                      background: `${d.color}14`,
                    }}
                  >
                    <Typography.Title level={3} style={{ margin: 0, color: d.color }}>
                      {d.value}
                    </Typography.Title>
                    <Typography.Text type="secondary" style={{ fontSize: 12 }}>
                      {d.label}
                    </Typography.Text>
                  </div>
                </Col>
              ))}
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
}
