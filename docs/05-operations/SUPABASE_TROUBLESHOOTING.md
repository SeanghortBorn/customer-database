# Supabase Troubleshooting Guide

## Rate Limiting Issues (Error 429)

### What This Means
Supabase applies rate limits to prevent abuse:
- **Free Tier**: ~500 requests per hour per IP
- **Authentication**: Stricter limits on signup/login attempts
- **Temporary**: Limits reset after waiting period

### Immediate Solutions

#### Option 1: Wait and Retry (Simplest)
```bash
# Wait 5-10 minutes, then try again
# The rate limit typically resets automatically
```

#### Option 2: Use Different Network
- Try from a different WiFi/network
- Use mobile hotspot temporarily
- Clear browser cache and cookies

#### Option 3: Check Supabase Dashboard
1. Visit: https://app.supabase.com
2. Go to your project → Settings → API
3. Check "Rate Limiting" section for details
4. View "Authentication" tab for user limits

### For Development/Testing

#### 1. Reduce Test Frequency
```javascript
// Add delays between test signups
await new Promise(resolve => setTimeout(resolve, 5000)); // 5s delay
```

#### 2. Reuse Test Accounts
Instead of creating new accounts, reuse existing ones:
```bash
# Delete test users from Supabase Dashboard:
# Authentication → Users → Select user → Delete
```

#### 3. Enable Email Confirmation (Reduces Spam Signups)
In Supabase Dashboard:
1. Authentication → Settings
2. Enable "Confirm email" 
3. This prevents abuse from bots

### For Production

#### Upgrade Supabase Plan
If hitting limits frequently in production:
1. Visit: https://app.supabase.com/project/[your-project]/settings/billing
2. Consider Pro plan ($25/mo) for:
   - Higher rate limits
   - Better performance
   - Priority support

#### Implement Client-Side Rate Limiting
Add cooldown to prevent repeated attempts:

```typescript
// In your signup component
const [cooldown, setCooldown] = useState(0);

useEffect(() => {
  if (cooldown > 0) {
    const timer = setTimeout(() => setCooldown(cooldown - 1), 1000);
    return () => clearTimeout(timer);
  }
}, [cooldown]);

const handleSignup = async (e: React.FormEvent) => {
  if (cooldown > 0) {
    setError(`Please wait ${cooldown} seconds before trying again`);
    return;
  }
  
  try {
    // ... signup logic
  } catch (err) {
    if (isRateLimitError(err)) {
      setCooldown(60); // 60 second cooldown
    }
  }
};
```

#### Monitor Your Usage
Track signup patterns to identify issues:
```sql
-- In Supabase SQL Editor
SELECT 
  DATE_TRUNC('hour', created_at) as hour,
  COUNT(*) as signups
FROM auth.users
GROUP BY hour
ORDER BY hour DESC
LIMIT 24;
```

## Other Common Supabase Issues

### Error: "Invalid API Key"
**Problem**: Wrong or expired Supabase credentials
**Solution**:
1. Check environment variables match:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
2. Regenerate keys in Dashboard if needed
3. Restart both frontend and backend after updating

### Error: "Email Not Confirmed"
**Problem**: User hasn't verified email
**Solution**:
1. Check Supabase → Authentication → Email Templates
2. Ensure email delivery is working
3. Test with your own email first
4. For development, disable email confirmation

### Error: "User Already Registered"
**Problem**: Email already exists in system
**Solution**:
```typescript
// Show helpful message
if (error.message.includes('already registered')) {
  setError('Email already registered. Try signing in instead.');
  // Optionally redirect to login
}
```

### Connection Timeouts
**Problem**: Slow or failed connections to Supabase
**Solution**:
1. Check Supabase status: https://status.supabase.com
2. Verify network connectivity
3. Check if region is appropriate (use closest region)
4. Consider implementing retry logic:

```typescript
const retryRequest = async (fn: Function, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await new Promise(r => setTimeout(r, 1000 * Math.pow(2, i))); // Exponential backoff
    }
  }
};
```

## Best Practices to Avoid Rate Limits

### 1. Implement Proper Authentication Flow
```typescript
// Check if user is already logged in
useEffect(() => {
  supabase.auth.getSession().then(({ data: { session } }) => {
    if (session) {
      router.push('/dashboard');
    }
  });
}, []);
```

### 2. Add Form Validation Before API Call
```typescript
// Validate email format client-side first
const isValidEmail = (email: string) => {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};

// Only call API if validation passes
if (!isValidEmail(email)) {
  setError('Please enter a valid email');
  return; // Don't call Supabase API
}
```

### 3. Debounce User Input
```typescript
import { useDebouncedCallback } from 'use-debounce';

const checkEmailExists = useDebouncedCallback(async (email) => {
  // Check if email exists (debounced to avoid too many calls)
}, 1000);
```

### 4. Use Session Persistence
```typescript
// Supabase automatically stores session in localStorage
// Just check for existing session on app load
const { data: { session } } = await supabase.auth.getSession();
```

## When to Contact Support

Contact Supabase support if:
- Rate limits seem unreasonably low for your usage
- You're on paid plan and hitting limits
- Issues persist after following all troubleshooting steps
- You suspect a bug or service issue

Support: https://supabase.com/support

## Monitoring and Alerts

Set up monitoring for authentication issues:

```typescript
// Log authentication failures
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_OUT' || event === 'USER_DELETED') {
    console.log('Auth event:', event);
  }
  
  if (event === 'TOKEN_REFRESHED') {
    console.log('Token refreshed successfully');
  }
});
```

## Quick Reference

| Error | Status Code | Solution |
|-------|-------------|----------|
| Rate Limited | 429 | Wait 5-10 minutes, try different network |
| Invalid Credentials | 400 | Check email/password |
| Email Not Confirmed | 400 | Check email for confirmation link |
| Network Error | 0 | Check internet, Supabase status |
| Invalid API Key | 401 | Verify environment variables |
| Forbidden | 403 | Check RLS policies in Supabase |

For more help, see:
- Supabase Docs: https://supabase.com/docs/guides/auth
- Status Page: https://status.supabase.com
- GitHub Issues: https://github.com/supabase/supabase/issues
