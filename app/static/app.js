document.addEventListener('DOMContentLoaded', () => {
    // ---- Profile Menu Toggling ----
    const avatarContainer = document.getElementById('avatar-container');
    const profileMenu = document.getElementById('profile-menu');
    const userAvatar = document.getElementById('user-avatar');
    const largeAvatar = document.getElementById('large-avatar');
    const initialInput = document.getElementById('initial-input');
    const updateBtn = document.getElementById('update-initial-btn');

    // Load initial from localStorage
    const savedInitial = localStorage.getItem('userInitial') || 'P';
    if (userAvatar) userAvatar.textContent = savedInitial;
    if (largeAvatar) largeAvatar.textContent = savedInitial;
    if (initialInput) initialInput.value = savedInitial;

    if (avatarContainer && profileMenu) {
        avatarContainer.addEventListener('click', (e) => {
            e.stopPropagation();
            profileMenu.classList.toggle('show');
        });

        // Update initial
        if (updateBtn && initialInput) {
            updateBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                const newInitial = initialInput.value.trim().toUpperCase() || 'P';
                userAvatar.textContent = newInitial;
                largeAvatar.textContent = newInitial;
                localStorage.setItem('userInitial', newInitial);
                profileMenu.classList.remove('show');
            });

            initialInput.addEventListener('click', (e) => e.stopPropagation());
            initialInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') updateBtn.click();
            });
        }

        // Close menu when clicking outside
        document.addEventListener('click', () => {
            profileMenu.classList.remove('show');
        });
    }

    // ---- Sidebar toggle (mobile) ----
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
            if (overlay) overlay.classList.toggle('show');
        });

        // Close sidebar when clicking overlay
        if (overlay) {
            overlay.addEventListener('click', () => {
                sidebar.classList.remove('open');
                overlay.classList.remove('show');
            });
        }

        // Close sidebar when clicking outside on mobile
        document.addEventListener('click', (e) => {
            if (
                window.innerWidth <= 768 &&
                sidebar.classList.contains('open') &&
                !sidebar.contains(e.target) &&
                !sidebarToggle.contains(e.target) &&
                !avatarContainer.contains(e.target) &&
                (!overlay || !overlay.contains(e.target))
            ) {
                sidebar.classList.remove('open');
                if (overlay) overlay.classList.remove('show');
            }
        });
    }

    // ---- Auto-dismiss toast notifications ----
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach((toast, i) => {
        setTimeout(() => {
            toast.style.animation = 'toastOut 0.3s ease-in forwards';
            setTimeout(() => toast.remove(), 300);
        }, 4000 + i * 500);
    });

    // Add toast-out animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes toastOut {
            to { opacity: 0; transform: translateY(30px); }
        }
    `;
    document.head.appendChild(style);

    // ---- Email row hover effects ----
    const emailRows = document.querySelectorAll('.email-row');
    emailRows.forEach(row => {
        const link = row.querySelector('.email-row-link');
        if (link) {
            // Make entire row clickable (except checkboxes & stars)
            row.addEventListener('click', (e) => {
                if (
                    !e.target.closest('.checkbox-wrapper') &&
                    !e.target.closest('.star-btn') &&
                    !e.target.closest('.delete-action')
                ) {
                    link.click();
                }
            });
        }
    });

    // ---- Select All checkbox ----
    const selectAll = document.getElementById('select-all');
    if (selectAll) {
        selectAll.addEventListener('change', (e) => {
            const checkboxes = document.querySelectorAll('.email-checkbox');
            checkboxes.forEach(cb => {
                cb.checked = e.target.checked;
            });
        });
    }

    // ---- Keyboard shortcuts ----
    document.addEventListener('keydown', (e) => {
        // 'c' to compose (when not in input)
        if (
            e.key === 'c' &&
            !e.target.matches('input, textarea, select')
        ) {
            const composeBtn = document.getElementById('compose-btn');
            if (composeBtn) {
                e.preventDefault();
                composeBtn.click();
            }
        }

        // '/' to focus search
        if (
            e.key === '/' &&
            !e.target.matches('input, textarea, select')
        ) {
            const searchInput = document.getElementById('search-input');
            if (searchInput) {
                e.preventDefault();
                searchInput.focus();
            }
        }

        // Escape to close search
        if (e.key === 'Escape') {
            const searchInput = document.getElementById('search-input');
            if (searchInput && document.activeElement === searchInput) {
                searchInput.blur();
            }
        }
    });

    // ---- Compose form: auto-fill date to now if empty ----
    const dateInput = document.getElementById('received-date');
    if (dateInput && !dateInput.value) {
        const now = new Date();
        // Format: YYYY-MM-DDTHH:MM
        const pad = (n) => String(n).padStart(2, '0');
        const formatted = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
        dateInput.value = formatted;
    }

    // ---- Email row entrance animation ----
    emailRows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateY(8px)';
        row.style.transition = `opacity 0.3s ease ${index * 0.03}s, transform 0.3s ease ${index * 0.03}s`;
        requestAnimationFrame(() => {
            row.style.opacity = '1';
            row.style.transform = 'translateY(0)';
        });
    });

    // ---- Local Device Persistence (Enhanced Sync) ----
    const emailDataEl = document.getElementById('email-data');
    const offlineModal = document.getElementById('offline-modal');
    const closeModal = document.getElementById('close-modal');

    function openOfflineEmail(email) {
        if (!offlineModal) return;
        document.getElementById('modal-subject').textContent = email.subject || '(no subject)';
        document.getElementById('modal-sender').textContent = email.sender || 'Unknown';
        document.getElementById('modal-sender-email').textContent = `<${email.sender_email || 'unknown@example.com'}>`;
        document.getElementById('modal-sender-avatar').textContent = (email.sender || 'U').charAt(0).toUpperCase();
        document.getElementById('modal-email-body').textContent = email.body || '';
        offlineModal.classList.add('show');
    }

    if (closeModal) {
        closeModal.addEventListener('click', () => offlineModal.classList.remove('show'));
    }
    if (offlineModal) {
        offlineModal.addEventListener('click', (e) => {
            if (e.target === offlineModal) offlineModal.classList.remove('show');
        });
    }

    if (emailDataEl) {
        const serverEmails = JSON.parse(emailDataEl.textContent);
        let localEmails = JSON.parse(localStorage.getItem('localEmails') || '[]');

        // Sync logic: merge server data into local storage
        serverEmails.forEach(serverMail => {
            const index = localEmails.findIndex(m => m.id === serverMail.id);
            if (index === -1) {
                localEmails.push(serverMail);
            } else {
                // Update existing with potential changes (starred, read, etc)
                localEmails[index] = { ...localEmails[index], ...serverMail };
            }
        });

        // Limit storage to last 500 emails to prevent bloat
        if (localEmails.length > 500) localEmails = localEmails.slice(-500);
        localStorage.setItem('localEmails', JSON.stringify(localEmails));

        const emailList = document.getElementById('email-list');
        const emptyState = document.getElementById('empty-inbox');
        
        // If the server returns nothing (or we are offline), restore from local storage
        if (emptyState && !window.is_search && localEmails.length > 0) {
            // Filter by folder if possible (default to inbox if not specified)
            const pathParts = window.location.pathname.split('/').filter(p => p);
            const currentFolder = pathParts[pathParts.length - 1] || 'inbox';
            
            const folderEmails = localEmails.filter(m => m.folder === currentFolder || (currentFolder === 'starred' && m.is_starred));

            if (folderEmails.length > 0) {
                emailList.innerHTML = '';
                folderEmails.slice().reverse().forEach(email => {
                    const row = document.createElement('div');
                    row.className = `email-row row-restored ${email.is_read ? '' : 'unread'}`;
                    row.innerHTML = `
                        <div class="email-row-left">
                            <label class="checkbox-wrapper"><input type="checkbox" class="email-checkbox"><span class="checkmark"></span></label>
                            <span class="star-btn ${email.is_starred ? 'starred' : ''}" style="margin-left: 8px;">
                                <span class="material-icons-outlined" style="font-size: 20px;">
                                    ${email.is_starred ? 'star' : 'star_border'}
                                </span>
                            </span>
                        </div>
                        <div class="email-row-link" style="cursor: pointer;">
                            <span class="email-sender">${email.sender}</span>
                            <div class="email-content-preview">
                                <span class="email-subject">${email.subject}</span>
                                <span class="email-snippet"> — ${email.snippet}</span>
                            </div>
                            <span class="email-date">${email.date}</span>
                        </div>
                        <div class="email-row-actions">
                            <span class="icon-btn" title="Saved on device">
                                <span class="material-icons-outlined" style="color: var(--green);">offline_pin</span>
                            </span>
                        </div>
                    `;
                    
                    row.addEventListener('click', (e) => {
                        if (!e.target.closest('.checkbox-wrapper') && !e.target.closest('.star-btn')) {
                            // Try to go to detail page, but if it fails (offline), open modal
                            openOfflineEmail(email);
                        }
                    });
                    
                    emailList.appendChild(row);
                });
                
                const countEl = document.getElementById('email-count');
                if (countEl) countEl.innerHTML = `1–${folderEmails.length} <span style="color: var(--green); font-weight: bold; margin-left: 8px;">✔ Saved Locally</span>`;
            }
        }
    }
});
