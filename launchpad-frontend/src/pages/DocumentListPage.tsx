import { useState } from "react";
import {
  Table,
  Button,
  Modal,
  Select,
  Upload,
  Tag,
  message,
} from "antd";
import { UploadOutlined, FileOutlined, DownloadOutlined } from "@ant-design/icons";
import { useUploadDocument, useGetMyDocuments, downloadDocument } from "../hooks/useDocuments";
import { useGetMyTasks } from "../hooks/useTasks";
import { PageHeader } from "../components/shared/PageHeader";
import { EmptyStateIllustration } from "../components/illustrations/EmptyStateIllustration";
import dayjs from "dayjs";

export default function DocumentListPage() {
  const [uploadModalOpen, setUploadModalOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState<string | undefined>();
  const [selectedFile, setSelectedFile] = useState<File | undefined>();
  const { data: tasks } = useGetMyTasks();
  const { data: myDocs, isLoading: docsLoading } = useGetMyDocuments();
  const uploadMutation = useUploadDocument();

  const handleUpload = () => {
    if (!selectedTask || !selectedFile) {
      message.warning("Select a task and a file");
      return;
    }
    uploadMutation.mutate(
      { task_id: selectedTask, file: selectedFile },
      {
        onSuccess: () => {
          message.success("Document uploaded");
          setUploadModalOpen(false);
          setSelectedTask(undefined);
          setSelectedFile(undefined);
        },
        onError: (err: any) =>
          message.error(err.response?.data?.detail || "Upload failed"),
      }
    );
  };

  const docs = (myDocs as any[] | undefined) || [];

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
      title: "Rejection Reason",
      dataIndex: "rejection_reason",
      key: "rejection_reason",
      render: (reason: string | null) => reason || "-",
    },
    {
      title: "Uploaded At",
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
            <FileOutlined className="brand-text" /> My Documents
          </>
        }
        subtitle="Upload files for your tasks and review their status"
        actions={
          <Button
            type="primary"
            icon={<UploadOutlined />}
            onClick={() => setUploadModalOpen(true)}
          >
            Upload Document
          </Button>
        }
      />

      <Table
        dataSource={docs || []}
        columns={columns}
        rowKey="id"
        loading={docsLoading}
        locale={{
          emptyText: (
            <div style={{ padding: 24 }}>
              <EmptyStateIllustration />
              <div>No documents uploaded yet</div>
            </div>
          ),
        }}
      />

      <Modal
        title="Upload Document"
        open={uploadModalOpen}
        onCancel={() => setUploadModalOpen(false)}
        onOk={handleUpload}
        confirmLoading={uploadMutation.isPending}
      >
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <Select
            placeholder="Select task"
            style={{ width: "100%" }}
            value={selectedTask}
            onChange={setSelectedTask}
            options={(tasks || [])
              .filter((t: any) => t.status === "pending")
              .map((t: any) => ({
                label: t.title,
                value: t.id,
              }))}
          />
          <Upload
            beforeUpload={(file) => {
              setSelectedFile(file);
              return false;
            }}
            onRemove={() => setSelectedFile(undefined)}
            fileList={
              selectedFile
                ? [
                    {
                      uid: "-1",
                      name: selectedFile.name,
                      status: "done",
                    },
                  ]
                : []
            }
          >
            <Button icon={<UploadOutlined />}>Select File</Button>
          </Upload>
          <div style={{ fontSize: 12, color: "rgba(0,0,0,0.45)" }}>
            Max 10 MB per file (pdf, docx, doc, txt, png, jpg, jpeg)
          </div>
        </div>
      </Modal>
    </div>
  );
}
