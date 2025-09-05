// US Game Hub - 国际化语言支持

// 语言包数据
const translations = {
    en: {
        // 导航
        nav: {
            home: 'Home',
            categories: 'Categories ▾',
            about: 'About'
        },
        
        // 分类
        categories: {
            puzzle: 'Puzzle Games',
            action: 'Action Games', 
            multiplayer: 'Multiplayer Games',
            cards: 'Card Games',
            sports: 'Sports Games',
            strategy: 'Strategy Games'
        },
        
        // 分类描述
        categoryDesc: {
            puzzle: 'Challenge your mind with number games, jigsaw puzzles, memory games and more',
            action: 'Fast-paced action games including shooters, fighting, and running games',
            multiplayer: 'Games to play with friends, 2 player or multiplayer games',
            cards: 'Classic card games and board games',
            sports: 'Various sports and athletic games',
            strategy: 'Games that require strategic thinking'
        },
        
        // 页面区块
        sections: {
            categories: 'Game Categories',
            newest: 'New Games',
            popular: 'Popular Games',
            tags: 'Popular Tags'
        },
        
        // 按钮
        buttons: {
            viewMoreNew: 'View More New Games →',
            viewMorePopular: 'View More Popular Games →',
            playNow: '🎮 Play Now',
            startGame: '▶ Start Game',
            fullscreen: 'Fullscreen',
            newWindow: '🎮 Open in New Window',
            reload: '🔄 Reload',
            loadMore: 'Load More Games',
            postComment: 'Post Comment'
        },
        
        // 页脚
        footer: {
            categories: 'Game Categories',
            info: 'Site Information',
            updates: 'Recent Updates',
            about: 'About Us',
            privacy: 'Privacy Policy',
            sitemap: 'Sitemap',
            contact: 'Contact Us'
        },
        
        // 游戏相关
        game: {
            loading: 'Game loading...',
            cannotLoad: 'Game cannot load here',
            loadFailed: '😕 Game loading failed',
            networkIssue: 'Network connection may have issues, or game is temporarily unavailable',
            tryNewWindow: '🎮 Try in New Window',
            notSupported: 'This game may not support embedded playback',
            clickAbove: 'Click the button above to play in a new tab',
            gameControls: 'Game Controls',
            gameTips: 'How to Play',
            relatedGames: 'Related Games',
            similarGames: 'Similar Games',
            categoryHot: 'Popular in Category',
            shareLabel: 'Share:',
            plays: 'plays',
            clickToPlay: 'Click to Play',
            rateGame: 'Rate this game',
            shareGame: 'Share this game',
            comments: 'Comments',
            writeComment: 'Share your gaming experience...',
            postComment: 'Post Comment',
            gameDescription: 'About This Game'
        },
        
        // 分类页面
        categoryPage: {
            sortBy: 'Sort by:',
            mostPopular: 'Most Popular',
            newest: 'Newest',
            highestRated: 'Highest Rated',
            name: 'Name',
            showing: 'Showing',
            games: 'games',
            allCategories: 'All Categories'
        },
        
        // 搜索
        search: {
            placeholder: 'Search games...',
            noResults: 'No games found',
            results: 'Search Results'
        },
        
        // Cookie提示
        cookie: {
            message: 'We use cookies to enhance your gaming experience.',
            learnMore: 'Learn more',
            accept: 'Accept'
        },
        
        // 时间
        time: {
            yesterday: 'yesterday',
            daysAgo: 'days ago',
            weeksAgo: 'weeks ago'
        }
    },
    
    zh: {
        // 导航
        nav: {
            home: '首页',
            categories: '分类 ▾',
            about: '关于'
        },
        
        // 分类
        categories: {
            puzzle: '益智游戏',
            action: '动作游戏',
            multiplayer: '双人游戏', 
            cards: '棋牌游戏',
            sports: '体育游戏',
            strategy: '策略游戏'
        },
        
        // 分类描述
        categoryDesc: {
            puzzle: '挑战你的思维能力，包括数字游戏、拼图、记忆游戏等',
            action: '快节奏的动作游戏，包括射击、格斗、跑酷等',
            multiplayer: '与朋友一起玩的双人或多人游戏',
            cards: '经典的纸牌和棋类游戏',
            sports: '各种体育运动游戏',
            strategy: '需要策略思考的游戏'
        },
        
        // 页面区块
        sections: {
            categories: '游戏分类',
            newest: '最新游戏',
            popular: '热门游戏',
            tags: '热门标签'
        },
        
        // 按钮
        buttons: {
            viewMoreNew: '查看更多新游戏 →',
            viewMorePopular: '查看更多热门游戏 →',
            playNow: '🎮 立即游戏',
            startGame: '▶ 开始游戏',
            fullscreen: '🔍 全屏游戏',
            newWindow: '🎮 在新窗口中打开游戏',
            reload: '🔄 重新加载',
            loadMore: '加载更多游戏'
        },
        
        // 页脚
        footer: {
            categories: '游戏分类',
            info: '网站信息',
            updates: '最新更新',
            about: '关于我们',
            privacy: '隐私政策',
            sitemap: '网站地图',
            contact: '联系我们'
        },
        
        // 游戏相关
        game: {
            loading: '游戏加载中...',
            cannotLoad: '游戏无法在此处加载',
            loadFailed: '😕 游戏加载失败',
            networkIssue: '网络连接可能有问题，或游戏暂时不可用',
            tryNewWindow: '🎮 在新窗口中尝试',
            notSupported: '该游戏可能不支持嵌入播放',
            clickAbove: '点击上方按钮在新标签页中游戏',
            gameControls: '游戏操作',
            gameTips: '游戏攻略',
            relatedGames: '推荐游戏',
            similarGames: '相似游戏',
            categoryHot: '同分类热门',
            shareLabel: '分享:',
            plays: '次游戏',
            clickToPlay: '点击游戏',
            rateGame: '为游戏评分',
            shareGame: '分享游戏',
            comments: '游戏评论',
            writeComment: '分享你的游戏体验...',
            postComment: '发表评论',
            gameDescription: '关于这个游戏'
        },
        
        // 分类页面
        categoryPage: {
            sortBy: '排序:',
            mostPopular: '最受欢迎',
            newest: '最新游戏',
            highestRated: '最高评分',
            name: '游戏名称',
            showing: '显示',
            games: '个游戏',
            allCategories: '所有分类'
        },
        
        // 搜索
        search: {
            placeholder: '搜索游戏...',
            noResults: '没有找到游戏',
            results: '搜索结果'
        },
        
        // Cookie提示
        cookie: {
            message: '我们使用Cookie来增强您的游戏体验。',
            learnMore: '了解更多',
            accept: '接受'
        },
        
        // 时间
        time: {
            yesterday: '昨天',
            daysAgo: '天前',
            weeksAgo: '周前'
        }
    }
};

// 当前语言
let currentLanguage = 'en';

// 国际化类
class I18n {
    constructor() {
        this.currentLang = 'en'; // 强制使用英文
        this.translations = translations;
    }
    
    // 获取存储的语言
    getStoredLanguage() {
        return localStorage.getItem('language');
    }
    
    // 设置语言
    setLanguage(lang) {
        if (lang in this.translations) {
            this.currentLang = lang;
            localStorage.setItem('language', lang);
            currentLanguage = lang;
            this.updateAllTexts();
            this.updateLanguageToggle();
            console.log('Language changed to:', lang);
        }
    }
    
    // 获取翻译文本
    t(key) {
        const keys = key.split('.');
        let result = this.translations[this.currentLang];
        
        for (const k of keys) {
            if (result && typeof result === 'object') {
                result = result[k];
            } else {
                break;
            }
        }
        
        // 如果找不到翻译，返回英文版本或key
        if (!result) {
            let fallback = this.translations.en;
            for (const k of keys) {
                if (fallback && typeof fallback === 'object') {
                    fallback = fallback[k];
                } else {
                    break;
                }
            }
            result = fallback || key;
        }
        
        return result;
    }
    
    // 更新所有带有data-i18n属性的元素
    updateAllTexts() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.t(key);
            
            if (element.tagName === 'INPUT' && element.type === 'text') {
                element.placeholder = translation;
            } else {
                element.textContent = translation;
            }
        });
        
        // 更新页面语言属性
        document.documentElement.lang = this.currentLang;
    }
    
    // 更新语言切换按钮
    updateLanguageToggle() {
        const langToggle = document.querySelector('.lang-text');
        if (langToggle) {
            langToggle.textContent = 'EN'; // Always show EN since we force English
        }
    }
    
    // 获取当前语言
    getCurrentLanguage() {
        return this.currentLang;
    }
}

// 创建全局i18n实例
window.i18n = new I18n();

// 初始化多语言
document.addEventListener('DOMContentLoaded', function() {
    // 初始化时应用当前语言
    window.i18n.updateAllTexts();
    window.i18n.updateLanguageToggle();
});

// 导出到全局
window.I18n = I18n;
window.translations = translations;