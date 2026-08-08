import { useState } from "react";
import {
  Table,
  Tag,
  Button,
  Modal,
  Input,
  message,
} from "antd";
import { CheckOutlined, CloseOutlined, FileSearchOutlined, DownloadOutlined } from "@ant-design/icons";
import { useApproveDocument, useRejectDocument, useGetPendingDocuments, downloadDocument } from "../hooks/useDocuments";
import { PageHeader } from "../components/shared/PageHeader";
import { EmptyStateIllustration } from "../components/illustrations/EmptyStateIllustration";
import dayjs from "dayjs";

export default function PendingReviewsPage() {
  const { data: pendingDocs, isLoading } = useGetPendingDocuments();
  const approveMutation = useApproveDocument();
  const rejectMutation = useRejectDocument();
  const [rejectModalOpen, setRejectModalOpen] = useState(false);
  const [rejectDocId, setRejectDocId] = useState<string | null>(null);
  const [rejectReason, setRejectReason] = useState("");

  const handleApprove = (docId: string) => {
    approveMutation.mutate(docId, {
      onSuccess: () => message.success("Document approved"),
      onError: (err: any) =>
        message.error(err.response?.data?.detail || "Failed to approve"),
    });
  };

  const handleReject = () => {
    if (!rejectDocId || rejectReason.length < 6) {
      message.warning("Reason must be at least 6 characters");
      return;
    }
    rejectMutation.mutate(
      { document_id: rejectDocId, reason: rejectReason },
      {
        onSuccess: () => {
          message.success("Document rejected");
          setRejectModalOpen(false);
          setRejectReason("");
          setRejectDocId(null);
        },
        onError: (err: any) =>
          message.error(err.response?.data?.detail || "Failed to reject"),
      }
    );
  };

  const columns = [
    { title: "Task", dataIndex: "task_title", key: "task_title" },
    {
      title: "File",
      dataIndex: "file_path",
      key: "file_path",
      render: (path: string, record: any) => (
        <a
          href="#"
          onClick={(e) => {
            e.preventDefault();
            downloadDocument(record.id, path.split("/").pop()).catch(() =>
              message.error("Failed to download file")
            );
          }}
        >
          <DownloadOutlined /> {path.split("/").pop()}
        </a>
      ),
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
      render: (status: string) => (
        <Tag color="orange">{status.toUpperCase()}</Tag>
      ),
    },
    {
      title: "Uploaded At",
      dataIndex: "created_at",
      key: "created_at",
      render: (date: string) => dayjs(date).format("YYYY-MM-DD HH:mm"),
    },
    {
      title: "Action",
      key: "action",
      render: (_: any, record: any) => (
        <div style={{ display: "flex", gap: 8 }}>
          <Button
            type="primary"
            size="small"
            icon={<CheckOutlined />}
            onClick={() => handleApprove(record.id)}
            loading={approveMutation.isPending}
          >
            Approve
          </Button>
          <Button
            danger
            size="small"
            icon={<CloseOutlined />}
            onClick={() => {
              setRejectDocId(record.id);
              setRejectModalOpen(true);
            }}
          >
            Reject
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div>
      <PageHeader
        title={
          <>
            <FileSearchOutlined className="brand-text" /> Pending Document Reviews
          </>
        }
        subtitle="Review documents submitted by new hires"
      />
      <Table
        dataSource={pendingDocs}
        columns={columns}
        rowKey="id"
        loading={isLoading}
        locale={{
          emptyText: (
            <div style={{ padding: 24 }}>
              <EmptyStateIllustration />
              <div>No pending reviews</div>
            </div>
          ),
        }}
      />

      <Modal
        title="Reject Document"
        open={rejectModalOpen}
        onCancel={() => {
          setRejectModalOpen(false);
          setRejectReason("");
          setRejectDocId(null);
        }}
        onOk={handleReject}
        confirmLoading={rejectMutation.isPending}
      >
        <Input.TextArea
          placeholder="Reason for rejection (min 6 characters)"
          rows={4}
          value={rejectReason}
          onChange={(e) => setRejectReason(e.target.value)}
          showCount
          maxLength={20}
        />
      </Modal>
    </div>
  );
}
