import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { Task } from '../../models/task.model';
import { TaskService } from '../../services/task.service';

@Component({
  selector: 'app-day-view',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './day-view.component.html',
  styleUrl: './day-view.component.css',
})
export class DayViewComponent implements OnInit {
  readonly todayDate = formatLocalDate(new Date());

  todayTasks: Task[] = [];
  futureTasks: Task[] = [];
  newTitle = '';
  newTaskDate = this.todayDate;
  loading = false;
  saving = false;
  errorMessage = '';

  constructor(private readonly taskService: TaskService) {}

  ngOnInit(): void {
    this.loadTasks();
  }

  get formattedToday(): string {
    return formatDisplayDate(this.todayDate);
  }

  get futureGroups(): { date: string; label: string; tasks: Task[] }[] {
    const groups = new Map<string, Task[]>();
    for (const task of this.futureTasks) {
      const existing = groups.get(task.task_date) ?? [];
      existing.push(task);
      groups.set(task.task_date, existing);
    }
    return Array.from(groups.entries()).map(([date, tasks]) => ({
      date,
      label: formatDisplayDate(date),
      tasks,
    }));
  }

  loadTasks(): void {
    this.loading = true;
    this.errorMessage = '';
    this.taskService.listGrouped(this.todayDate).subscribe({
      next: (grouped) => {
        this.todayTasks = grouped.today;
        this.futureTasks = grouped.future;
        this.loading = false;
      },
      error: () => {
        this.errorMessage =
          'Could not load tasks. Is the API running on http://localhost:8000?';
        this.loading = false;
      },
    });
  }

  addTask(): void {
    const title = this.newTitle.trim();
    if (!title) {
      return;
    }

    this.saving = true;
    this.errorMessage = '';
    const payload = {
      title,
      task_date: this.newTaskDate,
    };

    this.taskService.create(payload).subscribe({
      next: () => {
        this.newTitle = '';
        this.newTaskDate = this.todayDate;
        this.saving = false;
        this.loadTasks();
      },
      error: () => {
        this.errorMessage = 'Could not create the task.';
        this.saving = false;
      },
    });
  }

  removeTask(task: Task): void {
    this.taskService.delete(task.id).subscribe({
      next: () => this.loadTasks(),
      error: () => {
        this.errorMessage = 'Could not delete the task.';
      },
    });
  }
}

export function formatLocalDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function formatDisplayDate(isoDate: string): string {
  const [year, month, day] = isoDate.split('-').map(Number);
  const date = new Date(year, month - 1, day);
  return date.toLocaleDateString(undefined, {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
