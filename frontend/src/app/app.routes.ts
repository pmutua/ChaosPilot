import { Routes } from '@angular/router';
import { ChatComponent } from './components/chat/chat.component';
import { HistoryComponent } from './components/history/history.component';
import { SettingsComponent } from './components/settings/settings.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LandingComponent } from './components/landing/landing.component';
import { AuthGuard } from './guards/auth.guard';
import { PublicGuard } from './guards/public.guard';

export const routes: Routes = [
  { path: 'landing', component: LandingComponent, canActivate: [PublicGuard] },
  { 
    path: 'dashboard', 
    component: DashboardComponent,
    canActivate: [AuthGuard]
  },
  { 
    path: 'chat', 
    component: ChatComponent,
    canActivate: [AuthGuard]
  },
  { 
    path: 'history', 
    component: HistoryComponent,
    canActivate: [AuthGuard]
  },
  { 
    path: 'settings', 
    component: SettingsComponent,
    canActivate: [AuthGuard]
  },
  { path: '', redirectTo: '/landing', pathMatch: 'full' }
];