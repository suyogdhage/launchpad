import { Table, Tag, Button, message, Tabs, Empty, Typography } from "antd";
import { CheckCircleOutlined, CheckSquareOutlined } from "@ant-design/icons";
import { useGetMyTasks, useCompleteTask } from "../hooks/useTasks";
import { PageHeader } from "../components/shared/PageHeader";
import { EmptyStateIllustration } from "../components/illustrations/EmptyStateIllustration";
import { useState } from "react";
import dayjs from "dayjs";

export default function TaskListPage() {
  const { data: tasks, isLoading } = useGetMyTasks();
  const completeMutation = useCompleteTask();
  const [statusFilter, setStatusFilter] = useState("all");

  const handleComplete = (taskId: string) => {
    completeMutation.mutate(taskId, {
      onSuccess: () => message.success("Task completed!"),
      onError: (err: any) =>
        message.error(err.response?.data?.detail || "Failed to complete"),
    });
  };

  const filteredTasks = (tasks || []).filter(
    (t: any) => statusFilter === "all" || t.status === statusFilter
  );

  const pendingCount = (tasks || []).filter((t: any) => t.status === "pending").length;
  const completedCount = (tasks || []).filter((t: any) => t.status === "completed").length;

  const columns = [
    {
      title: "Title",
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
      title: "Completed At",
      dataIndex: "completed_at",
      key: "completed_at",
      render: (date: string | undefined) =>
        date ? dayjs(date).format("YYYY-MM-DD HH:mm") : "-",
    },
    {
      title: "Action",
      key: "action",
      render: (_: any, record: any) =>
        record.status === "pending" ? (
          <Button
            type="link"
            icon={<CheckCircleOutlined />}
            onClick={() => handleComplete(record.id)}
            loading={completeMutation.isPending}
          >
            Complete
          </Button>
        ) : null,
    },
  ];

  return (
    <div>
      <PageHeader
        title={
          <>
            <CheckSquareOutlined className="brand-text" /> My Tasks
          </>
        }
        subtitle="Track and complete your onboarding checklist"
      />
      <Tabs
        activeKey={statusFilter}
        onChange={setStatusFilter}
        items={[
          { key: "all", label: `All (${(tasks || []).length})` },
          { key: "pending", label: `Pending (${pendingCount})` },
          { key: "completed", label: `Completed (${completedCount})` },
        ]}
        style={{ marginBottom: 8 }}
      />
      <Table
        dataSource={filteredTasks}
        columns={columns}
        rowKey="id"
        loading={isLoading}
        locale={{
          emptyText: (
            <div style={{ padding: 24 }}>
              <EmptyStateIllustration />
              <Empty
                image={null}
                description={statusFilter === "all" ? "No tasks assigned yet" : "No tasks in this state"}
              />
            </div>
          ),
        }}
      />
    </div>
  );
}
