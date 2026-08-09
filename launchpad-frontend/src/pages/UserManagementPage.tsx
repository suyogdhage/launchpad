import { useState } from "react";
import {
  Table,
  Button,
  Modal,
  Form,
  Input,
  Select,
  message,
  Tag,
  Typography,
  Space,
} from "antd";
import { PlusOutlined, SwapOutlined, TeamOutlined, DeleteOutlined } from "@ant-design/icons";
import { useGetUsers, useAssignManager, useDeleteUser } from "../hooks/useUsers";
import { useRegister } from "../hooks/useAuth";
import { useAuth } from "../context/AuthContext";
import { PageHeader } from "../components/shared/PageHeader";
import type { User } from "../types/api";


export default function UserManagementPage() {
  const { data: users, isLoading } = useGetUsers();
  const registerMutation = useRegister();
  const assignMutation = useAssignManager();
  const deleteMutation = useDeleteUser();
  const { user: currentUser } = useAuth();
  const [createModalOpen, setCreateModalOpen] = useState(false);
  const [assignModalOpen, setAssignModalOpen] = useState(false);
  const [createForm] = Form.useForm();
  const [assignForm] = Form.useForm();

  const isSuperadmin = currentUser?.role === "superadmin";

  const handleCreate = (values: {
    email: string;
    name: string;
    password: string;
    role_name?: string;
  }) => {
    registerMutation.mutate({ ...values, role_name: values.role_name || "new_hire" }, {
      onSuccess: () => {
        message.success("User created");
        setCreateModalOpen(false);
        createForm.resetFields();
      },
      onError: (err: any) => {
        message.error(err.response?.data?.detail || "Failed to create user");
      },
    });
  };

  const handleAssign = (values: { user_id: string; manager_id: string }) => {
    assignMutation.mutate(values, {
      onSuccess: () => {
        message.success("Manager assigned");
        setAssignModalOpen(false);
        assignForm.resetFields();
      },
      onError: (err: any) => {
        message.error(err.response?.data?.detail || "Failed to assign");
      },
    });
  };

  const handleDelete = (record: User) => {
    Modal.confirm({
      title: `Delete ${record.name}?`,
      content:
        "This permanently removes the user along with their tasks, documents, notifications, requests, and chat history. This cannot be undone.",
      okText: "Delete",
      okType: "danger",
      cancelText: "Cancel",
      onOk: () =>
        deleteMutation.mutate(record.id, {
          onSuccess: () => message.success("User deleted"),
          onError: (err: any) =>
            message.error(err.response?.data?.detail || "Failed to delete user"),
        }),
    });
  };

  const managers = users?.filter((u) => u.role_name === "manager") || [];
  const nonManagers = users?.filter((u) => u.role_name !== "manager") || [];

  const columns = [
    { title: "Name", dataIndex: "name", key: "name" },
    { title: "Email", dataIndex: "email", key: "email" },
    {
      title: "Role",
      dataIndex: "role_name",
      key: "role_name",
      render: (role: string) => (
        <Tag
          color={
            role === "superadmin"
              ? "red"
              : role === "hr"
              ? "blue"
              : role === "manager"
              ? "purple"
              : "green"
          }
        >
          {role}
        </Tag>
      ),
    },
    {
      title: "Assigned To",
      dataIndex: "assigned_to",
      key: "assigned_to",
      render: (val: string | undefined) =>
        val ? (
          <Typography.Text copyable={{ text: val }}>
            {users?.find((u) => u.id === val)?.name || val?.slice(0, 8) + "..."}
          </Typography.Text>
        ) : (
          <Tag>Unassigned</Tag>
        ),
    },
    ...(isSuperadmin
      ? [
          {
            title: "Actions",
            key: "actions",
            render: (_: unknown, record: User) => {
              const isSelf = record.id === currentUser?.id;
              return (
                <Space>
                  <Button
                    danger
                    size="small"
                    icon={<DeleteOutlined />}
                    disabled={isSelf}
                    title={isSelf ? "You cannot delete your own account" : "Delete user"}
                    onClick={() => handleDelete(record)}
                  >
                    Delete
                  </Button>
                </Space>
              );
            },
          },
        ]
      : []),
  ];

  return (
    <div>
      <PageHeader
        title={
          <>
            <TeamOutlined className="brand-text" /> User Management
          </>
        }
        subtitle="Manage users and manager assignments"
        actions={
          <Space>
            <Button
              icon={<SwapOutlined />}
              onClick={() => setAssignModalOpen(true)}
            >
              Assign Manager
            </Button>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => setCreateModalOpen(true)}
            >
              Create User
            </Button>
          </Space>
        }
      />

      <Table
        dataSource={users}
        columns={columns}
        rowKey="id"
        loading={isLoading}
      />

      <Modal
        title="Create User"
        open={createModalOpen}
        onCancel={() => setCreateModalOpen(false)}
        footer={null}
      >
        <Form form={createForm} layout="vertical" onFinish={handleCreate}>
          <Form.Item
            name="name"
            label="Name"
            rules={[{ required: true, message: "Required" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: "Required" },
              { type: "email", message: "Invalid email" },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="password"
            label="Password"
            rules={[
              { required: true, message: "Required" },
              { min: 6, message: "Min 6 characters" },
              { max: 20, message: "Max 20 characters" },
            ]}
          >
            <Input.Password />
          </Form.Item>
          <Form.Item name="role_name" label="Role">
            <Select
              options={[
                { label: "New Hire", value: "new_hire" },
                { label: "HR", value: "hr" },
                { label: "Manager", value: "manager" },
              ]}
            />
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={registerMutation.isPending}
            >
              Create
            </Button>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="Assign Manager"
        open={assignModalOpen}
        onCancel={() => setAssignModalOpen(false)}
        footer={null}
      >
        <Form form={assignForm} layout="vertical" onFinish={handleAssign}>
          <Form.Item
            name="user_id"
            label="User"
            rules={[{ required: true, message: "Select user" }]}
          >
            <Select
              showSearch
              placeholder="Select user"
              filterOption={(input, option) =>
                (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
              }
              options={nonManagers.map((u) => ({
                label: `${u.name} (${u.email})`,
                value: u.id,
              }))}
            />
          </Form.Item>
          <Form.Item
            name="manager_id"
            label="Manager"
            rules={[{ required: true, message: "Select manager" }]}
          >
            <Select
              showSearch
              placeholder="Select manager"
              filterOption={(input, option) =>
                (option?.label ?? "").toLowerCase().includes(input.toLowerCase())
              }
              options={managers.map((u) => ({
                label: `${u.name} (${u.email})`,
                value: u.id,
              }))}
            />
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={assignMutation.isPending}
            >
              Assign
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
}
