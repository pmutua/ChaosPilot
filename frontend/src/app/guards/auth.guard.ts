import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SupabaseService } from '../services/supabase.service';
import { map, take, filter } from 'rxjs/operators';
import { Observable } from 'rxjs';

export const AuthGuard: CanActivateFn = (route, state): Observable<boolean> => {
  const supabaseService = inject(SupabaseService);
  const router = inject(Router);

  return supabaseService.currentUser$.pipe(
    filter(user => user !== undefined), // Wait until auth state is determined
    take(1),
    map(user => {
      if (user) {
        return true;
      } else {
        router.navigate(['/landing']);
        return false;
      }
    })
  );
}; 