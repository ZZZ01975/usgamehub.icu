// US Game Hub - Google Analytics 4 配置

// Google Analytics 4 初始化
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}

// 基础配置
gtag('js', new Date());

// 配置GA4 - 使用原仓库的测量ID
const GA_MEASUREMENT_ID = 'G-P13WZKJZ3H'; // Monster Survivors 原仓库的Analytics ID

gtag('config', GA_MEASUREMENT_ID, {
    // 基础设置
    page_title: document.title,
    page_location: window.location.href,
    
    // 隐私设置
    anonymize_ip: true,
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
    
    // 自定义配置
    custom_map: {
        'game_category': 'category',
        'game_id': 'game_id'
    }
});

// 游戏相关事件追踪
const Analytics = {
    // 游戏开始事件
    trackGameStart: function(gameId, gameName, category) {
        gtag('event', 'game_start', {
            'game_id': gameId,
            'game_name': gameName,
            'game_category': category,
            'event_category': 'Games',
            'event_label': gameName,
            'value': 1
        });
        
        console.log('Analytics: 游戏开始 -', gameName);
    },
    
    // 游戏完成事件
    trackGameComplete: function(gameId, gameName, playTime) {
        gtag('event', 'game_complete', {
            'game_id': gameId,
            'game_name': gameName,
            'play_time': playTime,
            'event_category': 'Games',
            'event_label': gameName,
            'value': playTime
        });
        
        console.log('Analytics: 游戏完成 -', gameName, '用时:', playTime);
    },
    
    // 搜索事件
    trackSearch: function(searchTerm, resultsCount) {
        gtag('event', 'search', {
            'search_term': searchTerm,
            'results_count': resultsCount,
            'event_category': 'Search',
            'event_label': searchTerm
        });
        
        console.log('Analytics: 搜索 -', searchTerm, '结果数:', resultsCount);
    },
    
    // 分类浏览事件
    trackCategoryView: function(categoryId, categoryName, gamesCount) {
        gtag('event', 'category_view', {
            'category_id': categoryId,
            'category_name': categoryName,
            'games_count': gamesCount,
            'event_category': 'Navigation',
            'event_label': categoryName
        });
        
        console.log('Analytics: 分类浏览 -', categoryName);
    },
    
    // 分享事件
    trackShare: function(platform, gameId, gameName) {
        gtag('event', 'share', {
            'method': platform,
            'content_type': 'game',
            'item_id': gameId,
            'game_name': gameName,
            'event_category': 'Social',
            'event_label': gameName
        });
        
        console.log('Analytics: 分享 -', platform, gameName);
    },
    
    // 用户参与度事件
    trackEngagement: function(action, gameId, value = 1) {
        gtag('event', 'engagement', {
            'engagement_type': action,
            'game_id': gameId,
            'event_category': 'Engagement',
            'event_label': action,
            'value': value
        });
        
        console.log('Analytics: 用户参与 -', action);
    },
    
    // 错误事件
    trackError: function(errorType, errorMessage, page, gameId = null) {
        gtag('event', 'exception', {
            'description': errorMessage,
            'fatal': false,
            'error_type': errorType,
            'page': page,
            'game_id': gameId,
            'event_category': 'Errors'
        });
        
        console.log('Analytics: 错误 -', errorType, errorMessage);
    },
    
    // 游戏模式追踪 (iframe vs new window)
    trackGameMode: function(gameId, gameName, mode, success = true) {
        gtag('event', 'game_mode', {
            'game_id': gameId,
            'game_name': gameName,
            'display_mode': mode, // 'iframe' or 'new_window'
            'success': success,
            'event_category': 'Game Display',
            'event_label': mode
        });
        
        console.log('Analytics: 游戏模式 -', gameName, mode, success ? '成功' : '失败');
    },
    
    // 弹窗拦截追踪
    trackPopupBlocked: function(gameId, gameName) {
        gtag('event', 'popup_blocked', {
            'game_id': gameId,
            'game_name': gameName,
            'event_category': 'User Experience',
            'event_label': 'popup_blocked'
        });
        
        console.log('Analytics: 弹窗被拦截 -', gameName);
    },
    
    // 页面浏览时间
    trackPageTiming: function(pageName, loadTime) {
        gtag('event', 'timing_complete', {
            'name': 'page_load',
            'value': loadTime,
            'page_name': pageName,
            'event_category': 'Performance'
        });
        
        console.log('Analytics: 页面加载时间 -', pageName, loadTime + 'ms');
    },
    
    // 转换事件（如广告点击、注册等）
    trackConversion: function(action, value = 1) {
        gtag('event', 'conversion', {
            'send_to': GA_MEASUREMENT_ID,
            'event_category': 'Conversion',
            'event_label': action,
            'value': value
        });
        
        console.log('Analytics: 转换事件 -', action);
    }
};

// 自动追踪页面性能
window.addEventListener('load', function() {
    const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
    const pageName = window.location.pathname;
    Analytics.trackPageTiming(pageName, loadTime);
});

// 自动追踪用户参与度（滚动深度）
let scrollDepthTracked = {
    25: false,
    50: false,
    75: false,
    100: false
};

window.addEventListener('scroll', throttle(function() {
    const scrollTop = window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const scrollPercent = Math.round((scrollTop / docHeight) * 100);
    
    Object.keys(scrollDepthTracked).forEach(depth => {
        if (scrollPercent >= depth && !scrollDepthTracked[depth]) {
            scrollDepthTracked[depth] = true;
            gtag('event', 'scroll', {
                'event_category': 'Engagement',
                'event_label': depth + '%',
                'value': parseInt(depth)
            });
            console.log('Analytics: 滚动深度 -', depth + '%');
        }
    });
}, 1000));

// 防抖函数
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
    };
}

// 自动追踪外链点击
document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && link.hostname !== window.location.hostname) {
        gtag('event', 'click', {
            'event_category': 'Outbound Link',
            'event_label': link.href,
            'transport_type': 'beacon'
        });
        console.log('Analytics: 外链点击 -', link.href);
    }
});

// 追踪文件下载（如果有的话）
document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && link.href) {
        const fileExtension = link.href.split('.').pop().toLowerCase();
        const downloadableFiles = ['pdf', 'zip', 'doc', 'xls', 'ppt', 'mp3', 'mp4', 'avi'];
        
        if (downloadableFiles.includes(fileExtension)) {
            gtag('event', 'file_download', {
                'event_category': 'Downloads',
                'event_label': link.href,
                'file_extension': fileExtension
            });
            console.log('Analytics: 文件下载 -', link.href);
        }
    }
});

// 游戏特定的分析功能
const GameAnalytics = {
    // 开始追踪游戏会话
    startGameSession: function(gameId) {
        const startTime = Date.now();
        sessionStorage.setItem(`game_start_${gameId}`, startTime);
        
        // 触发游戏开始事件
        const game = window.GameManager ? window.GameManager.getGameById(gameId) : null;
        if (game) {
            Analytics.trackGameStart(gameId, game.title, game.category);
        }
        
        return startTime;
    },
    
    // 结束游戏会话
    endGameSession: function(gameId) {
        const startTime = sessionStorage.getItem(`game_start_${gameId}`);
        if (startTime) {
            const playTime = Date.now() - parseInt(startTime);
            const game = window.GameManager ? window.GameManager.getGameById(gameId) : null;
            
            if (game) {
                Analytics.trackGameComplete(gameId, game.title, Math.round(playTime / 1000));
            }
            
            sessionStorage.removeItem(`game_start_${gameId}`);
            return playTime;
        }
        return 0;
    },
    
    // 追踪游戏内事件（如果游戏支持的话）
    trackGameEvent: function(gameId, eventType, eventData = {}) {
        gtag('event', 'game_event', {
            'game_id': gameId,
            'event_type': eventType,
            'event_category': 'Game Events',
            'event_label': eventType,
            ...eventData
        });
        
        console.log('Analytics: 游戏内事件 -', gameId, eventType);
    }
};

// 页面卸载时结束所有游戏会话
window.addEventListener('beforeunload', function() {
    // 检查是否有活跃的游戏会话
    for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        if (key && key.startsWith('game_start_')) {
            const gameId = key.replace('game_start_', '');
            GameAnalytics.endGameSession(gameId);
        }
    }
});

// 导出到全局
window.Analytics = Analytics;
window.GameAnalytics = GameAnalytics;

// 开发环境下的提示
if (GA_MEASUREMENT_ID === 'GA_MEASUREMENT_ID') {
    console.warn('请配置正确的 Google Analytics 4 测量ID');
}

console.log('Analytics.js 加载完成');