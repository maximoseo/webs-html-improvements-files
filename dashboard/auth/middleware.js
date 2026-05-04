// dashboard/auth/middleware.js
// Route protection, redirect to login, rate limit tracking client-side wrapper

import { sessionManager } from './session-manager.js';

const RATE_LIMIT_KEY = 'maximo_login_attempts';
const MAX_ATTEMPTS = 5;
const LOCKOUT_DURATION = 5 * 60 * 1000; // 5 minutes

export function requireAuth() {
    const session = sessionManager.getSession();
    if (!session || !session.access_token) {
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

export function trackLoginAttempt(success) {
    let attempts = JSON.parse(localStorage.getItem(RATE_LIMIT_KEY)) || { count: 0, lockoutUntil: null };
    
    if (success) {
        localStorage.removeItem(RATE_LIMIT_KEY);
        return { allowed: true };
    }

    // Failed attempt
    attempts.count += 1;
    if (attempts.count >= MAX_ATTEMPTS) {
        attempts.lockoutUntil = Date.now() + LOCKOUT_DURATION;
    }
    localStorage.setItem(RATE_LIMIT_KEY, JSON.stringify(attempts));
    
    return checkRateLimit();
}

export function checkRateLimit() {
    const attempts = JSON.parse(localStorage.getItem(RATE_LIMIT_KEY));
    if (!attempts) return { allowed: true };

    if (attempts.lockoutUntil) {
        const now = Date.now();
        if (now < attempts.lockoutUntil) {
            const minutesLeft = Math.ceil((attempts.lockoutUntil - now) / 60000);
            return { allowed: false, minutesLeft };
        } else {
            // Lockout expired
            localStorage.removeItem(RATE_LIMIT_KEY);
            return { allowed: true };
        }
    }
    return { allowed: true, count: attempts.count };
}
