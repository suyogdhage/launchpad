import { Table, Tag, Typography, Button, Empty, message } from "antd";
import { DownloadOutlined, ProfileOutlined } from "@ant-design/icons";
import { useGetAssignedByMe } from "../hooks/useTasks";
import { downloadDocument } from "../hooks/useDocuments";
import { PageHeader } from "../components/shared/PageHeader";
import { EmptyStateIllustration } from "../components/illustrations/EmptyStateIllustration";
import dayjs from "dayjs";

export default function AssignedTasksPage() {
  const { data: tasks, isLoading } = useGetAssignedByMe();

  const columns = [
    {
      title: "Task",
      dataIndex: "title",
      key: "title",
      render: (title: string, record: any) => (
        <div>
          <Typography.Text strong>{title}</Typography.Text>
          <Typography.Paragraph
            type="secondary"
            ellipsis={{ rows: 1 }}
            style={{ marginBottom: 0, fontSize: 13 }}
          >
            {record.description || "-"}
          </Typography.Paragraph>
        </div>
      ),
    },
    {
      title: "Assigned To",
      dataIndex: "assignee_name",
      key: "assignee_name",
      render: (name: string | null) => name || "-",
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (status: string) => (
        <Tag
          color={status === "completed" ? "green" : "orange"}
          style={{ borderRadius: 999 }}
        >
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: "Deadline",
      dataIndex: "deadline",
      key: "deadline",
      render: (date: string | undefined) =>
        date ? dayjs(date).format("YYYY-MM-DD") : "-",
    },
    {
      title: "Documents",
      dataIndex: "documents",
      key: "documents",
      render: (docs: any[]) => {
        if (!docs || docs.length === 0) return "-";
        return (
          <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
            {docs.map((doc) => (
              <div key={doc.id} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <Tag
                  color={
                    doc.status === "approved"
                      ? "green"
                      : doc.status === "rejected"
                      ? "red"
                      : "orange"
                  }
                  style={{ marginInlineEnd: 0 }}
                >
                  {doc.status.toUpperCase()}
                </Tag>
                <Button
                  type="link"
                  size="small"
                  icon={<DownloadOutlined />}
                  style={{ padding: 0 }}
                  onClick={() =>
                    downloadDocument(doc.id, doc.file_path.split("/").pop()).catch(() =>
                      message.error("Failed to download file")
                    )
                  }
                >
                  {doc.file_path.split("/").pop()}
                </Button>
                {doc.rejection_reason && (
                  <Typography.Text type="danger" style={{ fontSize: 12 }}>
                    ({doc.rejection_reason})
                  </Typography.Text>
                )}
              </div>
            ))}
          </div>
        );
      },
    },
    {
      title: "Created At",
      dataIndex: "created_at",
      key: "created_at",
      render: (date: string) =>
        date ? dayjs(date).format("YYYY-MM-DD HH:mm") : "-",
    },
  ];

  return (
    <div>
      <PageHeader
        title={
          <>
            <ProfileOutlined className="brand-text" /> Assigned by Me
          </>
        }
        subtitle="Track the status and submitted documents of tasks you assigned"
      />
      <Table
        dataSource={tasks || []}
        columns={columns}
        rowKey="id"
        loading={isLoading}
        locale={{
          emptyText: (
            <div style={{ padding: 24 }}>
              <EmptyStateIllustration />
              <Empty image={null} description="No tasks assigned yet" />
            </div>
          ),
        }}
      />
    </div>
  );
}
