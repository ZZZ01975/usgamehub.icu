// US Game Hub - 工具函数库

// 获取URL参数
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// 格式化数字（如播放次数）
function formatNumber(num) {
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
}

// 生成星级评分HTML
function generateStars(rating) {
    let starsHtml = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(rating)) {
            starsHtml += '<span class="star">★</span>';
        } else if (i - 0.5 <= rating) {
            starsHtml += '<span class="star">☆</span>';
        } else {
            starsHtml += '<span class="star empty">☆</span>';
        }
    }
    return starsHtml;
}

// 创建游戏卡片HTML
function createGameCard(game) {
    return `
        <a href="/game.html?id=${game.id}" class="game-card" data-game-id="${game.id}">
            <div class="game-thumbnail">
                <div class="game-placeholder" style="
                    width: 100%; 
                    height: 200px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    flex-direction: column;
                    color: white;
                    position: relative;
                ">
                    <!-- Dark overlay for better text contrast -->
                    <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.4);"></div>
                    <div class="category-icon-display" style="font-size: 3rem; margin-bottom: 0.5rem; position: relative; z-index: 1; transition: opacity 0.3s ease;">${getCategoryIcon(game.category)}</div>
                    <div style="font-size: 0.9rem; font-weight: 600; position: relative; z-index: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8); transition: opacity 0.3s ease;" data-i18n="game.clickToPlay">Click to Play</div>
                </div>
                <div class="game-overlay" style="z-index: 10;">
                    <button class="play-btn" style="position: relative; z-index: 11;" data-i18n="buttons.startGame">▶ Start Game</button>
                </div>
            </div>
            <div class="game-info">
                <h3 class="game-title">${game.title}</h3>
                <p class="game-description">${game.shortDesc}</p>
                <div class="game-meta">
                    <div class="game-rating">
                        <div class="stars">${generateStars(game.rating)}</div>
                        <span class="rating-text">${game.rating}</span>
                    </div>
                    <span class="game-category">${getCategoryName(game.category)}</span>
                </div>
                <div class="game-tags">
                    ${game.tags && game.tags.length > 0 ? 
                        game.tags.slice(0, 3).map(tag => tag.trim() ? `<span class="game-tag">${tag}</span>` : '').join('') 
                        : '<span class="game-tag">New Game</span>'}
                </div>
            </div>
        </a>
    `;
}

// 创建分类卡片HTML
function createCategoryCard(category) {
    const gameCount = window.gamesData ? 
        window.gamesData.games.filter(game => game.category === category.id).length : 0;
    
    // 使用英文数据或i18n翻译
    const categoryName = window.i18n ? 
        window.i18n.t(`categories.${category.id}`) : 
        (category.nameEn || category.name);
    const categoryDesc = window.i18n ? 
        window.i18n.t(`categoryDesc.${category.id}`) : 
        (category.descriptionEn || category.description);
    
    return `
        <a href="/category.html?cat=${category.id}" class="category-card">
            <div class="category-icon">${getCategoryIcon(category.id)}</div>
            <h3 class="category-name">${categoryName}</h3>
            <p class="category-description">${categoryDesc}</p>
            <span class="category-count">${gameCount} <span data-i18n="categoryPage.games">games</span></span>
        </a>
    `;
}

// 获取分类名称
function getCategoryName(categoryId) {
    if (window.i18n) {
        return window.i18n.t(`categories.${categoryId}`);
    }
    const categoryNames = {
        'puzzle': 'Puzzle Games',
        'action': 'Action Games',
        'multiplayer': 'Multiplayer Games',
        'cards': 'Card Games',
        'sports': 'Sports Games',
        'strategy': 'Strategy Games'
    };
    return categoryNames[categoryId] || categoryId;
}

// 获取分类图标
function getCategoryIcon(categoryId) {
    const categoryIcons = {
        'puzzle': '🧩',
        'action': '⚡',
        'multiplayer': '👥',
        'cards': '🃏',
        'sports': '⚽',
        'strategy': '🎯'
    };
    return categoryIcons[categoryId] || '🎮';
}

// 显示加载动画
function showLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.add('active');
    }
}

// 隐藏加载动画
function hideLoading() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.classList.remove('active');
    }
}

// 错误处理
function showError(message) {
    console.error('Error:', message);
    // 可以在这里添加用户友好的错误提示
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 节流函数
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// 懒加载图片
function lazyLoadImages() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

// 本地存储操作
const Storage = {
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error getting from localStorage:', e);
            return null;
        }
    },
    
    set: function(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Error setting to localStorage:', e);
            return false;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
            return true;
        } catch (e) {
            console.error('Error removing from localStorage:', e);
            return false;
        }
    }
};

// 设备检测
const Device = {
    isMobile: function() {
        return window.innerWidth <= 768;
    },
    
    isTablet: function() {
        return window.innerWidth > 768 && window.innerWidth <= 1024;
    },
    
    isDesktop: function() {
        return window.innerWidth > 1024;
    },
    
    hasTouch: function() {
        return 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    }
};

// 平滑滚动到元素
function scrollToElement(element, offset = 0) {
    const targetPosition = element.offsetTop - offset;
    window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
    });
}

// 复制到剪贴板
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        return true;
    } catch (err) {
        // 回退方案
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        document.execCommand('copy');
        document.body.removeChild(textArea);
        return true;
    }
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) {
        return window.i18n ? window.i18n.t('time.yesterday') : 'yesterday';
    } else if (diffDays < 7) {
        const daysText = window.i18n ? window.i18n.t('time.daysAgo') : 'days ago';
        return `${diffDays} ${daysText}`;
    } else if (diffDays < 30) {
        const weeksText = window.i18n ? window.i18n.t('time.weeksAgo') : 'weeks ago';
        return `${Math.floor(diffDays / 7)} ${weeksText}`;
    } else {
        const lang = window.i18n ? window.i18n.getCurrentLanguage() : 'en';
        return date.toLocaleDateString(lang === 'zh' ? 'zh-CN' : 'en-US');
    }
}

// 导出到全局
window.Utils = {
    getUrlParameter,
    formatNumber,
    generateStars,
    createGameCard,
    createCategoryCard,
    getCategoryName,
    getCategoryIcon,
    showLoading,
    hideLoading,
    showError,
    debounce,
    throttle,
    lazyLoadImages,
    Storage,
    Device,
    scrollToElement,
    copyToClipboard,
    formatDate
};