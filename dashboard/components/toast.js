// dashboard/components/toast.js
// Handles displaying error and success states

export class ToastNotification {
    constructor() {
        this.container = document.getElementById('toast-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'toast-container';
            this.container.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                z-index: 10000;
            `;
            document.body.appendChild(this.container);
        }
    }

    show(message, type = 'error') {
        const toast = document.createElement('div');
        
        let bgColor = '#333';
        if (type === 'error') bgColor = 'var(--color-error, #dc2626)';
        if (type === 'success') bgColor = 'var(--color-success, #16a34a)';
        if (type === 'warning') bgColor = 'var(--color-warning, #f59e0b)';

        toast.style.cssText = `
            background-color: ${bgColor};
            color: white;
            padding: 12px 20px;
            border-radius: var(--radius-md, 8px);
            box-shadow: var(--shadow-md, 0 4px 6px rgba(0,0,0,0.1));
            font-family: var(--font-sans, sans-serif);
            font-size: 14px;
            opacity: 0;
            transform: translateY(20px);
            transition: all 0.3s ease;
        `;
        toast.textContent = message;

        this.container.appendChild(toast);

        // Animate in
        requestAnimationFrame(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        });

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(20px)';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
}

export const toast = new ToastNotification();
