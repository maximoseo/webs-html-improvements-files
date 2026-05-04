// dashboard/auth/supabase-client.js
// Shared Supabase Instance Configuration

const SUPABASE_URL = 'https://wtpczvyupmavzrxisvcm.supabase.co'; // To be replaced in actual environment
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0cGN6dnl1cG1hdnpyeGlzdmNtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njg3MjEyOTgsImV4cCI6MjA4NDI5NzI5OH0.-_AP23-lVz_v3HPrqp4HfN4_QJZ_0zklfyRb9tSeTk4'; // To be replaced

// Create a single instance using the standard JS library or simple REST if vanilla
// In Vanilla JS without bundler, we assume the Supabase CDN script is loaded or we use REST methods

class SupabaseAuthClient {
    constructor(url, key) {
        this.url = url;
        this.key = key;
        this.headers = {
            'apikey': this.key,
            'Authorization': `Bearer ${this.key}`,
            'Content-Type': 'application/json'
        };
    }

    async signIn(email, password) {
        try {
            const res = await fetch(`${this.url}/auth/v1/token?grant_type=password`, {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify({ email, password })
            });
            const data = await res.json();
            if (!res.ok) { return { error: data }; }
            return data;
        } catch(e) {
            return { error: { message: "Network error or Supabase unavailable." }};
        }
    }

    async refreshSession(refreshToken) {
        try {
            const res = await fetch(`${this.url}/auth/v1/token?grant_type=refresh_token`, {
                method: 'POST',
                headers: this.headers,
                body: JSON.stringify({ refresh_token: refreshToken })
            });
            const data = await res.json();
            if (!res.ok) { return { error: data }; }
            return data;
        } catch(e) {
            return { error: { message: "Failed to refresh session." }};
        }
    }/auth/v1/token?grant_type=refresh_token`, {
            method: 'POST',
            headers: this.headers,
            body: JSON.stringify({ refresh_token: refreshToken })
        });
        return await res.json();
    }
}

export const supabaseClient = new SupabaseAuthClient(SUPABASE_URL, SUPABASE_ANON_KEY);
