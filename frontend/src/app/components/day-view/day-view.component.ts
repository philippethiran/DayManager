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
  selectedDate = formatLocalDate(new Date());
  tasks: Task[] = [];
  newTitle = '';
  newTime = '';
  loading = false;
  saving = false;
  errorMessage = '';

  constructor(private readonly taskService: TaskService) {}

  ngOnInit(): void {
    this.loadTasks();
  }

  get formattedSelectedDate(): string {
    const [year, month, day] = this.selectedDate.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    return date.toLocaleDateString(undefined, {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  }

  shiftDay(offset: number): void {
    const [year, month, day] = this.selectedDate.split('-').map(Number);
    const date = new Date(year, month - 1, day);
    date.setDate(date.getDate() + offset);
    this.selectedDate = formatLocalDate(date);
    this.loadTasks();
  }

  goToToday(): void {
    this.selectedDate = formatLocalDate(new Date());
    this.loadTasks();
  }

  loadTasks(): void {
    this.loading = true;
    this.errorMessage = '';
    this.taskService.listForDate(this.selectedDate).subscribe({
      next: (tasks) => {
        this.tasks = tasks;
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
      task_date: this.selectedDate,
      due_time: this.newTime ? `${this.newTime}:00` : null,
    };

    this.taskService.create(payload).subscribe({
      next: () => {
        this.newTitle = '';
        this.newTime = '';
        this.saving = false;
        this.loadTasks();
      },
      error: () => {
        this.errorMessage = 'Could not create the task.';
        this.saving = false;
      },
    });
  }

  toggleDone(task: Task): void {
    const nextDone = !task.is_done;
    this.taskService.update(task.id, { is_done: nextDone }).subscribe({
      next: (updated) => {
        this.tasks = this.tasks.map((item) =>
          item.id === updated.id ? updated : item
        );
      },
      error: () => {
        this.errorMessage = 'Could not update the task.';
      },
    });
  }

  removeTask(task: Task): void {
    this.taskService.delete(task.id).subscribe({
      next: () => {
        this.tasks = this.tasks.filter((item) => item.id !== task.id);
      },
      error: () => {
        this.errorMessage = 'Could not delete the task.';
      },
    });
  }

  formatDueTime(dueTime: string | null): string {
    if (!dueTime) {
      return '';
    }
    return dueTime.slice(0, 5);
  }
}

function formatLocalDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}
