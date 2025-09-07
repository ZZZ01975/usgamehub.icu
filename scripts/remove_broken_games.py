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
Remove broken games with 404 errors
"""

import json
from datetime import datetime, timezone

def main():
    print("删除有问题的游戏")
    print("=" * 30)
    
    # Games to remove (404 errors)
    games_to_remove = [
        "snake-adventure-gd",
        "tic-tac-toe-pro-gd"
    ]
    
    # Load current games data
    try:
        with open("data/games.json", 'r', encoding='utf-8') as f:
            games_data = json.load(f)
    except Exception as e:
        print(f"Error loading games data: {e}")
        return
    
    # Create backup
    backup_file = f"data/games_backup_removed_broken_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Backup failed: {e}")
        return
    
    # Remove broken games
    removed_count = 0
    original_count = len(games_data["games"])
    
    # Filter out broken games
    games_data["games"] = [
        game for game in games_data["games"] 
        if game["id"] not in games_to_remove
    ]
    
    removed_count = original_count - len(games_data["games"])
    
    # Update metadata
    games_data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    games_data["version"] = f"2.6-removed-{removed_count}-broken-games"
    games_data["note"] = f"Removed {removed_count} broken games with 404 errors"
    
    # Save updated data
    try:
        with open("data/games.json", 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"\n成功！删除了 {removed_count} 个有问题的游戏")
        print(f"剩余游戏数量：{len(games_data['games'])}")
        print("\n删除的游戏：")
        for game_id in games_to_remove:
            print(f"  - {game_id}")
        print("\n现在所有游戏都可以正常使用！")
    except Exception as e:
        print(f"Save failed: {e}")

if __name__ == "__main__":
    main()