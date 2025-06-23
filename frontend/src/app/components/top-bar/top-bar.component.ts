import { Component, EventEmitter, Output } from '@angular/core';
import { AgentService } from '../../services/agent.service';
import { SupabaseService } from '../../services/supabase.service';
import { Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { GoogleAdkService } from '../../services/google-adk.service';

@Component({
  standalone: true,
  selector: 'app-top-bar',
  templateUrl: './top-bar.component.html',
  styleUrls: ['./top-bar.component.scss'],
  imports: [CommonModule, RouterModule]
})
export class TopBarComponent {
  @Output() toggleSidebar = new EventEmitter<void>();

  isUserMenuOpen = false;

  constructor(
    private googleAdkService: GoogleAdkService,
    private supabaseService: SupabaseService,
    private router: Router
  ) {}

  onToggleSidebar(): void {
    this.toggleSidebar.emit();
  }

  toggleUserMenu(): void {
    this.isUserMenuOpen = !this.isUserMenuOpen;
  }

  async quickAnalysis(): Promise<void> {
    try {
      await this.googleAdkService.createOrResumeSession();
      await this.googleAdkService.sendMessage({
        role: 'user',
        parts: [{ text: 'Perform a quick analysis of recent logs' }]
      });
      this.router.navigate(['/chat']);
    } catch (error) {
      console.error('Failed to start quick analysis:', error);
    }
  }

  viewLogs(): void {
    this.router.navigate(['/chat']);
  }

  async logout(): Promise<void> {
    try {
      await this.supabaseService.signOut();
      this.router.navigate(['/landing']);
    } catch (error) {
      console.error('Error signing out:', error);
    }
  }
}