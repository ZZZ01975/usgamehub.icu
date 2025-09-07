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
Add 10 new GameDistribution games from EMBED.md (entries 11-20)
"""

import json
from datetime import datetime, timezone
import re

def extract_game_id_from_embed(embed_code):
    """Extract game ID from iframe embed code"""
    match = re.search(r'https://html5\.gamedistribution\.com/([a-f0-9]+)/', embed_code)
    if match:
        return match.group(1)
    return None

def determine_category(title, description):
    """Determine game category based on title and description"""
    title_lower = title.lower()
    desc_lower = description.lower()
    
    # Category keywords mapping
    categories = {
        'puzzle': ['puzzle', 'brain', 'riddle', 'math', 'solitaire', 'tripeaks', 'maze'],
        'action': ['platformer', 'geometry', 'race', 'racing', 'climber'],
        'simulation': ['grass land', 'exploration', 'asmr', 'beauty', 'superstar'],
        'strategy': ['traffic cop', 'cop', 'police'],
        'trivia': ['guess', 'brainrot', 'animals', 'italian']
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in desc_lower:
                return category
    
    return 'puzzle'  # Default category

def main():
    print("批量添加10款新的GameDistribution游戏")
    print("=" * 50)
    
    # New games data from EMBED.md entries 11-20
    new_games = [
        {
            "title": "Draw Climber",
            "description": "Funniest race you ever played! Draw your legs to win the race! Any drawing will make you run! When you are stuck you can draw another shape to pass!",
            "controls": "Draw your legs to win the race!",
            "embed": '<iframe src="https://html5.gamedistribution.com/f3471828433f4cafab9b5d64aa4ef6ae/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="1600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Grass Land",
            "description": "Grass Land is a vibrant exploration game that drops you into a sprawling world of thick greenery and hidden surprises. Take control of your grass cutter, uncover valuable resources beneath the overgrowth, and build up your base as you roam the fields. Stay sharp, move fast, and make the most of every patch of grass you find.",
            "controls": "Use WASD / arrow keys / joystick to control the character.",
            "embed": '<iframe src="https://html5.gamedistribution.com/265715cb6c0344e19716900ca42eca18/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "ASMR Beauty Superstar",
            "description": "Welcome to ASMR Clinic, where relaxation meets rejuvenation! Our superstar guest is receiving expert care for acne-prone skin and rough feet in a serene atmosphere. Our skilled doctors will work their magic, providing personalized attention to detail and soothing care. Customize her look with various hairstyles, makeup looks, and shoes to create a stunning outfit that's uniquely hers. Unwind and express your creativity in this calming and fashionable game.",
            "controls": "Use MOUSE to play the game.",
            "embed": '<iframe src="https://html5.gamedistribution.com/1674fcf4337743cfadd20005158c6f2f/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Guess The Italian Brainrot Animals",
            "description": "Get ready for a wild and hilarious ride with Guess the Italian Brainrot Animals, a fast-paced, emoji-fueled trivia game that tests your knowledge of 64 iconic Italian Brainrot characters! From the most famous to the obscure, this game challenges you to guess the correct character based on three emoji clues before the timer runs out. Think you're a Brainrot expert? Prove it!",
            "controls": "How to Play Guess the Italian Brainrot Animals? Mouse/Touch: Click or tap to select your answer. Keyboard Shortcuts: Use W, A, or D to quickly choose from the three options. 2 Player Mode: Player 1: W, A, D keys. Player 2: Right, Left, Up arrow keys.",
            "embed": '<iframe src="https://html5.gamedistribution.com/485ace88aed344f8b2ff6821a46e4431/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="960" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Block Pixels",
            "description": "Block Pixels is a vibrant puzzle game where classic block-clearing action meets the creative joy of pixel art discovery. Your main goal is to strategically place colorful pieces to clear lines on the board. But the real magic lies in what you clear. Each block you eliminate contributes to a larger masterpiece. Clearing specific colors helps you build and reveal dozens of charming hidden images, from cute animals to fun objects.",
            "controls": "Drag the colorful blocks onto the grid to complete lines and clear them from the board. Collect the specific colors needed to reveal the hidden pixel image for a huge bonus!",
            "embed": '<iframe src="https://html5.gamedistribution.com/60243f5a5a994dd8ba4030b11f0a41a9/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Geometry Platformer",
            "description": "Geometry Platformer is a fast-paced, reflex-testing platformer where players guide a shape-shifting cube through a series of dangerous geometric obstacles. The game features sharp spikes, swinging hazards, and gravity-defying mechanics that challenge your timing and precision. The neon graphics and intense gameplay create a thrilling experience, requiring quick reactions and memorization of complex patterns.",
            "controls": "WASD - Move Space - Jump",
            "embed": '<iframe src="https://html5.gamedistribution.com/b072eec82dec4ad8b6fa3a602052e90b/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="960" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Traffic Cop 3D",
            "description": "Traffic Cop 3D is a casual game where you play as a police officer enforcing the law of the road. Scan nearby drivers and use intel from the police database to decide whether you should pull them over, or let them go, all while progressing through the story and increasing your duties as a cop.",
            "controls": "Use the left mouse button on desktop or touch on mobile to play the game.",
            "embed": '<iframe src="https://html5.gamedistribution.com/fed5711667c840b3a394043324bf0def/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "World Solitaire -Tripeaks-",
            "description": "It is TriPeaks, one of the most famous solitaires in the world. Take a step to go up and test your brain and luck How far can I clean it?",
            "controls": "TriPeaks Solitaire is a puzzle card game where cards are arranged in a pyramid shape on the table. You remove cards one by one by selecting cards that are one rank higher or lower than the card from the deck. Suit and color don't matter. If no moves are available, draw a new card from the deck. Consecutive removals earn bonus points, and you win by clearing all cards from the table.",
            "embed": '<iframe src="https://html5.gamedistribution.com/5e0be72dc1d44e659adc627331797b2d/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "RiddleMath",
            "description": "Math Riddles level up your IQ with a mix of logical puzzles. Challenge yourself with different levels of math games and stretch the limits of your mind. Brain games are prepared with an approach of an IQ test.",
            "controls": "For Pc - Use your mouse to click on any of the available numbers. Once selected, click on an empty spot in the puzzle to place the number there. For Mobile - Drag the number from the available list and drop it into the empty space.",
            "embed": '<iframe src="https://html5.gamedistribution.com/a74a2b0e637149389b9a805f2dd21feb/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="960" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Alphabet Lore Maze",
            "description": "Alphabet Maze: Escape Letters is an exciting puzzle game that will help develop the struggle of minds and learn the letters of the alphabet. In this educational game you will explore the maze, defeating monsters, teddy bear and letter creatures. Choose characters from the collection that include Huggy, Teddy Bear, Harry and many other unique characters. To get out of the maze, you need to choose rooms with a smaller number than yours and avoid monsters larger than your level.",
            "controls": "PC Control: Arrows/WASD Control on a mobile device: Swipe - Move between rooms - Choose a room with a smaller room than yours - Avoid enemies bigger than your level - Move on and defeat the last monster",
            "embed": '<iframe src="https://html5.gamedistribution.com/d7ff6011917d4fb98589e5087f00795d/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        }
    ]
    
    # Load current games data
    try:
        with open("data/games.json", 'r', encoding='utf-8') as f:
            games_data = json.load(f)
    except Exception as e:
        print(f"Error loading games data: {e}")
        return
    
    # Create backup
    backup_file = f"data/games_backup_new_10_games_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Backup failed: {e}")
        return
    
    # Add new games
    added_count = 0
    
    for game_info in new_games:
        # Extract game ID from embed code
        game_id_gd = extract_game_id_from_embed(game_info["embed"])
        if not game_id_gd:
            print(f"Failed to extract game ID from: {game_info['title']}")
            continue
            
        # Generate game ID for our system
        game_id = game_info["title"].lower().replace(" ", "-").replace("'", "").replace("-", "-") + "-gd"
        game_id = re.sub(r'[^a-z0-9-]', '', game_id)
        game_id = re.sub(r'-+', '-', game_id)
        game_id = game_id.strip('-')
        
        # Check if game already exists
        existing_game = any(game["id"] == game_id for game in games_data["games"])
        if existing_game:
            print(f"Game already exists: {game_id}")
            continue
        
        # Create game entry
        new_game = {
            "id": game_id,
            "title": game_info["title"],
            "description": game_info["description"],
            "shortDesc": game_info["description"].split('.')[0] + '.' if '.' in game_info["description"] else game_info["description"][:100] + '...',
            "iframeUrl": f"https://html5.gamedistribution.com/{game_id_gd}/?gd_sdk_referrer_url=https://usgamehub.icu/game.html?id={game_id}",
            "category": determine_category(game_info["title"], game_info["description"]),
            "tags": [],
            "keywords": [],
            "controls": game_info["controls"],
            "rating": 4.5,
            "plays": 0,
            "featured": False,
            "trending": False,
            "new": True,
            "thumbnailUrl": f"assets/images/{game_id}.jpg",
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "updatedAt": datetime.now(timezone.utc).isoformat()
        }
        
        # Add keywords and tags based on title and description
        title_words = re.findall(r'\w+', game_info["title"].lower())
        desc_words = re.findall(r'\w+', game_info["description"].lower())
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'game', 'play', 'player', 'games'}
        
        keywords = list(set([word for word in title_words + desc_words if len(word) > 3 and word not in common_words]))[:6]
        new_game["keywords"] = keywords
        new_game["tags"] = keywords[:5]
        
        games_data["games"].append(new_game)
        print(f"Added: {game_info['title']} (ID: {game_id})")
        added_count += 1
    
    # Update metadata
    games_data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    games_data["version"] = f"2.5-added-{added_count}-new-games"
    games_data["note"] = f"Added {added_count} new GameDistribution games from EMBED.md entries 11-20"
    
    # Save updated data
    try:
        with open("data/games.json", 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"\n成功！添加了 {added_count} 款新游戏")
        print(f"总游戏数量：{len(games_data['games'])}")
        print("\n新增游戏列表：")
        for i, game_info in enumerate(new_games, 1):
            if i <= added_count:
                print(f"  {i}. {game_info['title']}")
        print("\n下一步：")
        print("1. 运行健康检查验证所有游戏")
        print("2. 删除有问题的游戏")
        print("3. 提交到 GitHub")
    except Exception as e:
        print(f"Save failed: {e}")

if __name__ == "__main__":
    main()