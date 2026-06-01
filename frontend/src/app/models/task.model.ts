export interface Task {
  id: number;
  title: string;
  task_date: string;
  created_at: string;
}

export interface TaskGrouped {
  today: Task[];
  future: Task[];
}

export interface TaskCreatePayload {
  title: string;
  task_date: string;
}

export interface TaskUpdatePayload {
  title?: string;
  task_date?: string;
}
