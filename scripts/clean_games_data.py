#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据探活检测结果清理games.json，只保留可用的游戏
"""

import json
import os
from datetime import datetime

def clean_games_data():
    """根据检测结果清理游戏数据"""
    
    # 读取检测结果
    try:
        with open('scripts/results/summary_20250907.json', 'r', encoding='utf-8') as f:
            results = json.load(f)
    except FileNotFoundError:
        print("Error: Detection results not found")
        return
    
    # 读取原始游戏数据
    try:
        with open('data/games.json', 'r', encoding='utf-8') as f:
            original_data = json.load(f)
    except FileNotFoundError:
        print("Error: Original games.json not found")
        return
    
    # 获取可用游戏的ID列表
    available_ids = [game['id'] for game in results['available_games']]
    print(f"Available game IDs: {available_ids}")
    
    # 筛选可用的游戏（保留完整数据）
    available_games = []
    for game in original_data['games']:
        if game['id'] in available_ids:
            # 添加可嵌入标记
            game['embeddable'] = True
            game['verified_date'] = datetime.now().strftime('%Y-%m-%d')
            available_games.append(game)
    
    # 创建清理后的数据结构
    cleaned_data = {
        "games": available_games,
        "totalCount": len(available_games),
        "lastUpdated": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.000Z'),
        "version": "2.0-cleaned",
        "note": f"Cleaned version containing only {len(available_games)} verified working games"
    }
    
    # 备份原始文件
    backup_filename = f'data/games_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(backup_filename, 'w', encoding='utf-8') as f:
        json.dump(original_data, f, indent=2, ensure_ascii=False)
    print(f"Original games.json backed up to: {backup_filename}")
    
    # 保存清理后的数据
    with open('data/games.json', 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, indent=2, ensure_ascii=False)
    
    # 显示清理结果
    print("\n" + "=" * 60)
    print("Games data cleaned successfully!")
    print(f"Original games: {original_data.get('totalCount', len(original_data['games']))}")
    print(f"Cleaned games: {len(available_games)}")
    print(f"Removed: {original_data.get('totalCount', len(original_data['games'])) - len(available_games)} games")
    
    print("\nRemaining games by category:")
    category_count = {}
    for game in available_games:
        cat = game['category']
        category_count[cat] = category_count.get(cat, 0) + 1
    
    for category, count in category_count.items():
        print(f"  - {category}: {count} games")
    
    print("\nRemaining games list:")
    for i, game in enumerate(available_games, 1):
        status = "[Featured]" if game.get('featured', False) else ""
        print(f"  {i}. {game['title']} ({game['category']}) {status}")
    
    return cleaned_data

if __name__ == "__main__":
    # 确保在正确的目录下运行
    if not os.path.exists('data/games.json'):
        print("Please run this script from project root directory")
        exit(1)
    
    clean_games_data()