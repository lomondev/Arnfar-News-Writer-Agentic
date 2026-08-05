// Icon SVG maps
const ICONS = {
    play: `<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>`,
    bolt: `<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M19 9h-6l2.5-9L6 15h6l-2.5 9z"/></svg>`,
    code: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>`,
    check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>`,
    cross: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>`,
    globe: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>`,
    lock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>`,
    layers: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>`,
    chart: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
    spark: `<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l2.4 7.6 7.6 2.4-7.6 2.4-2.4 7.6-2.4-7.6-7.6-2.4 7.6-2.4z"/></svg>`,
    doc: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>`,
    clock: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
    video: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="2" y="2" width="20" height="20" rx="2"/><line x1="7" y1="2" x2="7" y2="22"/><line x1="17" y1="2" x2="17" y2="22"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="2" y1="7" x2="7" y2="7"/><line x1="2" y1="17" x2="7" y2="17"/><line x1="17" y1="17" x2="22" y2="17"/><line x1="17" y1="7" x2="22" y2="7"/></svg>`
};

document.addEventListener('DOMContentLoaded', () => {
    const specSelector = document.getElementById('specSelector');
    const mainContainer = document.getElementById('mainContainer');
    const themeToggle = document.getElementById('themeToggle');
    const viewButtons = {
        desktop: document.getElementById('btnDesktop'),
        tablet: document.getElementById('btnTablet'),
        mobile: document.getElementById('btnMobile')
    };

    // Load theme setting
    const savedTheme = localStorage.getItem('arnfar-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeToggle.querySelector('.theme-icon').textContent = savedTheme === 'dark' ? '🌙' : '☀️';

    // Theme toggler
    themeToggle.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', nextTheme);
        localStorage.setItem('arnfar-theme', nextTheme);
        themeToggle.querySelector('.theme-icon').textContent = nextTheme === 'dark' ? '🌙' : '☀️';
    });

    // Viewport Simulator Toggles
    Object.keys(viewButtons).forEach(view => {
        viewButtons[view].addEventListener('click', () => {
            // Remove active classes
            Object.values(viewButtons).forEach(btn => btn.classList.remove('active'));
            viewButtons[view].classList.add('active');

            // Apply simulation layout classes
            mainContainer.className = `app-main-layout ${view}-layout`;
        });
    });

    // Handle Spec Selector changes
    specSelector.addEventListener('change', (e) => {
        loadSpec(e.target.value);
    });

    // Initial spec load
    loadSpec(specSelector.value);

    // Main loader
    function loadSpec(url) {
        mainContainer.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <p>ກຳລັງດຶງຂໍ້ມູນ Spec...</p>
            </div>
        `;

        fetch(url)
            .then(res => {
                if (!res.ok) throw new Error('Cannot load spec file');
                return res.json();
            })
            .then(data => {
                renderCards(data);
            })
            .catch(err => {
                mainContainer.innerHTML = `
                    <div class="loading-state">
                        <span style="font-size: 48px;">⚠️</span>
                        <p style="color: #ef4444; font-weight: 700;">ບໍ່ສາມາດໂຫລດ Spec ໄດ້: ${err.message}</p>
                        <p style="font-size: 13px;">ກະລຸນາກວດສອບໄຟລ໌ spec ໃນ output/ ວ່າຖືກຕ້ອງຕາມ format ຫຼື ບໍ່</p>
                    </div>
                `;
            });
    }

    // Dynamic Card Node Builder
    function renderCards(spec) {
        mainContainer.innerHTML = '';
        const cards = spec.cards || [];
        const globalBrand = spec.brand || 'Arnfar';
        const globalCategory = spec.category || '';
        const globalFooterTags = spec.footer_tags || '#arnfar   #ArnfarERP   #arnfar.com';
        
        cards.forEach((card, idx) => {
            const cardWrapper = document.createElement('div');
            cardWrapper.className = 'card-image-wrapper';
            
            // Set dynamic orb variations for each card based on index
            const variants = ['lines', 'dots', 'diag', 'none'];
            const variant = variants[idx % variants.length];
            cardWrapper.setAttribute('data-bg-variant', variant);

            // Construct Card Header Bar
            const headerBar = document.createElement('div');
            headerBar.className = 'card-header-bar';

            const headerTags = document.createElement('div');
            headerTags.className = 'card-header-tags';

            const tags = card.tags || spec.tags;
            if (tags && tags.length > 0) {
                tags.forEach((tag, i) => {
                    const tagPill = document.createElement('span');
                    tagPill.className = `tag-pill ${i === 0 ? 'highlight' : 'normal'}`;
                    tagPill.textContent = tag;
                    headerTags.appendChild(tagPill);
                });
            } else {
                const catText = card.category || globalCategory;
                if (catText) {
                    const catPill = document.createElement('span');
                    catPill.className = 'tag-pill normal';
                    catPill.textContent = catText;
                    headerTags.appendChild(catPill);
                }
            }
            headerBar.appendChild(headerTags);

            const brandLogo = document.createElement('div');
            brandLogo.className = 'card-brand-logo';
            // Default icon is logo
            brandLogo.innerHTML = `
                <img class="brand-icon" src="../arnfar-icon/arnfar-nobg.png" alt="" onerror="this.style.display='none'">
                <span>${card.brand || globalBrand}</span>
            `;
            headerBar.appendChild(brandLogo);
            cardWrapper.appendChild(headerBar);

            // Construct Card Content Container
            const contentBody = document.createElement('div');
            contentBody.className = 'card-content-body';

            // Headline block for Hero, Code, Feature types
            if (['hero', 'code', 'feature'].includes(card.kind || 'hero')) {
                if (card.eyebrow) {
                    const eyebrow = document.createElement('div');
                    eyebrow.className = 'card-eyebrow';
                    eyebrow.textContent = card.eyebrow;
                    contentBody.appendChild(eyebrow);
                }

                if (card.headline && card.headline.length > 0) {
                    const headline = document.createElement('h1');
                    headline.className = 'card-headline';
                    
                    let hlContent = card.headline.join('<br>');
                    if (card.accent) {
                        hlContent += `<br><span class="card-accent-text">${card.accent}</span>`;
                    }
                    headline.innerHTML = hlContent;
                    contentBody.appendChild(headline);
                    
                    const underline = document.createElement('div');
                    underline.className = 'headline-underline';
                    contentBody.appendChild(underline);
                }

                if (card.subhead) {
                    const subhead = document.createElement('p');
                    subhead.className = 'card-subhead';
                    subhead.textContent = card.subhead;
                    contentBody.appendChild(subhead);
                }
            }

            // Render specific components per card kind
            const innerGlassCard = document.createElement('div');
            innerGlassCard.className = 'glass-card';

            const kind = card.kind || 'hero';
            if (kind === 'hero') {
                renderHeroContent(contentBody, card);
            } else if (kind === 'code') {
                renderCodeContent(contentBody, card, idx);
            } else if (kind === 'points') {
                renderPointsContent(contentBody, card);
            } else if (kind === 'stat') {
                renderStatContent(contentBody, card);
            } else if (kind === 'showcase') {
                renderShowcaseContent(contentBody, card, idx);
            } else if (kind === 'feature') {
                renderFeatureContent(contentBody, card, idx);
            } else if (kind === 'stack') {
                renderStackContent(contentBody, card);
            }

            cardWrapper.appendChild(contentBody);

            // Construct Card Footer Bar (Showcase template uses no footer)
            if (kind !== 'showcase') {
                const footerBar = document.createElement('div');
                footerBar.className = 'card-footer-bar';
                
                const footerLine = document.createElement('div');
                footerLine.className = 'footer-line';
                footerBar.appendChild(footerLine);

                const footerText = document.createElement('div');
                footerText.className = 'footer-tags';
                footerText.textContent = card.footer_tags || globalFooterTags;
                footerBar.appendChild(footerText);

                cardWrapper.appendChild(footerBar);
            }

            mainContainer.appendChild(cardWrapper);
        });
    }

    // 1. RENDER HERO CONTENT
    function renderHeroContent(container, card) {
        const statsArea = document.createElement('div');
        statsArea.className = 'hero-stats';

        if (card.stat) {
            const statRow = document.createElement('div');
            statRow.className = 'hero-stat-row';
            statRow.innerHTML = `
                <span class="hero-stat-value">${card.stat.value}</span>
                <span class="hero-stat-label">${card.stat.label || ''}</span>
            `;
            statsArea.appendChild(statRow);
        }

        if (card.chips && card.chips.length > 0) {
            const subChips = document.createElement('div');
            subChips.className = 'stat-sub-chips';
            card.chips.forEach(chip => {
                const chipPill = document.createElement('span');
                chipPill.className = 'sub-chip';
                chipPill.textContent = chip;
                subChips.appendChild(chipPill);
            });
            statsArea.appendChild(subChips);
        }

        if (card.date) {
            const dateBlock = document.createElement('div');
            dateBlock.className = 'hero-date-block';
            dateBlock.innerHTML = `
                <div class="hero-date-text">${card.date}</div>
                <div class="hero-date-sub">${card.date_sub || ''}</div>
            `;
            statsArea.appendChild(dateBlock);
        }

        container.appendChild(statsArea);
    }

    // 2. RENDER CODE CONTENT
    function renderCodeContent(container, card, seed) {
        const codeWin = document.createElement('div');
        codeWin.className = 'code-window glass-card';
        
        // Header
        const filename = card.file || 'main.go';
        codeWin.innerHTML = `
            <div class="code-titlebar">
                <div class="traffic-lights">
                    <span class="light-dot red"></span>
                    <span class="light-dot yellow"></span>
                    <span class="light-dot green"></span>
                </div>
                <div class="code-filename">${filename}</div>
                <div style="width: 42px;"></div>
            </div>
            <div class="code-editor-content">
                <!-- Decorative pseudo syntax rows -->
                <div class="code-row-bar"><span class="code-block-pill" style="width: 40px; background-color: var(--brand-green);"></span><span class="code-block-pill" style="width: 80px; background-color: var(--brand-blue);"></span></div>
                <div class="code-row-bar" style="margin-left: 20px;"><span class="code-block-pill" style="width: 60px; background-color: var(--text-muted);"></span><span class="code-block-pill" style="width: 90px; background-color: var(--brand-green);"></span></div>
                <div class="code-row-bar" style="margin-left: 20px;"><span class="code-block-pill" style="width: 110px; background-color: var(--brand-blue);"></span></div>
                <div class="code-row-bar" style="margin-left: 40px;"><span class="code-block-pill" style="width: 50px; background-color: var(--brand-green);"></span><span class="code-block-pill" style="width: 70px; background-color: var(--text-primary);"></span></div>
                <div class="code-row-bar"><span class="code-block-pill" style="width: 20px; background-color: var(--brand-green); animation: pulseCursor 1s infinite alternate;"></span></div>
                
                ${card.badge ? `
                    <div class="badge-float">
                        <span class="badge-sparkle">✨</span>
                        <span>${card.badge}</span>
                    </div>
                ` : ''}
            </div>
        `;
        
        container.appendChild(codeWin);
    }

    // 3. RENDER POINTS CONTENT
    function renderPointsContent(container, card) {
        // Point cards can have a title
        if (card.title) {
            const title = document.createElement('h2');
            title.className = 'card-headline';
            title.style.fontSize = '26px';
            title.style.marginTop = '10px';
            title.textContent = card.title;
            container.appendChild(title);

            const underline = document.createElement('div');
            underline.className = 'headline-underline';
            underline.style.width = '100px';
            underline.style.height = '4px';
            container.appendChild(underline);
        }

        const list = document.createElement('div');
        list.className = 'points-list';

        const items = card.items || [];
        items.forEach(item => {
            const text = item.text || item;
            const mark = item.mark || 'dot';
            
            const cardItem = document.createElement('div');
            cardItem.className = 'points-item-card glass-card';
            
            let iconSvg = ICONS.play; // fallback
            if (mark === 'check') iconSvg = ICONS.check;
            else if (mark === 'cross') iconSvg = ICONS.cross;
            else if (mark === 'dot') iconSvg = ICONS.spark;
            else if (mark === 'num') iconSvg = `<span style="font-weight: 800; font-size: 12px;">#</span>`;

            cardItem.innerHTML = `
                <div class="point-indicator ${mark}">${iconSvg}</div>
                <span class="point-text">${text}</span>
            `;
            list.appendChild(cardItem);
        });

        container.appendChild(list);
    }

    // 4. RENDER STAT CONTENT
    function renderStatContent(container, card) {
        const statCard = document.createElement('div');
        statCard.className = 'stat-panel-card glass-card';
        
        statCard.innerHTML = `
            <div class="stat-value">${card.value}</div>
            ${card.label ? `<div class="stat-label">${card.label}</div>` : ''}
            ${card.note ? `<div class="stat-note">${card.note}</div>` : ''}
        `;

        // Render floating badges
        if (card.badges && card.badges.length > 0) {
            const badgeContainer = document.createElement('div');
            badgeContainer.className = 'stat-floating-badges';
            card.badges.forEach(badgeText => {
                const floatB = document.createElement('div');
                floatB.className = 'floating-badge';
                floatB.textContent = badgeText;
                badgeContainer.appendChild(floatB);
            });
            statCard.appendChild(badgeContainer);
        }

        container.appendChild(statCard);

        // Sub-metric chips under card
        if (card.chips && card.chips.length > 0) {
            const chipsRow = document.createElement('div');
            chipsRow.className = 'stat-sub-chips';
            card.chips.forEach(chipText => {
                const subChip = document.createElement('div');
                subChip.className = 'sub-chip glass-card';
                subChip.textContent = chipText;
                chipsRow.appendChild(subChip);
            });
            container.appendChild(chipsRow);
        }
    }

    // 5. RENDER SHOWCASE CONTENT
    function renderShowcaseContent(container, card, seed) {
        // Benchmark Chart (top)
        if (card.chart) {
            const chartArea = document.createElement('div');
            chartArea.className = 'showcase-chart-area glass-card';

            const title = document.createElement('div');
            title.className = 'chart-title';
            title.textContent = card.chart.title || 'Benchmark Comparison';
            chartArea.appendChild(title);

            const grid = document.createElement('div');
            grid.className = 'bar-chart-grid';

            const maxVal = card.chart.max || 100;
            const bars = card.chart.bars || [];
            
            bars.forEach(bar => {
                const val = bar.value || 0;
                const pct = Math.min(100, (val / maxVal) * 100);
                
                let theme = 'light';
                if (bar.highlight) theme = 'highlight';
                else if (bar.muted) theme = 'dark';
                else if (bar.color) theme = bar.color;

                const column = document.createElement('div');
                column.className = 'bar-column';
                column.innerHTML = `
                    <div class="bar-fill ${theme}" style="height: ${pct}%;">
                        <span class="bar-value">${val}%</span>
                    </div>
                    <span class="bar-label">${bar.label}</span>
                `;
                grid.appendChild(column);
            });
            chartArea.appendChild(grid);
            container.appendChild(chartArea);
        }

        // Solar System illustration (middle)
        const solarBand = document.createElement('div');
        solarBand.className = 'solar-system-band';
        
        // Orbital circles
        const o1 = document.createElement('div');
        o1.className = 'orbital-line orbit-1';
        const o2 = document.createElement('div');
        o2.className = 'orbital-line orbit-2';
        solarBand.appendChild(o1);
        solarBand.appendChild(o2);

        const bodies = card.bodies || ['Sol', 'Terra', 'Luna'];
        const bodySubs = card.body_subs || [];
        const bodiesKinds = ['sun', 'earth', 'moon'];

        bodies.forEach((body, idx) => {
            const celestial = document.createElement('div');
            celestial.className = 'celestial-body';
            celestial.innerHTML = `
                <div class="sphere ${bodiesKinds[idx]}"></div>
                <span class="sphere-name">${body}</span>
                ${bodySubs[idx] ? `<span class="sphere-sub">${bodySubs[idx]}</span>` : ''}
            `;
            solarBand.appendChild(celestial);
        });
        container.appendChild(solarBand);

        // Bold headline and subhead (bottom)
        if (card.headline && card.headline.length > 0) {
            const headline = document.createElement('h1');
            headline.className = 'card-headline';
            headline.style.fontSize = '26px';
            headline.innerHTML = card.headline.join('<br>');
            container.appendChild(headline);
        }

        if (card.subhead) {
            const subhead = document.createElement('p');
            subhead.className = 'card-subhead';
            subhead.style.fontSize = '14px';
            subhead.style.borderLeft = '3px solid var(--brand-blue)';
            subhead.style.paddingLeft = '10px';
            
            if (Array.isArray(card.subhead)) {
                subhead.innerHTML = card.subhead.join('<br>');
            } else {
                subhead.textContent = card.subhead;
            }
            container.appendChild(subhead);
        }
    }

    // 6. RENDER FEATURE CONTENT
    function renderFeatureContent(container, card, seed) {
        const mockup = card.mockup || {};
        const type = mockup.type || 'browser';

        const mockArea = document.createElement('div');
        mockArea.className = 'feature-mockup-area glass-card';

        if (type === 'browser') {
            const url = mockup.url || 'https://arnfar.com';
            mockArea.innerHTML = `
                <div class="code-titlebar">
                    <div class="traffic-lights">
                        <span class="light-dot red"></span>
                        <span class="light-dot yellow"></span>
                        <span class="light-dot green"></span>
                    </div>
                    <div class="code-filename">${url}</div>
                    <div style="width: 42px;"></div>
                </div>
                <div class="browser-content">
                    <div class="browser-mock-row" style="width: 60%;"></div>
                    <div class="browser-mock-row" style="width: 85%;"></div>
                    <div class="browser-mock-grid">
                        <div class="browser-mock-card glass-card">
                            <div class="browser-mock-row" style="height: 6px; background-color: var(--brand-blue);"></div>
                            <div class="browser-mock-row" style="height: 4px; width: 50%;"></div>
                        </div>
                        <div class="browser-mock-card glass-card">
                            <div class="browser-mock-row" style="height: 6px; background-color: var(--brand-green);"></div>
                            <div class="browser-mock-row" style="height: 4px; width: 60%;"></div>
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'video') {
            mockArea.innerHTML = `
                <div class="video-mock-container">
                    <div class="tag-pill normal" style="align-self: flex-start; font-size: 8px;">${mockup.tag || '1080p'}</div>
                    <div class="video-play-btn">${ICONS.play}</div>
                    <div>
                        <div class="video-timeline">
                            <div class="video-timeline-fill"></div>
                        </div>
                        <div class="video-time-label">${mockup.time || '0:00 / 1:00'}</div>
                    </div>
                </div>
            `;
        } else if (type === 'dashboard') {
            const tiles = mockup.tiles || [];
            let tilesHtml = '';
            tiles.forEach(tile => {
                tilesHtml += `
                    <div class="dash-mock-stat-tile glass-card">
                        <div class="dash-mock-value">${tile.value}</div>
                        <div class="dash-mock-label">${tile.label}</div>
                    </div>
                `;
            });
            mockArea.innerHTML = `
                <div class="browser-content">
                    <div class="dash-mock-grid">${tilesHtml}</div>
                    <div class="browser-mock-row" style="height: 30px; margin-top: 10px; background-color: rgba(255,255,255,0.03); border: 1px solid var(--glass-border); border-radius: 6px;"></div>
                </div>
            `;
        } else if (type === 'leaderboard') {
            const rows = mockup.rows || [];
            let rowsHtml = '';
            rows.forEach(row => {
                const hl = row.highlight ? 'highlight' : 'normal';
                rowsHtml += `
                    <div class="lead-mock-row ${hl}">
                        <span>${row.name}</span>
                        <strong>${row.value || ''}</strong>
                    </div>
                `;
            });
            mockArea.innerHTML = `
                <div class="browser-content" style="padding: 10px;">
                    <div style="font-size: 10px; font-weight: 700; color: var(--text-muted); margin-bottom: 6px;">${mockup.label || 'Rankings'}</div>
                    <div class="lead-mock-list">${rowsHtml}</div>
                </div>
            `;
        }

        container.appendChild(mockArea);

        // Feature chips grid (2-column layout)
        if (card.features && card.features.length > 0) {
            const chipsGrid = document.createElement('div');
            chipsGrid.className = 'feature-chips-grid';

            card.features.forEach(feat => {
                const chip = document.createElement('div');
                chip.className = 'feature-chip-card glass-card';
                
                const iconName = feat.icon || 'spark';
                const iconSvg = ICONS[iconName] || ICONS.spark;

                chip.innerHTML = `
                    <div class="feature-icon-box">${iconSvg}</div>
                    <span class="feature-text">${feat.text}</span>
                `;
                chipsGrid.appendChild(chip);
            });
            container.appendChild(chipsGrid);
        }
    }

    // 7. RENDER STACK CONTENT
    function renderStackContent(container, card) {
        // Point cards can have a title
        if (card.title) {
            const title = document.createElement('h2');
            title.className = 'card-headline';
            title.style.fontSize = '26px';
            title.style.marginTop = '10px';
            title.textContent = card.title;
            container.appendChild(title);

            const underline = document.createElement('div');
            underline.className = 'headline-underline';
            underline.style.width = '100px';
            underline.style.height = '4px';
            container.appendChild(underline);
        }

        const list = document.createElement('div');
        list.className = 'stack-list';

        const tools = card.tools || [];
        tools.forEach(tool => {
            const name = tool.name || tool;
            const role = tool.role || '';
            const iconName = tool.icon || 'spark';
            const iconSvg = ICONS[iconName] || ICONS.spark;

            const cardItem = document.createElement('div');
            cardItem.className = 'stack-item-card glass-card';

            cardItem.innerHTML = `
                <div class="point-indicator num">${iconSvg}</div>
                <div style="display: flex; flex-direction: column;">
                    <span class="stack-item-title">${name}</span>
                    ${role ? `<span class="stack-item-role">${role}</span>` : ''}
                </div>
            `;
            list.appendChild(cardItem);
        });

        container.appendChild(list);
    }
});
