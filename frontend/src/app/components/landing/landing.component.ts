import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { SupabaseService } from '../../services/supabase.service';
import { Subscription } from 'rxjs';

interface Feature {
  icon: string;
  title: string;
  description: string;
  color: string;
}

interface Step {
  number: number;
  title: string;
  description: string;
  icon: string;
}

@Component({
  standalone: true,
  imports: [CommonModule, FormsModule],
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.scss']
})
export class LandingComponent implements OnInit, OnDestroy {
  isAuthenticated = false;
  showLoginForm = false;
  isSignUp = false;
  isLoading = false;
  authError = '';
  authMessage = '';
  authData = {
    email: '',
    password: ''
  };

  features: Feature[] = [
    {
      icon: '🔍',
      title: 'AI-Powered Log Analysis',
      description: 'Intelligent analysis of error, warning, and critical logs using advanced LLMs to detect patterns and anomalies.',
      color: 'bg-blue-500'
    },
    {
      icon: '⚡',
      title: 'Real-time Incident Response',
      description: 'Instant detection and automated response to system failures and performance issues from log analysis.',
      color: 'bg-green-500'
    },
    {
      icon: '🧠',
      title: 'Smart Root Cause Analysis',
      description: 'Deep insights into log patterns, service dependencies, and automated root cause identification.',
      color: 'bg-purple-500'
    },
    {
      icon: '🛠️',
      title: 'Automated Fix Recommendations',
      description: 'AI-generated fix suggestions and automated remediation for common issues detected in logs.',
      color: 'bg-red-500'
    }
  ];

  steps: Step[] = [
    {
      number: 1,
      title: 'Analyze',
      description: 'AI agents analyze error, warning, and critical logs to identify patterns, anomalies, and potential issues.',
      icon: '🔍'
    },
    {
      number: 2,
      title: 'Classify',
      description: 'Automatically classify incidents by severity, impact, and type based on log analysis.',
      icon: '📊'
    },
    {
      number: 3,
      title: 'Plan',
      description: 'Generate comprehensive response plans and fix recommendations using LLM-powered analysis.',
      icon: '📋'
    },
    {
      number: 4,
      title: 'Resolve',
      description: 'Execute automated fixes or guide teams through manual resolution with step-by-step instructions.',
      icon: '✅'
    }
  ];

  private authSubscription: Subscription;

  constructor(
    private router: Router,
    private supabaseService: SupabaseService
  ) {
    this.authSubscription = this.supabaseService.currentUser$.subscribe(user => {
      this.isAuthenticated = user !== null;
    });
  }

  ngOnInit(): void {
    // Check if user is already authenticated
    this.isAuthenticated = this.supabaseService.isAuthenticated();
  }

  ngOnDestroy(): void {
    if (this.authSubscription) {
      this.authSubscription.unsubscribe();
    }
  }

  async signIn(): Promise<void> {
    if (!this.authData.email || !this.authData.password) {
      this.authError = 'Please enter both email and password';
      return;
    }

    this.isLoading = true;
    this.authError = '';

    try {
      const { data, error } = await this.supabaseService.signIn(this.authData.email, this.authData.password);
      
      if (error) {
        this.authError = error.message || 'Sign in failed';
      } else {
        this.showLoginForm = false;
        this.authData = { email: '', password: '' };
        this.router.navigate(['/dashboard']);
      }
    } catch (error) {
      this.authError = 'An unexpected error occurred';
    } finally {
      this.isLoading = false;
    }
  }

  async signUp(): Promise<void> {
    if (!this.authData.email || !this.authData.password) {
      this.authError = 'Please enter both email and password';
      return;
    }

    if (this.authData.password.length < 6) {
      this.authError = 'Password must be at least 6 characters long';
      return;
    }

    this.isLoading = true;
    this.authError = '';
    this.authMessage = '';

    try {
      const { data, error } = await this.supabaseService.signUp(this.authData.email, this.authData.password);
      
      if (error) {
        this.authError = error.message || 'Sign up failed';
      } else {
        this.authMessage = 'Please check your email for verification link';
        this.isSignUp = false;
      }
    } catch (error) {
      this.authError = 'An unexpected error occurred';
    } finally {
      this.isLoading = false;
    }
  }

  async signOut(): Promise<void> {
    try {
      await this.supabaseService.signOut();
      this.router.navigate(['/landing']);
    } catch (error) {
      console.error('Sign out error:', error);
    }
  }

  async resetPassword(): Promise<void> {
    if (!this.authData.email) {
      this.authError = 'Please enter your email address';
      return;
    }

    this.isLoading = true;
    this.authError = '';

    try {
      const { error } = await this.supabaseService.resetPassword(this.authData.email);
      
      if (error) {
        this.authError = error.message || 'Password reset failed';
      } else {
        this.authError = 'Password reset email sent. Please check your inbox.';
      }
    } catch (error) {
      this.authError = 'An unexpected error occurred';
    } finally {
      this.isLoading = false;
    }
  }

  getStarted(): void {
    if (this.isAuthenticated) {
      this.router.navigate(['/chat']);
    } else {
      this.showLoginForm = true;
    }
  }

  viewDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
} 