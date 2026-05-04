// dashboard/auth/session-manager.js
// Token refresh, expiry, rotation

import { supabaseClient } from './supabase-client.js';

class SessionManager {
    constructor() {
        this.sessionKey = 'maximo_auth_session';
        this.refreshInterval = null;
    }

    saveSession(sessionData) {
        localStorage.setItem(this.sessionKey, JSON.stringify(sessionData));
        this.startRefreshTimer(sessionData.expires_in);
    }

    getSession() {
        const data = localStorage.getItem(this.sessionKey);
        return data ? JSON.parse(data) : null;
    }

    clearSession() {
        localStorage.removeItem(this.sessionKey);
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        // Force expiry of the legacy Python server cookie on logout
        document.cookie = "dash_auth=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    }

    startRefreshTimer(expiresInSeconds) {
        if (this.refreshInterval) clearInterval(this.refreshInterval);
        
        // Refresh 2 minutes before expiry or every 15 mins (whichever is appropriate based on Supabase config)
        const refreshTime = Math.min((expiresInSeconds - 120) * 1000, 15 * 60 * 1000); 
        
        this.refreshInterval = setInterval(async () => {
            const currentSession = this.getSession();
            if (currentSession && currentSession.refresh_token) {
                try {
                    const newSession = await supabaseClient.refreshSession(currentSession.refresh_token);
                    if (newSession.access_token) {
                        this.saveSession(newSession);
                    } else {
                        // Refresh failed, likely expired
                        this.clearSession();
                        window.location.href = '/login.html';
                    }
                } catch (e) {
                    console.error("Session refresh failed", e);
                }
            }
        }, refreshTime > 0 ? refreshTime : 15 * 60 * 1000); // Default to 15 mins
    }
    
    init() {
        const session = this.getSession();
        if (session) {
            // Check if expired
            const now = Math.floor(Date.now() / 1000);
            // Rough estimation if missing exact expiry timestamp
            this.startRefreshTimer(3600); // Kickoff timer 
        }
    }
}

export const sessionManager = new SessionManager();
sessionManager.init();
