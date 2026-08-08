import { Card, Descriptions, Tag, Spin, Typography, Avatar } from "antd";
import { UserOutlined } from "@ant-design/icons";
import { useAuth } from "../context/AuthContext";
import { useMe } from "../hooks/useUsers";
import { PageHeader } from "../components/shared/PageHeader";

const ROLE_COLORS: Record<string, string> = {
  superadmin: "red",
  hr: "blue",
  manager: "purple",
  new_hire: "green",
};

export default function ProfilePage() {
  const { user } = useAuth();
  const { data: profile, isLoading } = useMe();

  if (isLoading) return <Spin size="large" style={{ display: "block", margin: "100px auto" }} />;

  const role = user?.role || "new_hire";

  return (
    <div style={{ maxWidth: 600 }}>
      <PageHeader
        title={
          <>
            <UserOutlined className="brand-text" /> My Profile
          </>
        }
        subtitle="Your account details"
      />
      <Card style={{ borderRadius: 14, boxShadow: "0 1px 3px rgba(16,24,40,0.06)" }}>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 16,
            marginBottom: 24,
            paddingBottom: 20,
            borderBottom: "1px solid #f0f0f0",
          }}
        >
          <Avatar
            size={72}
            icon={<UserOutlined />}
            style={{ background: "linear-gradient(135deg, #a855f7, #6a15e8)", fontSize: 30 }}
          />
          <div>
            <Typography.Title level={4} style={{ margin: 0, marginBottom: 4 }}>
              {profile?.name || user?.id}
            </Typography.Title>
            <Typography.Text type="secondary">{profile?.email || "-"}</Typography.Text>
          </div>
        </div>
        <Descriptions column={1} bordered>
          <Descriptions.Item label="ID">{profile?.id || user?.id}</Descriptions.Item>
          <Descriptions.Item label="Name">{profile?.name}</Descriptions.Item>
          <Descriptions.Item label="Email">{profile?.email}</Descriptions.Item>
          <Descriptions.Item label="Role">
            <Tag color={ROLE_COLORS[role]} style={{ borderRadius: 999 }}>
              {role}
            </Tag>
          </Descriptions.Item>
        </Descriptions>
      </Card>
    </div>
  );
}
