import { Component } from '@angular/core';

import { DayViewComponent } from './components/day-view/day-view.component';

@Component({
  selector: 'app-root',
  imports: [DayViewComponent],
  template: '<app-day-view />',
  styleUrl: './app.component.css',
})
export class AppComponent {}
