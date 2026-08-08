import {
  Table,
  Tag,
  Button,
  message,
  Space,
} from "antd";
import { CheckOutlined, CloseOutlined, UnorderedListOutlined } from "@ant-design/icons";
import {
  useGetAllRequests,
  useApproveRequest,
  useRejectRequest,
} from "../hooks/useRequests";
import { PageHeader } from "../components/shared/PageHeader";
import { EmptyStateIllustration } from "../components/illustrations/EmptyStateIllustration";
import dayjs from "dayjs";

export default function AllRequestsPage() {
  const { data: requests, isLoading } = useGetAllRequests();
  const approveMutation = useApproveRequest();
  const rejectMutation = useRejectRequest();

  const handleApprove = (id: string) => {
    approveMutation.mutate(id, {
      onSuccess: () => message.success("Request approved"),
      onError: (err: any) =>
        message.error(err.response?.data?.detail || "Failed to approve"),
    });
  };

  const handleReject = (id: string) => {
    rejectMutation.mutate(id, {
      onSuccess: () => message.success("Request rejected"),
      onError: (err: any) =>
        message.error(err.response?.data?.detail || "Failed to reject"),
    });
  };

  const columns = [
    { title: "Description", dataIndex: "description", key: "description" },
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
    {
      title: "Action",
      key: "action",
      render: (_: any, record: any) =>
        record.status === "pending" ? (
          <Space>
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
              onClick={() => handleReject(record.id)}
              loading={rejectMutation.isPending}
            >
              Reject
            </Button>
          </Space>
        ) : null,
    },
  ];

  return (
    <div>
      <PageHeader
        title={
          <>
            <UnorderedListOutlined className="brand-text" /> All Requests
          </>
        }
        subtitle="Approve or reject requests from your team"
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
              <div>No requests submitted yet</div>
            </div>
          ),
        }}
      />
    </div>
  );
}
