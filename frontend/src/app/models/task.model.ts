export interface Task {
  id: number;
  title: string;
  task_date: string;
  due_time: string | null;
  is_done: boolean;
  created_at: string;
}

export interface TaskCreatePayload {
  title: string;
  task_date: string;
  due_time: string | null;
}

export interface TaskUpdatePayload {
  is_done?: boolean;
  title?: string;
  due_time?: string | null;
}
