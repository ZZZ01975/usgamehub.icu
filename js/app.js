// US Game Hub - 主应用程序

// DOM加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    console.log('US Game Hub 初始化开始...');
    
    // 初始化通用功能
    initializeApp();
    
    // 根据当前页面初始化相应功能
    const path = window.location.pathname;
    
    if (path === '/' || path.endsWith('/index.html')) {
        // 首页
        GameManager.initHomePage();
    } else if (path.endsWith('/game.html')) {
        // 游戏详情页
        const gameId = Utils.getUrlParameter('id');
        if (gameId) {
            GameManager.loadGamePage(gameId);
            initGamePage();
        }
    } else if (path.endsWith('/category.html')) {
        // 分类页
        const categoryId = Utils.getUrlParameter('cat');
        const sortBy = Utils.getUrlParameter('sort') || 'popular';
        if (categoryId) {
            GameManager.loadCategoryPage(categoryId, sortBy);
            initCategoryPage();
        }
    }
});

// 应用程序通用初始化
function initializeApp() {
    // 初始化移动端导航
    initMobileNavigation();
    
    // 初始化语言切换
    initLanguageToggle();
    
    // 初始化Cookie提示
    initCookieNotice();
    
    // 初始化全屏功能
    initFullscreenButtons();
    
    // 初始化分享功能
    initSocialShare();
    
    // 初始化懒加载
    Utils.lazyLoadImages();
    
    // 监听窗口大小变化
    window.addEventListener('resize', Utils.throttle(handleResize, 250));
    
    console.log('通用功能初始化完成');
}

// 移动端导航初始化
function initMobileNavigation() {
    const mobileToggle = document.querySelector('.mobile-toggle');
    const navList = document.querySelector('.nav-list');
    
    if (!mobileToggle || !navList) return;
    
    mobileToggle.addEventListener('click', function() {
        navList.classList.toggle('active');
        
        // 切换hamburger动画
        const lines = mobileToggle.querySelectorAll('.hamburger-line');
        lines.forEach((line, index) => {
            line.style.transform = navList.classList.contains('active') 
                ? `rotate(${index === 0 ? '45' : index === 2 ? '-45' : '0'}deg) translate(${index === 1 ? '100%' : '0'}, ${index === 0 ? '8px' : index === 2 ? '-8px' : '0'})`
                : 'none';
            line.style.opacity = navList.classList.contains('active') && index === 1 ? '0' : '1';
        });
    });
    
    // 点击外部关闭菜单
    document.addEventListener('click', function(e) {
        if (!mobileToggle.contains(e.target) && !navList.contains(e.target)) {
            navList.classList.remove('active');
        }
    });
}

// 语言切换功能
function initLanguageToggle() {
    const langToggle = document.querySelector('.lang-toggle');
    if (!langToggle) return;
    
    langToggle.addEventListener('click', function() {
        const currentLang = window.i18n.getCurrentLanguage();
        const newLang = currentLang === 'en' ? 'zh' : 'en';
        window.i18n.setLanguage(newLang);
    });
}

// Cookie提示初始化
function initCookieNotice() {
    const cookieNotice = document.getElementById('cookieNotice');
    const acceptBtn = document.getElementById('acceptCookies');
    
    if (!cookieNotice || !acceptBtn) return;
    
    // 检查用户是否已接受Cookie
    const cookieAccepted = Utils.Storage.get('cookieAccepted');
    
    if (!cookieAccepted) {
        // 延迟显示Cookie提示
        setTimeout(() => {
            cookieNotice.classList.add('show');
        }, 2000);
    }
    
    acceptBtn.addEventListener('click', function() {
        Utils.Storage.set('cookieAccepted', true);
        cookieNotice.classList.remove('show');
        
        setTimeout(() => {
            cookieNotice.style.display = 'none';
        }, 300);
    });
}

// 全屏功能初始化
function initFullscreenButtons() {
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-fullscreen') || 
            e.target.closest('.btn-fullscreen')) {
            e.preventDefault();
            
            const gameIframe = document.getElementById('gameIframe');
            if (gameIframe) {
                toggleFullscreen(gameIframe);
            }
        }
    });
}

// 切换全屏
function toggleFullscreen(element) {
    if (!document.fullscreenElement) {
        element.requestFullscreen().catch(err => {
            console.log('无法进入全屏模式:', err);
        });
    } else {
        document.exitFullscreen();
    }
}

// 社交分享功能
function initSocialShare() {
    document.addEventListener('click', function(e) {
        const shareBtn = e.target.closest('.share-btn');
        if (!shareBtn) return;
        
        e.preventDefault();
        
        const url = window.location.href;
        const title = document.title;
        
        if (shareBtn.classList.contains('facebook')) {
            shareOnFacebook(url, title);
        } else if (shareBtn.classList.contains('twitter')) {
            shareOnTwitter(url, title);
        } else if (shareBtn.classList.contains('copy')) {
            copyLinkToClipboard(url);
        }
    });
}

// Facebook分享
function shareOnFacebook(url, title) {
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
    openShareWindow(shareUrl);
}

// Twitter分享
function shareOnTwitter(url, title) {
    const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
    openShareWindow(shareUrl);
}

// 复制链接
async function copyLinkToClipboard(url) {
    try {
        await Utils.copyToClipboard(url);
        showMessage('Link copied to clipboard!');
    } catch (err) {
        console.error('复制失败:', err);
        showMessage('Copy failed, please copy the link manually');
    }
}

// 打开分享窗口
function openShareWindow(url) {
    const width = 600;
    const height = 400;
    const left = (window.screen.width / 2) - (width / 2);
    const top = (window.screen.height / 2) - (height / 2);
    
    window.open(
        url,
        'share',
        `width=${width},height=${height},left=${left},top=${top},resizable=yes,scrollbars=yes`
    );
}

// 游戏页面特定初始化
function initGamePage() {
    // 初始化评分系统
    initRatingSystem();
    
    // 初始化评论功能
    initCommentSystem();
    
    // 监听游戏加载状态
    monitorGameLoading();
}

// 评分系统
function initRatingSystem() {
    const stars = document.querySelectorAll('.rating-input .star');
    
    stars.forEach((star, index) => {
        star.addEventListener('click', function() {
            const gameId = Utils.getUrlParameter('id');
            const rating = index + 1;
            
            // 这里应该发送到服务器
            console.log(`用户评分 ${gameId}: ${rating} 星`);
            
            // 更新本地存储
            const ratings = Utils.Storage.get('gameRatings') || {};
            ratings[gameId] = rating;
            Utils.Storage.set('gameRatings', ratings);
            
            // 更新UI
            updateRatingDisplay(rating);
            showMessage(`Thanks for your ${rating} star rating!`);
        });
        
        star.addEventListener('mouseover', function() {
            highlightStars(index + 1);
        });
    });
}

// 更新评分显示
function updateRatingDisplay(rating) {
    const stars = document.querySelectorAll('.rating-input .star');
    stars.forEach((star, index) => {
        star.classList.toggle('active', index < rating);
    });
}

// 高亮星星
function highlightStars(count) {
    const stars = document.querySelectorAll('.rating-input .star');
    stars.forEach((star, index) => {
        star.classList.toggle('hover', index < count);
    });
}

// 评论系统
function initCommentSystem() {
    const commentForm = document.querySelector('.comment-form');
    const commentInput = document.querySelector('.comment-input');
    const submitBtn = document.querySelector('.comment-submit');
    
    if (!commentForm) return;
    
    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const comment = commentInput.value.trim();
        if (!comment) return;
        
        const gameId = Utils.getUrlParameter('id');
        
        // 创建评论对象
        const commentObj = {
            id: Date.now(),
            gameId: gameId,
            text: comment,
            author: '匿名用户',
            timestamp: new Date().toISOString()
        };
        
        // 保存到本地存储（实际项目中应该发送到服务器）
        const comments = Utils.Storage.get('gameComments') || [];
        comments.unshift(commentObj);
        Utils.Storage.set('gameComments', comments);
        
        // 添加到页面
        addCommentToPage(commentObj);
        
        // 清空表单
        commentInput.value = '';
        showMessage('Comment posted successfully!');
    });
}

// 添加评论到页面
function addCommentToPage(comment) {
    const commentsList = document.getElementById('commentsList');
    if (!commentsList) return;
    
    const commentHtml = `
        <div class="comment-item">
            <div class="comment-author">${comment.author}</div>
            <div class="comment-text">${comment.text}</div>
            <div class="comment-date">${Utils.formatDate(comment.timestamp)}</div>
        </div>
    `;
    
    commentsList.insertAdjacentHTML('afterbegin', commentHtml);
}

// 监控游戏加载
function monitorGameLoading() {
    const iframe = document.getElementById('gameIframe');
    const loading = document.getElementById('gameLoading');
    
    if (!iframe || !loading) return;
    
    let loadTimeout = setTimeout(() => {
        loading.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
            </div>
            <p>游戏加载时间较长，请耐心等待...</p>
        `;
    }, 10000); // 10秒后显示加载慢的提示
    
    iframe.onload = () => {
        clearTimeout(loadTimeout);
    };
}

// 分类页面初始化
function initCategoryPage() {
    // 初始化排序功能
    initSorting();
    
    // 初始化视图切换
    initViewToggle();
    
    // 初始化加载更多
    initLoadMore();
}

// 排序功能
function initSorting() {
    const sortSelect = document.getElementById('sortSelect');
    if (!sortSelect) return;
    
    sortSelect.addEventListener('change', function() {
        const categoryId = Utils.getUrlParameter('cat');
        const sortBy = this.value;
        
        if (categoryId) {
            GameManager.loadCategoryGames(categoryId, sortBy);
            
            // 更新URL但不刷新页面
            const newUrl = `${window.location.pathname}?cat=${categoryId}&sort=${sortBy}`;
            history.pushState(null, '', newUrl);
        }
    });
}

// 视图切换
function initViewToggle() {
    const viewBtns = document.querySelectorAll('.view-btn');
    const gamesGrid = document.getElementById('categoryGamesGrid');
    
    if (!gamesGrid) return;
    
    viewBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            viewBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            const view = this.dataset.view;
            gamesGrid.className = view === 'list' ? 'games-grid list-view' : 'games-grid';
        });
    });
}

// 加载更多功能
function initLoadMore() {
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    if (!loadMoreBtn) return;
    
    let currentPage = 1;
    const gamesPerPage = 12;
    
    loadMoreBtn.addEventListener('click', function() {
        const categoryId = Utils.getUrlParameter('cat');
        if (!categoryId) return;
        
        this.classList.add('loading');
        this.disabled = true;
        
        // 模拟加载延迟
        setTimeout(() => {
            const allGames = GameManager.getGamesByCategory(categoryId);
            const startIndex = currentPage * gamesPerPage;
            const endIndex = startIndex + gamesPerPage;
            const nextGames = allGames.slice(startIndex, endIndex);
            
            if (nextGames.length > 0) {
                const gamesGrid = document.getElementById('categoryGamesGrid');
                nextGames.forEach(game => {
                    gamesGrid.insertAdjacentHTML('beforeend', Utils.createGameCard(game));
                });
                
                currentPage++;
            }
            
            // 如果没有更多游戏了，隐藏按钮
            if (endIndex >= allGames.length) {
                this.style.display = 'none';
            }
            
            this.classList.remove('loading');
            this.disabled = false;
        }, 1000);
    });
}

// 窗口大小变化处理
function handleResize() {
    // 更新轮播图尺寸
    const carousel = document.querySelector('.featured-carousel');
    if (carousel) {
        // 触发轮播重新计算
        carousel.style.height = 'auto';
    }
    
    // 更新网格布局
    const grids = document.querySelectorAll('.games-grid, .categories-grid');
    grids.forEach(grid => {
        // 触发CSS重新计算
        grid.style.display = 'none';
        grid.offsetHeight; // 强制重排
        grid.style.display = '';
    });
}

// 显示消息提示
function showMessage(message, type = 'success') {
    // 创建消息元素
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${type}`;
    messageEl.textContent = message;
    
    // 添加样式
    Object.assign(messageEl.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: type === 'success' ? '#4CAF50' : '#f44336',
        color: 'white',
        padding: '12px 20px',
        borderRadius: '4px',
        zIndex: '10000',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    document.body.appendChild(messageEl);
    
    // 显示动画
    setTimeout(() => {
        messageEl.style.transform = 'translateX(0)';
    }, 100);
    
    // 自动隐藏
    setTimeout(() => {
        messageEl.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(messageEl);
        }, 300);
    }, 3000);
}

// 错误处理
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showMessage('An error occurred, please refresh and try again', 'error');
});

// 未处理的Promise错误
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled Promise Rejection:', e.reason);
    showMessage('Data loading failed, please try again later', 'error');
});

console.log('App.js 加载完成');