import {
  Layout,
  Menu,
  Button,
  Typography,
  theme,
  Breadcrumb,
  Avatar,
  Tooltip,
  Badge,
  Dropdown,
  Empty,
  Tag,
} from "antd";
import {
  DashboardOutlined,
  TeamOutlined,
  UserAddOutlined,
  CheckSquareOutlined,
  EditOutlined,
  FileOutlined,
  FileSearchOutlined,
  QuestionCircleOutlined,
  UnorderedListOutlined,
  RobotOutlined,
  LogoutOutlined,
  SunOutlined,
  MoonOutlined,
  BellOutlined,
  ProfileOutlined,
} from "@ant-design/icons";
import { Outlet, useNavigate, useLocation, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { useMe } from "../../hooks/useUsers";
import { useTheme } from "../../context/ThemeContext";
import {
  useGetNotifications,
  useGetUnreadCount,
  useMarkNotificationRead,
  useMarkAllNotificationsRead,
} from "../../hooks/useNotifications";
import dayjs from "dayjs";
import logo from "../../assets/logo-text-cropped.png";
import type { ItemType } from "antd/es/menu/interface";

const { Header, Sider, Content } = Layout;

function initials(name?: string) {
  if (!name) return "U";
  return name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0]?.toUpperCase())
    .join("");
}

function displayRole(role: string) {
  return role.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

const ROUTE_LABELS: Record<string, string> = {
  "/dashboard": "Dashboard",
  "/users": "User Management",
  "/register": "Register User",
  "/tasks": "My Tasks",
  "/tasks/create": "Create Task",
  "/tasks/assigned-by-me": "Assigned by Me",
  "/documents": "My Documents",
  "/documents/pending": "Pending Reviews",
  "/requests": "My Requests",
  "/requests/all": "All Requests",
  "/buddy": "Onboarding Buddy",
  "/profile": "My Profile",
};

export function AppLayout() {
  const { user, logout } = useAuth();
  const { data: me } = useMe();
  const { isDark, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const { data: notifications = [] } = useGetNotifications();
  const { data: unreadCount = 0 } = useGetUnreadCount();
  const markReadMutation = useMarkNotificationRead();
  const markAllReadMutation = useMarkAllNotificationsRead();
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  const role = user?.role || "new_hire";
  const isPrivileged = role === "hr" || role === "superadmin";
  const isManager = role === "manager" || role === "superadmin" || role === "hr";

  const menuItems: ItemType[] = [
    ...(isPrivileged
      ? [
          {
            type: "group",
            label: "Overview",
            children: [
              { key: "/dashboard", icon: <DashboardOutlined />, label: "Dashboard" },
              { key: "/users", icon: <TeamOutlined />, label: "Users" },
              ...(role === "hr"
                ? [{ key: "/register", icon: <UserAddOutlined />, label: "Register User" }]
                : []),
            ],
          } as ItemType,
        ]
      : []),
    {
      type: "group",
      label: "Tasks",
      children: [
        { key: "/tasks", icon: <CheckSquareOutlined />, label: "My Tasks" },
        ...(isManager
          ? [{ key: "/tasks/assigned-by-me", icon: <ProfileOutlined />, label: "Assigned by Me" }]
          : []),
        ...(isManager
          ? [{ key: "/tasks/create", icon: <EditOutlined />, label: "Create Task" }]
          : []),
      ],
    },
    {
      type: "group",
      label: "Documents",
      children: [
        { key: "/documents", icon: <FileOutlined />, label: "My Documents" },
        ...(isPrivileged
          ? [
              {
                key: "/documents/pending",
                icon: <FileSearchOutlined />,
                label: "Pending Reviews",
              },
            ]
          : []),
      ],
    },
    {
      type: "group",
      label: "Requests",
      children: [
        { key: "/requests", icon: <QuestionCircleOutlined />, label: "My Requests" },
        ...(isManager
          ? [
              {
                key: "/requests/all",
                icon: <UnorderedListOutlined />,
                label: "All Requests",
              },
            ]
          : []),
      ],
    },
    {
      type: "group",
      label: "Support",
      children: [
        { key: "/buddy", icon: <RobotOutlined />, label: "Onboarding Buddy" },
      ],
    },
  ];

  const pathSnippets = location.pathname.split("/").filter(Boolean);
  const breadcrumbItems = [
    { title: <Link to="/">Home</Link> },
    ...pathSnippets.map((_, index) => {
      const url = `/${pathSnippets.slice(0, index + 1).join("/")}`;
      return { title: <Link to={url}>{ROUTE_LABELS[url] || pathSnippets[index]}</Link> };
    }),
  ];

  const selectedKey = menuItems
    .flatMap((g: any) => g?.children || [])
    .map((c: any) => c.key)
    .find((k: string) => k === location.pathname);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider width={240}>
        <div
          className="brand-gradient"
          style={{
            height: 64,
            display: "flex",
            alignItems: "center",
            justifyContent: "flex-start",
            gap: 10,
            padding: "0 16px",
            overflow: "hidden",
            background: "linear-gradient(180deg, #574C91 0%, #6D5DA6 100%)",
          }}
        >
          <img
            src={logo}
            alt="Launchpad"
            style={{ height: 48, objectFit: "contain", width: "100%", maxWidth: 200 }}
          />
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={selectedKey ? [selectedKey] : []}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
          style={{ borderInlineEnd: "none" }}
        />
      </Sider>
      <Layout>
        <Header
          style={{
            padding: "0 24px",
            background: colorBgContainer,
            display: "flex",
            alignItems: "center",
            justifyContent: "space-between",
            boxShadow: "0 1px 4px rgba(16,24,40,0.06)",
            position: "sticky",
            top: 0,
            zIndex: 10,
          }}
        >
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <Breadcrumb items={breadcrumbItems} />
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <Dropdown
              trigger={["click"]}
              dropdownRender={() => (
                <div
                  style={{
                    width: 360,
                    maxHeight: 420,
                    overflowY: "auto",
                    background: colorBgContainer,
                    borderRadius: 12,
                    boxShadow: "0 8px 24px rgba(16,24,40,0.18)",
                    padding: 8,
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "center",
                      padding: "8px 12px",
                    }}
                  >
                    <Typography.Text strong>Notifications</Typography.Text>
                    <Button
                      type="link"
                      size="small"
                      disabled={!notifications.length}
                      onClick={() => markAllReadMutation.mutate()}
                    >
                      Mark all read
                    </Button>
                  </div>
                  {notifications.length === 0 ? (
                    <Empty
                      image={null}
                      description="No notifications yet"
                      style={{ padding: 24 }}
                    />
                  ) : (
                    notifications.map((n) => (
                      <div
                        key={n.id}
                        onClick={() => {
                          if (!n.is_read) markReadMutation.mutate(n.id);
                          if (n.link) navigate(n.link);
                        }}
                        style={{
                          padding: "10px 12px",
                          borderRadius: 8,
                          cursor: n.link ? "pointer" : "default",
                          background: n.is_read ? "transparent" : "rgba(134,59,255,0.06)",
                        }}
                      >
                        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                          <Typography.Text strong style={{ fontSize: 13 }}>
                            {n.title}
                          </Typography.Text>
                          {!n.is_read && <Tag color="purple" style={{ marginInlineEnd: 0, fontSize: 10 }}>NEW</Tag>}
                        </div>
                        {n.message && (
                          <Typography.Text type="secondary" style={{ fontSize: 12, display: "block" }}>
                            {n.message}
                          </Typography.Text>
                        )}
                        <Typography.Text type="secondary" style={{ fontSize: 11 }}>
                          {dayjs(n.created_at).format("MMM D, HH:mm")}
                        </Typography.Text>
                      </div>
                    ))
                  )}
                </div>
              )}
            >
              <Tooltip title="Notifications">
                <Badge count={unreadCount} size="small" offset={[-2, 2]}>
                  <Button type="text" icon={<BellOutlined />} style={{ fontSize: 16 }} />
                </Badge>
              </Tooltip>
            </Dropdown>
            <Tooltip title={isDark ? "Switch to light mode" : "Switch to dark mode"}>
              <Button
                type="text"
                icon={isDark ? <SunOutlined /> : <MoonOutlined />}
                onClick={toggleTheme}
                style={{ fontSize: 16 }}
              />
            </Tooltip>
            <Tooltip title="My Profile">
              <Button
                type="text"
                onClick={() => navigate("/profile")}
                style={{ display: "flex", alignItems: "center", gap: 8, height: "auto", padding: "6px 8px" }}
              >
                <Avatar
                  size={32}
                  style={{ background: "linear-gradient(135deg, #a855f7, #6a15e8)" }}
                >
                  {initials(me?.name)}
                </Avatar>
                <div style={{ textAlign: "left", lineHeight: 1.2 }}>
                  <Typography.Text strong style={{ display: "block", fontSize: 13 }}>
                    {me?.name || user?.id?.slice(0, 8) || "User"}
                  </Typography.Text>
                  <Typography.Text type="secondary" style={{ display: "block", fontSize: 12 }}>
                    {displayRole(role)}
                  </Typography.Text>
                </div>
              </Button>
            </Tooltip>
            <Button
              type="text"
              danger
              icon={<LogoutOutlined />}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </div>
        </Header>
        <Content
          style={{
            margin: 24,
            padding: 24,
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
            minHeight: 280,
          }}
        >
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
