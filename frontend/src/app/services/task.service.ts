import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import {
  Task,
  TaskCreatePayload,
  TaskGrouped,
  TaskUpdatePayload,
} from '../models/task.model';

const API_BASE = 'http://localhost:8000/api';

@Injectable({ providedIn: 'root' })
export class TaskService {
  constructor(private readonly http: HttpClient) {}

  listGrouped(referenceDate: string): Observable<TaskGrouped> {
    const params = new HttpParams().set('reference_date', referenceDate);
    return this.http.get<TaskGrouped>(`${API_BASE}/tasks`, { params });
  }

  create(payload: TaskCreatePayload): Observable<Task> {
    return this.http.post<Task>(`${API_BASE}/tasks`, payload);
  }

  update(taskId: number, payload: TaskUpdatePayload): Observable<Task> {
    return this.http.patch<Task>(`${API_BASE}/tasks/${taskId}`, payload);
  }

  delete(taskId: number): Observable<void> {
    return this.http.delete<void>(`${API_BASE}/tasks/${taskId}`);
  }
}
