// dashboard/auth/supabase-client.js
// Shared Supabase Instance Configuration

const SUPABASE_URL = 'https://cbysbvanpohcdgbrembr.supabase.co'; // To be replaced in actual environment
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNieXNidmFucG9oY2RnYnJlbWJyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc4ODcxNDcsImV4cCI6MjA5MzQ2MzE0N30.V4TvBwAaj9TZZqvkms47aA_ETY_kv_-8O153IpT3qmg'; // To be replaced

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
    // --- Data Fetching Methods --- //

    async getProjects(token) {
        try {
            const res = await fetch(`${this.url}/rest/v1/projects?select=*&order=created_at.desc`, {
                method: 'GET',
                headers: {
                    ...this.headers,
                    'Authorization': `Bearer ${token}` // Override anon key with user JWT
                }
            });
            const data = await res.json();
            if (!res.ok) return { error: data };
            return { data };
        } catch(e) {
            return { error: { message: "Failed to fetch projects." }};
        }
    }
    // --- Storage & Versioning Methods --- //

    async uploadFile(token, file, projectId) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            // Format: project_id/timestamp_filename
            const filePath = `${projectId || 'temp'}/${Date.now()}_${file.name}`;
            
            const res = await fetch(`${this.url}/storage/v1/object/html-uploads/${filePath}`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                    // Do not set Content-Type explicitly when using FormData, browser handles boundaries
                },
                body: formData
            });
            const data = await res.json();
            if (!res.ok) return { error: data };
            
            // Return public URL path
            const publicUrl = `${this.url}/storage/v1/object/public/html-uploads/${data.Key || filePath}`;
            return { data: { path: data.Key, url: publicUrl } };
        } catch(e) {
            return { error: { message: "Failed to upload file." }};
        }
    }

    async saveVersion(token, projectId, htmlUrl, notes) {
        try {
            const res = await fetch(`${this.url}/rest/v1/versions`, {
                method: 'POST',
                headers: {
                    ...this.headers,
                    'Authorization': `Bearer ${token}`,
                    'Prefer': 'return=representation'
                },
                body: JSON.stringify({
                    project_id: projectId,
                    version_number: Date.now(), // Simplified versioning logic
                    html_url: htmlUrl,
                    notes: notes
                })
            });
            const data = await res.json();
            if (!res.ok) return { error: data };
            return { data };
        } catch(e) {
            return { error: { message: "Failed to save version." }};
        }
    }
    async getProjectDetails(token, projectId) {
        try {
            const res = await fetch(`${this.url}/rest/v1/projects?id=eq.${projectId}`, {
                method: 'GET',
                headers: { ...this.headers, 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            if (!res.ok) return { error: data };
            return { data: data[0] }; // Return the single project object
        } catch(e) { return { error: { message: "Failed to fetch project details." }}; }
    }

    async getProjectVersions(token, projectId) {
        try {
            // Fetch versions ordered by creation date (newest first)
            const res = await fetch(`${this.url}/rest/v1/versions?project_id=eq.${projectId}&order=created_at.desc`, {
                method: 'GET',
                headers: { ...this.headers, 'Authorization': `Bearer ${token}` }
            });
            const data = await res.json();
            if (!res.ok) return { error: data };
            return { data };
        } catch(e) { return { error: { message: "Failed to fetch versions." }}; }
    }
}

export const supabaseClient = new SupabaseAuthClient(SUPABASE_URL, SUPABASE_ANON_KEY);
