# Supabase Authentication Setup

This guide will help you set up Supabase authentication for the ChaosPilot application.

## Prerequisites

1. A Supabase account (sign up at https://supabase.com)
2. A Supabase project

## Setup Steps

### 1. Create a Supabase Project

1. Go to https://supabase.com and sign in
2. Click "New Project"
3. Choose your organization
4. Enter a project name (e.g., "chaospilot")
5. Enter a database password
6. Choose a region close to your users
7. Click "Create new project"

### 2. Get Your Project Credentials

1. In your Supabase dashboard, go to Settings > API
2. Copy your Project URL and anon/public key
3. You'll need these values for the environment configuration

### 3. Configure Environment Variables

1. Open `src/environments/environment.ts`
2. Replace the placeholder values with your actual Supabase credentials:

```typescript
export const environment = {
  production: false,
  supabaseUrl: 'https://your-actual-project-id.supabase.co',
  supabaseAnonKey: 'your-actual-anon-key'
};
```

3. Also update `src/environments/environment.prod.ts` with the same values for production.

### 4. Enable Email Authentication

1. In your Supabase dashboard, go to Authentication > Settings
2. Make sure "Enable email confirmations" is enabled
3. Configure your email templates if needed

### 5. Test the Authentication

1. Run the application: `ng serve`
2. Navigate to the landing page
3. Try signing up with a new email
4. Check your email for the confirmation link
5. Sign in with your credentials

## Features Implemented

- **Sign Up**: Users can create new accounts with email verification
- **Sign In**: Users can sign in with email and password
- **Sign Out**: Users can sign out from the application
- **Password Reset**: Users can request password reset emails
- **Route Protection**: Protected routes require authentication
- **Conditional UI**: Sidebar and dashboard buttons only show when authenticated

## Security Features

- All authentication is handled server-side by Supabase
- Passwords are securely hashed and stored
- Email verification required for new accounts
- Session management with automatic token refresh
- Route guards prevent unauthorized access

## Troubleshooting

### Common Issues

1. **"Invalid API key" error**: Make sure you're using the anon key, not the service role key
2. **Email not received**: Check spam folder and verify email templates in Supabase dashboard
3. **CORS errors**: Ensure your Supabase project URL is correct
4. **Authentication not working**: Check browser console for errors and verify environment configuration

### Getting Help

- Supabase Documentation: https://supabase.com/docs
- Supabase Community: https://github.com/supabase/supabase/discussions
- Angular Documentation: https://angular.io/docs 