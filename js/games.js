// US Game Hub - Game Data Management and Functions

// Global game data
window.gamesData = null;
window.categoriesData = null;

// Data loading function
async function loadGameData() {
    try {
        showLoading();
        
        // Load game data and category data in parallel
        const [gamesResponse, categoriesResponse] = await Promise.all([
            fetch('/data/games.json'),
            fetch('/data/categories.json')
        ]);
        
        if (!gamesResponse.ok || !categoriesResponse.ok) {
            throw new Error('Failed to load data');
        }
        
        window.gamesData = await gamesResponse.json();
        window.categoriesData = await categoriesResponse.json();
        
        console.log('Data loaded successfully:', {
            games: window.gamesData.totalCount,
            categories: window.categoriesData.totalCategories
        });
        
        return { games: window.gamesData, categories: window.categoriesData };
        
    } catch (error) {
        console.error('Data loading failed:', error);
        showError('Game data loading failed, please refresh the page');
        throw error;
    } finally {
        hideLoading();
    }
}

// 根据分类获取游戏
function getGamesByCategory(categoryId, limit = null) {
    if (!window.gamesData) return [];
    
    const games = window.gamesData.games.filter(game => game.category === categoryId);
    return limit ? games.slice(0, limit) : games;
}

// 获取热门游戏
function getFeaturedGames(limit = 5) {
    if (!window.gamesData) return [];
    
    return window.gamesData.games
        .filter(game => game.featured)
        .slice(0, limit);
}

// 获取最新游戏
function getNewestGames(limit = 8) {
    if (!window.gamesData) return [];
    
    return window.gamesData.games
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
        .slice(0, limit);
}

// 获取热门游戏（按播放次数）
function getPopularGames(limit = 12) {
    if (!window.gamesData) return [];
    
    return window.gamesData.games
        .sort((a, b) => b.playCount - a.playCount)
        .slice(0, limit);
}

// 根据ID获取单个游戏
function getGameById(gameId) {
    if (!window.gamesData) return null;
    
    return window.gamesData.games.find(game => game.id === gameId);
}

// 根据关键词搜索游戏
function searchGames(query, limit = 20) {
    if (!window.gamesData || !query) return [];
    
    const searchTerm = query.toLowerCase();
    
    return window.gamesData.games.filter(game => {
        return game.title.toLowerCase().includes(searchTerm) ||
               game.description.toLowerCase().includes(searchTerm) ||
               game.keywords.some(keyword => keyword.toLowerCase().includes(searchTerm)) ||
               game.tags.some(tag => tag.toLowerCase().includes(searchTerm));
    }).slice(0, limit);
}

// 获取相关游戏推荐
function getRelatedGames(gameId, limit = 8) {
    if (!window.gamesData) return [];
    
    const currentGame = getGameById(gameId);
    if (!currentGame) return [];
    
    // 优先推荐同分类游戏
    const sameCategory = window.gamesData.games.filter(game => 
        game.id !== gameId && game.category === currentGame.category
    );
    
    // 如果同分类游戏不够，添加其他热门游戏
    if (sameCategory.length < limit) {
        const otherGames = window.gamesData.games
            .filter(game => game.id !== gameId && game.category !== currentGame.category)
            .sort((a, b) => b.playCount - a.playCount);
        
        return [...sameCategory, ...otherGames].slice(0, limit);
    }
    
    return sameCategory.slice(0, limit);
}

// 增加游戏播放次数
function incrementPlayCount(gameId) {
    const game = getGameById(gameId);
    if (game) {
        game.playCount += 1;
        
        // 记录到本地存储（实际项目中应该发送到服务器）
        const playHistory = Storage.get('playHistory') || {};
        playHistory[gameId] = (playHistory[gameId] || 0) + 1;
        Storage.set('playHistory', playHistory);
    }
}

// Get game tag cloud data
function getTagsCloud(limit = 30) {
    if (!window.gamesData) return [];
    
    const tagCount = {};
    
    // 统计所有标签的使用次数
    window.gamesData.games.forEach(game => {
        game.tags.forEach(tag => {
            tagCount[tag] = (tagCount[tag] || 0) + 1;
        });
    });
    
    // 按使用次数排序并返回前N个
    return Object.entries(tagCount)
        .sort(([,a], [,b]) => b - a)
        .slice(0, limit)
        .map(([tag, count]) => ({ tag, count }));
}

// Homepage data initialization
async function initHomePage() {
    try {
        await loadGameData();
        
        // 渲染轮播图
        renderFeaturedCarousel();
        
        // 渲染分类网格
        renderCategoriesGrid();
        
        // 渲染最新游戏
        renderNewestGames();
        
        // 渲染热门游戏
        renderPopularGames();
        
        // 渲染标签云
        renderTagsCloud();
        
        // 初始化搜索功能
        initSearch();
        
    } catch (error) {
        console.error('Homepage initialization failed:', error);
    }
}

// 渲染轮播图
function renderFeaturedCarousel() {
    const container = document.getElementById('featuredCarousel');
    const indicators = document.getElementById('carouselIndicators');
    
    if (!container || !indicators) return;
    
    const featuredGames = getFeaturedGames(5);
    
    // 确保有足够的热门游戏
    if (featuredGames.length === 0) {
        console.warn('No featured games found');
        return;
    }
    
    // 为每个游戏创建不同的渐变色
    const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
    ];
    
    container.innerHTML = featuredGames.map((game, index) => `
        <div class="carousel-item ${index === 0 ? 'active' : ''}" data-slide="${index}">
            <div class="carousel-bg" style="background: ${gradients[index % gradients.length]}; width: 100%; height: 100%; position: absolute; top: 0; left: 0;"></div>
            <div class="game-icon" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4rem; color: white; opacity: 0.4;">${getCategoryIcon(game.category)}</div>
            <div class="carousel-content">
                <h3 class="carousel-title">${game.title}</h3>
                <p>${game.shortDesc}</p>
                <a href="/game.html?id=${game.id}" class="btn btn-primary" data-i18n="buttons.playNow">🎮 Play Now</a>
            </div>
        </div>
    `).join('');
    
    indicators.innerHTML = featuredGames.map((_, index) => `
        <span class="indicator ${index === 0 ? 'active' : ''}" data-slide="${index}"></span>
    `).join('');
    
    console.log('轮播图渲染完成，游戏数量:', featuredGames.length);
    console.log('Featured games:', featuredGames.map(g => g.title));
    
    // 延迟初始化轮播，确保DOM已完全渲染
    setTimeout(() => {
        initCarousel();
        // 更新新添加元素的翻译
        if (window.i18n) {
            window.i18n.updateAllTexts();
        }
    }, 100);
}

// 初始化轮播功能
function initCarousel() {
    let currentSlide = 0;
    const slides = document.querySelectorAll('.carousel-item');
    const indicators = document.querySelectorAll('.indicator');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');
    
    console.log('初始化轮播，幻灯片数量:', slides.length);
    
    if (slides.length === 0) {
        console.warn('没有找到轮播项');
        return;
    }
    
    if (slides.length === 1) {
        console.log('只有一个轮播项，跳过轮播功能');
        return;
    }
    
    function showSlide(index) {
        // 移除所有active类
        slides.forEach((slide, i) => {
            slide.classList.remove('active');
            if (indicators[i]) {
                indicators[i].classList.remove('active');
            }
        });
        
        // 添加active类到当前幻灯片
        if (slides[index]) {
            slides[index].classList.add('active');
        }
        if (indicators[index]) {
            indicators[index].classList.add('active');
        }
        
        currentSlide = index;
        console.log('显示幻灯片:', index);
    }
    
    function nextSlide() {
        const next = (currentSlide + 1) % slides.length;
        showSlide(next);
    }
    
    function prevSlide() {
        const prev = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(prev);
    }
    
    // 确保第一张幻灯片是激活的
    showSlide(0);
    
    // 事件监听
    if (nextBtn) {
        nextBtn.addEventListener('click', (e) => {
            e.preventDefault();
            nextSlide();
        });
    }
    
    if (prevBtn) {
        prevBtn.addEventListener('click', (e) => {
            e.preventDefault();
            prevSlide();
        });
    }
    
    indicators.forEach((indicator, index) => {
        indicator.addEventListener('click', (e) => {
            e.preventDefault();
            showSlide(index);
        });
    });
    
    // 自动播放 - 只有多于1张时才自动播放
    if (slides.length > 1) {
        setInterval(nextSlide, 5000);
        console.log('启动自动播放，5秒切换');
    }
}

// 渲染分类网格
function renderCategoriesGrid() {
    const container = document.getElementById('categoriesGrid');
    if (!container || !window.categoriesData) return;
    
    container.innerHTML = window.categoriesData.categories.map(createCategoryCard).join('');
    
    // 更新新添加元素的翻译
    if (window.i18n) {
        window.i18n.updateAllTexts();
    }
}

// 渲染最新游戏
function renderNewestGames() {
    const container = document.getElementById('newGamesGrid');
    if (!container) return;
    
    const newestGames = getNewestGames(8);
    container.innerHTML = newestGames.map(createGameCard).join('');
    
    // 更新新添加元素的翻译
    if (window.i18n) {
        window.i18n.updateAllTexts();
    }
}

// 渲染热门游戏
function renderPopularGames() {
    const container = document.getElementById('popularGamesGrid');
    if (!container) return;
    
    const popularGames = getPopularGames(12);
    container.innerHTML = popularGames.map(createGameCard).join('');
    
    // 更新新添加元素的翻译
    if (window.i18n) {
        window.i18n.updateAllTexts();
    }
}

// 渲染标签云
function renderTagsCloud() {
    const container = document.getElementById('tagsCloud');
    if (!container) return;
    
    const tags = getTagsCloud(20);
    container.innerHTML = tags.map(({ tag, count }) => `
        <a href="/search.html?q=${encodeURIComponent(tag)}" class="tag-item" style="font-size: ${Math.min(1.5, 0.8 + count * 0.1)}rem;">
            ${tag} <small>(${count})</small>
        </a>
    `).join('');
}

// 初始化搜索功能
function initSearch() {
    const searchForm = document.querySelector('.search-form');
    const searchInput = document.querySelector('.search-input');
    
    if (!searchForm || !searchInput) return;
    
    // 搜索提交
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = searchInput.value.trim();
        if (query) {
            window.location.href = `/search.html?q=${encodeURIComponent(query)}`;
        }
    });
    
    // 实时搜索建议（可选）
    const debouncedSearch = debounce((query) => {
        if (query.length >= 2) {
            // 这里可以显示搜索建议
            console.log('Search suggestions for:', query);
        }
    }, 300);
    
    searchInput.addEventListener('input', (e) => {
        debouncedSearch(e.target.value);
    });
}

// 游戏页面初始化
async function loadGamePage(gameId) {
    try {
        await loadGameData();
        
        const game = getGameById(gameId);
        if (!game) {
            showError('游戏未找到');
            return;
        }
        
        // 更新页面元素
        updateGamePageContent(game);
        
        // Load related games
        loadRelatedGames(gameId);
        
        // 增加播放次数
        incrementPlayCount(gameId);
        
    } catch (error) {
        console.error('Game page loading failed:', error);
        showError('Game loading failed, please refresh the page');
    }
}

// 更新游戏页面内容
function updateGamePageContent(game) {
    // 更新页面标题和meta信息
    document.title = `${game.title} | US Game Hub`;
    
    const metaDescription = document.getElementById('gameDescription');
    const metaKeywords = document.getElementById('gameKeywords');
    
    if (metaDescription) metaDescription.content = game.description;
    if (metaKeywords) metaKeywords.content = game.keywords.join(', ');
    
    // 更新页面内容
    const elements = {
        gamePageTitle: game.title,
        gameStars: generateStars(game.rating),
        ratingText: game.rating,
        playCount: `${formatNumber(game.playCount)} plays`,
        gameCategory: getCategoryName(game.category),
        gameDescriptionText: game.description,
        gameTips: getGameTipsInEnglish(game),
        controlsText: getGameControlsInEnglish(game)
    };
    
    Object.entries(elements).forEach(([id, content]) => {
        const element = document.getElementById(id);
        if (element) {
            element.innerHTML = content;
        }
    });
    
    // 更新游戏标签
    const tagsContainer = document.getElementById('gameTags');
    if (tagsContainer) {
        tagsContainer.innerHTML = game.tags.map(tag => 
            `<span class="game-tag">${tag}</span>`
        ).join('');
    }
    
    // 更新面包屑导航
    updateBreadcrumb(game);
    
    // Load game iframe
    loadGameIframe(game);
}

// Load game iframe
function loadGameIframe(game) {
    const iframe = document.getElementById('gameIframe');
    const loading = document.getElementById('gameLoading');
    
    if (!iframe) return;
    
    // 设置iframe属性
    iframe.src = game.iframeUrl;
    iframe.setAttribute('sandbox', 'allow-scripts allow-same-origin allow-forms allow-pointer-lock allow-orientation-lock allow-presentation');
    
    // Set loading timeout
    const timeout = setTimeout(() => {
        if (loading && !loading.classList.contains('hidden')) {
            showGameLoadingError(game, loading, 'timeout');
        }
    }, 8000);
    
    iframe.onload = () => {
        clearTimeout(timeout);
        if (loading) {
            loading.classList.add('hidden');
        }
        console.log('Game loaded successfully:', game.title);
        
        // Record game start event
        if (window.GameAnalytics) {
            GameAnalytics.startGameSession(game.id);
        }
    };
    
    iframe.onerror = () => {
        clearTimeout(timeout);
        if (loading) {
            showGameLoadingError(game, loading, 'error');
        }
        console.warn('Game loading failed:', game.title, game.iframeUrl);
    };
}

// Show game loading error with fallback options
function showGameLoadingError(game, loadingElement, errorType) {
    const errorMessages = {
        timeout: {
            title: '⏰ Game Loading Timeout',
            message: 'The game is taking too long to load. This may be due to network issues or the game server being busy.'
        },
        error: {
            title: '❌ Game Loading Failed', 
            message: 'Unable to load this game. It may not support embedded playback or is temporarily unavailable.'
        }
    };
    
    const error = errorMessages[errorType] || errorMessages.error;
    const relatedGames = getRelatedGames(game.id, 3);
    const alternativeGamesHTML = relatedGames.length > 0 ? `
        <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
            <h4 style="margin-bottom: 15px; color: #fbbf24;">🎯 Try Similar Games Instead:</h4>
            <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
                ${relatedGames.slice(0, 3).map(relatedGame => `
                    <a href="/game.html?id=${relatedGame.id}" class="btn btn-outline" style="font-size: 0.85rem; padding: 8px 12px;">
                        🎮 ${relatedGame.title.length > 15 ? relatedGame.title.substring(0, 15) + '...' : relatedGame.title}
                    </a>
                `).join('')}
            </div>
        </div>
    ` : '';
    
    loadingElement.innerHTML = `
        <div class="game-error" style="text-align: center; color: white; padding: 40px; max-width: 600px; margin: 0 auto;">
            <h3 style="margin-bottom: 15px; font-size: 1.4rem;">${error.title}</h3>
            <p style="margin-bottom: 25px; line-height: 1.5; opacity: 0.9;">${error.message}</p>
            
            <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 15px;">
                <a href="${game.iframeUrl}" target="_blank" class="btn btn-primary" style="font-size: 0.9rem;">
                    🔗 Open Original Game
                </a>
                <button onclick="location.reload()" class="btn btn-outline" style="font-size: 0.9rem;">
                    🔄 Reload Page
                </button>
                <button onclick="history.back()" class="btn btn-outline" style="font-size: 0.9rem;">
                    ⬅️ Go Back
                </button>
            </div>
            
            ${alternativeGamesHTML}
            
            <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <small style="opacity: 0.8; line-height: 1.4;">
                    💡 <strong>Tip:</strong> Some games work better when opened in a new window due to security restrictions.
                    <br>You can also try the alternative games suggested above!
                </small>
            </div>
        </div>
    `;
    
    // Update translations if available
    if (window.i18n) {
        window.i18n.updateAllTexts();
    }
}

// Load related games
function loadRelatedGames(gameId) {
    const container = document.getElementById('relatedGamesGrid');
    if (!container) return;
    
    const relatedGames = getRelatedGames(gameId, 8);
    container.innerHTML = relatedGames.map(createGameCard).join('');
}

// 更新面包屑导航
function updateBreadcrumb(game) {
    const categoryBreadcrumb = document.getElementById('categoryBreadcrumb');
    const gameBreadcrumb = document.getElementById('gameBreadcrumb');
    
    if (categoryBreadcrumb) {
        categoryBreadcrumb.textContent = getCategoryName(game.category);
        categoryBreadcrumb.href = `/category.html?cat=${game.category}`;
    }
    
    if (gameBreadcrumb) {
        gameBreadcrumb.textContent = game.title;
    }
}

// 分类页面初始化
async function loadCategoryPage(categoryId, sortBy = 'popular') {
    try {
        await loadGameData();
        
        const category = window.categoriesData.categories.find(cat => cat.id === categoryId);
        if (!category) {
            showError('分类未找到');
            return;
        }
        
        // 更新页面内容
        updateCategoryPageContent(category);
        
        // Load category games
        loadCategoryGames(categoryId, sortBy);
        
    } catch (error) {
        console.error('Category page loading failed:', error);
        showError('Category page loading failed, please refresh the page');
    }
}

// 更新分类页面内容
function updateCategoryPageContent(category) {
    // Use English data
    const categoryName = category.nameEn || category.name;
    const categoryDescription = category.descriptionEn || category.description;
    const gameCount = getGamesByCategory(category.id).length;
    
    document.title = `${categoryName} | US Game Hub`;
    
    const elements = {
        categoryIcon: getCategoryIcon(category.id),
        categoryPageTitle: categoryName,
        categoryDesc: categoryDescription,
        gamesCount: `${gameCount} games`,
        categoryBreadcrumb: categoryName
    };
    
    Object.entries(elements).forEach(([id, content]) => {
        const element = document.getElementById(id);
        if (element) {
            element.innerHTML = content;
        }
    });
}

// Load category games
function loadCategoryGames(categoryId, sortBy = 'popular') {
    const container = document.getElementById('categoryGamesGrid');
    if (!container) return;
    
    let games = getGamesByCategory(categoryId);
    
    // 排序
    switch (sortBy) {
        case 'newest':
            games.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
            break;
        case 'rating':
            games.sort((a, b) => b.rating - a.rating);
            break;
        case 'name':
            games.sort((a, b) => a.title.localeCompare(b.title));
            break;
        default: // popular
            games.sort((a, b) => b.playCount - a.playCount);
    }
    
    container.innerHTML = games.map(createGameCard).join('');
    
    // 更新结果数量
    const resultsCount = document.getElementById('resultsCount');
    if (resultsCount) {
        resultsCount.textContent = `Showing ${games.length} games`;
    }
}

// 获取游戏控制说明（英文）
function getGameControlsInEnglish(game) {
    const controlsByCategory = {
        'puzzle': 'Use arrow keys or swipe to move tiles/pieces. Click to select and interact with game elements.',
        'action': 'Use WASD or arrow keys to move. Mouse to aim and click to shoot/attack. Spacebar for special actions.',
        'multiplayer': 'Player 1: WASD keys. Player 2: Arrow keys. Check game instructions for specific controls.',
        'cards': 'Click to select cards. Drag and drop to move cards. Use mouse to navigate game interface.',
        'sports': 'Use arrow keys for movement. Spacebar for actions like shooting/kicking. Mouse for precision control.',
        'strategy': 'Click to select units/buildings. Right-click for actions. Use mouse to navigate the map.'
    };
    
    return controlsByCategory[game.category] || 'Use mouse and keyboard to interact with the game. Check in-game instructions for specific controls.';
}

// 获取游戏攻略提示（英文）
function getGameTipsInEnglish(game) {
    const tipsByCategory = {
        'puzzle': 'Take your time to plan moves ahead. Look for patterns and combinations. Practice makes perfect!',
        'action': 'Stay mobile and use cover. Collect power-ups when possible. Learn enemy patterns for better strategy.',
        'multiplayer': 'Communicate with your teammate. Learn each player\'s strengths. Practice coordination for better results.',
        'cards': 'Plan your moves carefully. Keep track of played cards. Use strategy to anticipate opponent moves.',
        'sports': 'Time your actions well. Learn special moves and combos. Practice precision for better scores.',
        'strategy': 'Plan ahead and manage resources wisely. Balance offense and defense. Adapt your strategy based on situation.'
    };
    
    return tipsByCategory[game.category] || 'Read the game instructions carefully. Practice to improve your skills. Have fun and enjoy the game!';
}

// 导出全局函数
window.GameManager = {
    loadGameData,
    getGamesByCategory,
    getFeaturedGames,
    getNewestGames,
    getPopularGames,
    getGameById,
    searchGames,
    getRelatedGames,
    incrementPlayCount,
    getTagsCloud,
    initHomePage,
    loadGamePage,
    loadCategoryPage
};