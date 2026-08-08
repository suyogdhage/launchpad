import { Card, Form, Input, Select, Button, message, Space } from "antd";
import { UserAddOutlined } from "@ant-design/icons";
import { useRegister } from "../hooks/useAuth";
import { PageHeader } from "../components/shared/PageHeader";
import type { CreateUser } from "../types/api";

export default function RegisterPage() {
  const registerMutation = useRegister();
  const [form] = Form.useForm();

  const handleRegister = (values: CreateUser) => {
    registerMutation.mutate(
      { ...values, role_name: values.role_name || "new_hire" },
      {
        onSuccess: () => {
          message.success("User registered successfully");
          form.resetFields();
        },
        onError: (err: any) => {
          message.error(err.response?.data?.detail || "Failed to register user");
        },
      }
    );
  };

  return (
    <div style={{ maxWidth: 560 }}>
      <PageHeader
        title={
          <>
            <UserAddOutlined className="brand-text" /> Register User
          </>
        }
        subtitle="Create a new user account"
      />
      <Card>
        <Form form={form} layout="vertical" onFinish={handleRegister}>
          <Form.Item
            name="name"
            label="Full Name"
            rules={[{ required: true, message: "Name is required" }]}
          >
            <Input placeholder="e.g. Jane Doe" />
          </Form.Item>
          <Form.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: "Email is required" },
              { type: "email", message: "Invalid email" },
            ]}
          >
            <Input placeholder="name@company.com" />
          </Form.Item>
          <Form.Item
            name="password"
            label="Temporary Password"
            rules={[
              { required: true, message: "Password is required" },
              { min: 6, message: "Min 6 characters" },
              { max: 20, message: "Max 20 characters" },
            ]}
          >
            <Input.Password placeholder="Minimum 6 characters" />
          </Form.Item>
          <Form.Item name="role_name" label="Role">
            <Select
              defaultValue="new_hire"
              options={[
                { label: "New Hire", value: "new_hire" },
                { label: "HR", value: "hr" },
                { label: "Manager", value: "manager" },
              ]}
            />
          </Form.Item>
          <Form.Item style={{ marginBottom: 0 }}>
            <Space>
              <Button
                type="primary"
                htmlType="submit"
                loading={registerMutation.isPending}
              >
                Register User
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
