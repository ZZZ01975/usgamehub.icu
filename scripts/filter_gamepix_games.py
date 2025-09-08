#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GamePix游戏筛选脚本
从11,616个游戏中筛选50个高质量游戏用于网站
"""

import csv
import json
import random
from collections import defaultdict
from datetime import datetime
import sys
import os

# 增加CSV字段大小限制
csv.field_size_limit(1000000)

def load_csv_games(csv_path):
    """从CSV文件加载游戏数据"""
    games = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, quotechar="'")
            for row in reader:
                try:
                    # 清理和验证数据
                    game = {
                        'id': row['id'].strip("'").strip(),
                        'title': row['title'].strip("'").strip(),
                        'namespace': row['namespace'].strip("'").strip(),
                        'description': row['description'].strip("'").strip().replace('""', '"'),
                        'category': row['category'].strip("'").strip(),
                        'orientation': row['orientation'].strip("'").strip(),
                        'quality_score': float(row['quality_score'].strip("'")) if row['quality_score'].strip("'") else 0.0,
                        'width': int(row['width'].strip("'")) if row['width'].strip("'") else 800,
                        'height': int(row['height'].strip("'")) if row['height'].strip("'") else 600,
                        'date_published': row['date_published'].strip("'").strip(),
                        'banner_image': row['banner_image'].strip("'").strip(),
                        'image': row['image'].strip("'").strip(),
                        'url': row['url'].strip("'").strip()
                    }
                    
                    # 基础质量过滤
                    if (game['quality_score'] >= 0.25 and 
                        len(game['title']) > 3 and 
                        len(game['description']) > 50 and
                        'embed?sid=1' in game['url']):
                        games.append(game)
                        
                except (ValueError, KeyError) as e:
                    continue
                    
    except Exception as e:
        print(f"错误：无法读取CSV文件 {csv_path}: {e}")
        return []
    
    print(f"从CSV加载了 {len(games)} 个有效游戏")
    return games

def categorize_games(games):
    """按分类整理游戏"""
    categories = defaultdict(list)
    for game in games:
        categories[game['category']].append(game)
    
    # 输出分类统计
    print("\n=== 分类统计 ===")
    for category, game_list in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"{category}: {len(game_list)} 个游戏")
    
    return categories

def select_best_games(categories, target_count=50):
    """从每个分类选择最佳游戏"""
    
    # 定义目标分类和数量分配
    category_targets = {
        'action': 8,        # 动作游戏
        'puzzle': 8,        # 益智游戏  
        'casual': 6,        # 休闲游戏
        'runner': 5,        # 跑酷游戏
        'io': 4,           # IO游戏
        'shooting': 3,      # 射击游戏
        'first-person-shooter': 3,  # FPS
        'platformer': 3,    # 平台游戏
        'arcade': 3,        # 街机游戏
        'racing': 2,        # 赛车游戏
        'sports': 2,        # 体育游戏
        'educational': 2,   # 教育游戏
        'match-3': 1        # 消除游戏
    }
    
    selected_games = []
    
    for category, target in category_targets.items():
        if category in categories:
            # 按质量分数排序，选择最佳游戏
            category_games = sorted(categories[category], 
                                  key=lambda x: x['quality_score'], 
                                  reverse=True)
            
            # 确保横屏竖屏游戏均衡
            landscape_games = [g for g in category_games if g['orientation'] in ['landscape', 'all']]
            portrait_games = [g for g in category_games if g['orientation'] == 'portrait']
            
            selected = []
            
            # 优先选择高质量横屏游戏
            for game in landscape_games[:target]:
                selected.append(game)
                
            # 如果数量不足，添加竖屏游戏
            if len(selected) < target:
                remaining = target - len(selected)
                for game in portrait_games[:remaining]:
                    if game not in selected:
                        selected.append(game)
            
            selected_games.extend(selected)
            print(f"{category}: 选择了 {len(selected)} 个游戏")
        else:
            print(f"{category}: 未找到游戏")
    
    # 如果还没达到目标数量，从其他分类补充
    if len(selected_games) < target_count:
        remaining_count = target_count - len(selected_games)
        print(f"\n需要补充 {remaining_count} 个游戏...")
        
        # 从未使用的分类中选择高质量游戏
        used_games = set(g['id'] for g in selected_games)
        all_remaining = []
        
        for category, games_list in categories.items():
            if category not in category_targets:
                for game in games_list:
                    if game['id'] not in used_games and game['quality_score'] >= 0.3:
                        all_remaining.append(game)
        
        # 按质量排序补充
        all_remaining.sort(key=lambda x: x['quality_score'], reverse=True)
        selected_games.extend(all_remaining[:remaining_count])
    
    return selected_games[:target_count]

def convert_to_website_format(selected_games):
    """将筛选的游戏转换为网站JSON格式"""
    
    # 分类映射
    category_mapping = {
        'action': 'action',
        'puzzle': 'puzzle', 
        'casual': 'puzzle',
        'runner': 'action',
        'io': 'multiplayer',
        'shooting': 'action',
        'first-person-shooter': 'action',
        'platformer': 'action',
        'arcade': 'action',
        'racing': 'sports',
        'sports': 'sports',
        'educational': 'puzzle',
        'match-3': 'puzzle',
        'board': 'cards',
        'card': 'cards'
    }
    
    website_games = []
    
    for i, game in enumerate(selected_games):
        # 生成SEO友好的关键词
        keywords = generate_keywords(game)
        
        # 转换为网站格式
        website_game = {
            "id": f"{game['namespace']}-gamepix",
            "title": game['title'],
            "description": clean_description(game['description']),
            "shortDesc": generate_short_desc(game['description']),
            "keywords": keywords,
            "category": category_mapping.get(game['category'], 'puzzle'),
            "tags": generate_tags(game),
            "source": "GamePix",
            "sourceUrl": "https://gamepix.com",
            "developer": "GamePix Studios",
            "attribution": "Powered by GamePix",
            "iframeUrl": game['url'],
            "thumbnailUrl": game['banner_image'],
            "iconUrl": game['image'],
            "difficulty": assign_difficulty(game['quality_score']),
            "rating": round(3.0 + game['quality_score'] * 2, 1),  # 转换为3.0-5.0评分
            "featured": i < 6,  # 前6个设为featured
            "quality": game['quality_score'],
            "dateAdded": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        
        website_games.append(website_game)
    
    return website_games

def generate_keywords(game):
    """生成SEO关键词"""
    base_keywords = [
        game['title'].lower(),
        game['category'],
        f"{game['category']} game",
        "free online game"
    ]
    
    # 基于分类添加特定关键词
    category_keywords = {
        'action': ['action game', 'adventure', 'fighting'],
        'puzzle': ['puzzle game', 'brain teaser', 'logic'],
        'runner': ['running game', 'endless runner'],
        'io': ['multiplayer', 'online multiplayer'],
        'shooting': ['shooter', 'gun game'],
        'racing': ['racing game', 'car game'],
        'sports': ['sports game', 'athletic']
    }
    
    if game['category'] in category_keywords:
        base_keywords.extend(category_keywords[game['category']])
    
    return base_keywords[:5]

def generate_tags(game):
    """生成游戏标签"""
    tags = [game['category']]
    
    if game['orientation'] == 'portrait':
        tags.append('mobile-friendly')
    elif game['orientation'] == 'landscape':
        tags.append('desktop-friendly')
    else:
        tags.append('all-devices')
        
    if game['quality_score'] >= 0.5:
        tags.append('high-quality')
    elif game['quality_score'] >= 0.4:
        tags.append('premium')
        
    return tags[:4]

def clean_description(desc):
    """清理游戏描述"""
    # 移除多余引号和格式化
    cleaned = desc.replace('""', '"').replace("''''", "'")
    
    # 确保描述长度适中
    if len(cleaned) > 300:
        cleaned = cleaned[:297] + "..."
    
    return cleaned

def generate_short_desc(desc):
    """生成简短描述"""
    cleaned = clean_description(desc)
    sentences = cleaned.split('.')
    return sentences[0][:80] + ("..." if len(sentences[0]) > 80 else "")

def assign_difficulty(quality_score):
    """基于质量分数分配难度"""
    if quality_score >= 0.5:
        return "hard"
    elif quality_score >= 0.35:
        return "medium"
    else:
        return "easy"

def save_results(games, output_path):
    """保存结果到JSON文件"""
    result = {"games": games}
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n成功保存 {len(games)} 个游戏到 {output_path}")
        return True
    except Exception as e:
        print(f"保存失败: {e}")
        return False

def main():
    """主函数"""
    print("GamePix游戏筛选工具")
    print("=" * 50)
    
    # 文件路径
    csv_path = "GameDistribution/gamepix_items.csv"
    output_path = "data/games_gamepix_filtered.json"
    
    # 检查CSV文件是否存在
    if not os.path.exists(csv_path):
        print(f"错误：找不到CSV文件 {csv_path}")
        return False
    
    # 步骤1：加载游戏数据
    print(f"加载游戏数据从 {csv_path}...")
    all_games = load_csv_games(csv_path)
    
    if not all_games:
        print("没有加载到有效游戏数据")
        return False
    
    # 步骤2：分类统计
    categories = categorize_games(all_games)
    
    # 步骤3：选择最佳游戏
    print(f"\n筛选50个最佳游戏...")
    selected_games = select_best_games(categories, 50)
    
    print(f"\n成功筛选出 {len(selected_games)} 个游戏")
    
    # 步骤4：转换格式
    print("\n转换为网站JSON格式...")
    website_games = convert_to_website_format(selected_games)
    
    # 步骤5：保存结果
    if save_results(website_games, output_path):
        print("\n游戏筛选完成！")
        
        # 输出总结
        print("\n=== 筛选总结 ===")
        category_counts = defaultdict(int)
        for game in website_games:
            category_counts[game['category']] += 1
            
        for category, count in category_counts.items():
            print(f"{category}: {count} 个游戏")
            
        quality_high = sum(1 for g in website_games if g['quality'] >= 0.4)
        print(f"\n高质量游戏(≥0.4): {quality_high}/{len(website_games)}")
        
        featured_count = sum(1 for g in website_games if g['featured'])
        print(f"精选游戏: {featured_count}/{len(website_games)}")
        
        return True
    else:
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)