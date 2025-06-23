import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-history',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.scss']
})
export class HistoryComponent {
  pastChats = [
    { id: 1, title: 'Memory outage in Europe zone', date: '2023-06-15', status: 'Resolved' },
    { id: 2, title: 'Database connection issues', date: '2023-06-14', status: 'Resolved' },
    { id: 3, title: 'Network latency spikes', date: '2023-06-12', status: 'In Progress' },
    { id: 4, title: 'API gateway timeout errors', date: '2023-06-10', status: 'Resolved' }
  ];
}