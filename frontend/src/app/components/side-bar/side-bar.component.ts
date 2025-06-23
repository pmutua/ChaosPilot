import { CommonModule } from '@angular/common';
import { Component, Input, Output, EventEmitter } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  standalone: true,
  imports: [
    CommonModule,
    RouterModule
  ],
  selector: 'app-side-bar',
  templateUrl: './side-bar.component.html',
  styleUrls: ['./side-bar.component.scss']
})
export class SideBarComponent {
  @Input() isOpen = true;
  @Output() sidebarToggle = new EventEmitter<void>();
  
  navigationItems = [
    {
      label: 'Dashboard',
      icon: '📊',
      route: '/dashboard',
      description: 'System overview and metrics'
    },
    {
      label: 'Log Analysis',
      icon: '🔍',
      route: '/chat',
      description: 'AI-powered log analysis and incident response'
    },
    {
      label: 'History',
      icon: '📋',
      route: '/history',
      description: 'Past incidents and resolutions'
    },
    {
      label: 'Settings',
      icon: '⚙️',
      route: '/settings',
      description: 'Configuration and preferences'
    }
  ];

  toggleSidebar() {
    this.sidebarToggle.emit();
  }
}