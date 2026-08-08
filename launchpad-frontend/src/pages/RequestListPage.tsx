import { useState } from "react";
import {
  Table,
  Button,
  Modal,
  Input,
  Tag,
  message,
} from "antd";
import { PlusOutlined, QuestionCircleOutlined } from "@ant-design/icons";
import { useCreateRequest, useGetMyRequests } from "../hooks/useRequests";
import { PageHeader } from "../components/shared/PageHeader";
import { EmptyStateIllustration } from "../components/illustrations/EmptyStateIllustration";
import dayjs from "dayjs";

export default function RequestListPage() {
  const { data: requests, isLoading } = useGetMyRequests();
  const createMutation = useCreateRequest();
  const [modalOpen, setModalOpen] = useState(false);
  const [description, setDescription] = useState("");

  const handleCreate = () => {
    if (!description.trim()) {
      message.warning("Description is required");
      return;
    }
    createMutation.mutate(
      { description },
      {
        onSuccess: () => {
          message.success("Request created");
          setModalOpen(false);
          setDescription("");
        },
        onError: (err: any) =>
          message.error(err.response?.data?.detail || "Failed to create"),
      }
    );
  };

  const columns = [
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (status: string) => (
        <Tag
          color={
            status === "approved"
              ? "green"
              : status === "rejected"
              ? "red"
              : "orange"
          }
        >
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: "Created At",
      dataIndex: "created_at",
      key: "created_at",
      render: (date: string) => dayjs(date).format("YYYY-MM-DD HH:mm"),
    },
  ];

  return (
    <div>
      <PageHeader
        title={
          <>
            <QuestionCircleOutlined className="brand-text" /> My Requests
          </>
        }
        subtitle="Submit and track your support requests"
        actions={
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={() => setModalOpen(true)}
          >
            New Request
          </Button>
        }
      />

      <Table
        dataSource={requests}
        columns={columns}
        rowKey="id"
        loading={isLoading}
        locale={{
          emptyText: (
            <div style={{ padding: 24 }}>
              <EmptyStateIllustration />
              <div>No requests yet — create your first one</div>
            </div>
          ),
        }}
      />

      <Modal
        title="New Request"
        open={modalOpen}
        onCancel={() => {
          setModalOpen(false);
          setDescription("");
        }}
        onOk={handleCreate}
        confirmLoading={createMutation.isPending}
      >
        <Input.TextArea
          placeholder="Describe your request..."
          rows={4}
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </Modal>
    </div>
  );
}
