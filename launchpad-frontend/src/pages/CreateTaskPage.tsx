import { Card, Form, Input, DatePicker, Select, Button, message } from "antd";
import { useNavigate } from "react-router-dom";
import { useCreateTask } from "../hooks/useTasks";
import { useGetUsers } from "../hooks/useUsers";
import { useAuth } from "../context/AuthContext";
import { PageHeader } from "../components/shared/PageHeader";
import { EditOutlined } from "@ant-design/icons";
import dayjs from "dayjs";

export default function CreateTaskPage() {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const { user } = useAuth();
  const createTaskMutation = useCreateTask();
  const { data: users } = useGetUsers();

  const isHrOrSuperadmin = user?.role === "hr" || user?.role === "superadmin";

  const assignableUsers = isHrOrSuperadmin
    ? users || []
    : users?.filter((u) => u.assigned_to === user?.id) || [];

  const onFinish = (values: {
    title: string;
    description?: string;
    assigned_to: string;
    deadline?: dayjs.Dayjs;
  }) => {
    const payload = {
      title: values.title,
      description: values.description,
      assigned_to: values.assigned_to,
      deadline: values.deadline?.format("YYYY-MM-DD"),
    };
    createTaskMutation.mutate(payload, {
      onSuccess: () => {
        message.success("Task created");
        navigate("/tasks");
      },
      onError: (err: any) => {
        console.error("Task creation error:", err.response?.data);
        message.error(err.response?.data?.detail || "Failed to create task");
      },
    });
  };

  return (
    <div style={{ maxWidth: 600 }}>
      <PageHeader
        title={
          <>
            <EditOutlined className="brand-text" /> Create Task
          </>
        }
        subtitle="Assign an onboarding task to a team member"
      />
      <Card style={{ borderRadius: 14, boxShadow: "0 1px 3px rgba(16,24,40,0.06)" }}>
        <Form form={form} layout="vertical" onFinish={onFinish}>
          <Form.Item
            name="title"
            label="Title"
            rules={[{ required: true, message: "Required" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item name="description" label="Description">
            <Input.TextArea rows={4} />
          </Form.Item>
          <Form.Item
            name="assigned_to"
            label="Assign To"
            rules={[{ required: true, message: "Required" }]}
          >
            <Select
              showSearch
              placeholder="Select user"
              filterOption={(input, option) =>
                (option?.label ?? "")
                  .toLowerCase()
                  .includes(input.toLowerCase())
              }
              options={assignableUsers.map((u) => ({
                label: `${u.name} (${u.email}) [${u.role_name}]`,
                value: u.id,
              }))}
            />
          </Form.Item>
          <Form.Item name="deadline" label="Deadline">
            <DatePicker
              style={{ width: "100%" }}
              disabledDate={(current) => current && current < dayjs().startOf("day")}
            />
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              loading={createTaskMutation.isPending}
            >
              Create Task
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
}
