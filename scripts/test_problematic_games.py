#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    os.system("chcp 65001 > nul 2>&1")
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

"""
Test specific games that might have domain restrictions
"""

import json
import requests
from datetime import datetime

def test_game_accessibility(game_id, iframe_url):
    """Test if a game shows domain restriction message"""
    try:
        response = requests.get(iframe_url, timeout=10)
        content = response.text.lower()
        
        # Check for common domain restriction messages
        restriction_indicators = [
            'not available here',
            'click here to play',
            'redirect',
            '不在这里',
            'available on',
            'play it on'
        ]
        
        has_restriction = any(indicator in content for indicator in restriction_indicators)
        
        return {
            'game_id': game_id,
            'status_code': response.status_code,
            'has_restriction': has_restriction,
            'content_length': len(content)
        }
    except Exception as e:
        return {
            'game_id': game_id,
            'status_code': 0,
            'has_restriction': True,
            'error': str(e)
        }

def main():
    print("测试可能有域名限制的GameDistribution游戏")
    print("=" * 50)
    
    # Load games data
    with open("data/games.json", 'r', encoding='utf-8') as f:
        games_data = json.load(f)
    
    # Test GameDistribution games
    gd_games = [game for game in games_data["games"] 
               if "gamedistribution.com" in game["iframeUrl"]]
    
    print(f"Found {len(gd_games)} GameDistribution games to test")
    print()
    
    problematic_games = []
    
    for i, game in enumerate(gd_games, 1):
        print(f"[{i}/{len(gd_games)}] Testing: {game['title']}")
        
        result = test_game_accessibility(game['id'], game['iframeUrl'])
        
        if result['has_restriction']:
            problematic_games.append(result)
            print(f"  ⚠️  PROBLEM DETECTED: {game['title']}")
        else:
            print(f"  ✅  OK: {game['title']}")
    
    print("\n" + "=" * 50)
    print("测试结果总结:")
    print(f"总GameDistribution游戏数: {len(gd_games)}")
    print(f"有问题的游戏数: {len(problematic_games)}")
    
    if problematic_games:
        print("\n有域名限制的游戏:")
        for game in problematic_games:
            print(f"  - {game['game_id']}")
        
        print("\n建议:")
        print("1. 联系GameDistribution申请域名白名单")
        print("2. 或者移除这些游戏")
        print("3. 或者使用新窗口打开模式")

if __name__ == "__main__":
    main()