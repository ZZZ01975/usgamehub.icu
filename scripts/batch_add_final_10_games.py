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
Add final 10 GameDistribution games from EMBED.md (entries 21-30)
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
        'puzzle': ['merge', 'numbers', 'math', 'rockets', 'division', 'runner', 'words', 'owl', 'spelling'],
        'simulation': ['hair salon', 'beauty', 'dress up', 'doll', 'princess', 'makeover', 'fashion'],
        'action': ['dance', 'wednesday', 'worms', 'snake', 'slithery', 'zone'],
        'cards': ['solitaire'],
        'educational': ['math', 'spelling', 'word'],
        'arcade': ['worms', 'snake']
    }
    
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in title_lower or keyword in desc_lower:
                return category
    
    return 'puzzle'  # Default category

def main():
    print("批量添加最后10款GameDistribution游戏")
    print("=" * 50)
    
    # New games data from EMBED.md entries 21-30
    new_games = [
        {
            "title": "Merge the Numbers",
            "description": "Merge the numbers and reach the highest score!",
            "controls": "Drag the same numbers and merge them to reach the highest score",
            "embed": '<iframe src="https://html5.gamedistribution.com/b29c057bedf0482b858f004fb61b1b44/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="1024" height="768" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Math Rockets Division",
            "description": "This is a math puzzle game where the player needs to tap the rocket, showing the correct answer to the given division expression. In each level, you will have 10 expressions to solve. Complete all 8 challenges and enhance your math skills.",
            "controls": "Use a mouse or touchpad to play this game.",
            "embed": '<iframe src="https://html5.gamedistribution.com/e8853f6d4f2f49d68a7af7142077f7ab/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="450" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Math Runner",
            "description": "Challenge your mind and reflexes in this fast-paced arithmetic adventure! Solve math problems on the run, dodge obstacles, and race against time to achieve the highest score. Perfect for players of all ages looking to sharpen their math skills while enjoying thrilling gameplay.",
            "controls": "1. Start Running: Your character begins sprinting through dynamic environments. 2. Solve Math Problems: Encounter math challenges that you must solve quickly to continue. 3. Choose the Correct Path: Select the right answer to keep running; a wrong choice ends the game. 4. Collect Rewards: Gather coins and power-ups to boost your score and unlock new features. 5. Aim for High Scores: The faster and more accurately you solve problems, the higher your score.",
            "embed": '<iframe src="https://html5.gamedistribution.com/a8870b5a6a76492db5cb8ca599f64843/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Hair Salon: Beauty Salon",
            "description": "Get ready to unleash your inner hairstylist with the adorable and entertaining game Hair Salon: Beauty Salon Spa! This charming simulation game allows you to run your very own hair salon, where you can give your cute and quirky customers the hair style of their dreams. From washing, styling hair and providing luxurious jewelry & makeup accessories, there's never a dull moment in this delightful game.",
            "controls": "With a wide range of hairstyles and makeup accessories to choose from, you can let your creativity run wild and give your clients a look that's uniquely their own.",
            "embed": '<iframe src="https://html5.gamedistribution.com/551fb5282e0042f692221fb6e427e269/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="1080" height="1920" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Words with Owl",
            "description": "Test your spelling skills and word recognition in this fun and challenging game! Complete words by filling in the missing letters and aim for the highest score. Unlock exciting new stages as you progress and enjoy a rewarding wordplay experience.",
            "controls": "You'll be given incomplete words with missing letters—your goal is to click the letters in the correct order to complete them. Think fast and act quickly to earn more stars before time runs out. The faster you are, the higher your score!",
            "embed": '<iframe src="https://html5.gamedistribution.com/f44a159d660b4b9289f9add40a3cd7c0/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Magic Princess: Dress Up Doll",
            "description": "Magic Princess - Dress up & Character Maker game, come and design the cutest doll! Magic Princess is a fashionable ultra-casual simulation girl game with a strong anime chibi style, suitable for all unique girls to play. Design dolls and let your imagination soar! Dress up your doll in your own unique way now!",
            "controls": "Click to makeover with your finger, Put on suitable cosmetics, Dress up in a variety of clothing and items, Arrange the scenario, Create an unique photographic memory",
            "embed": '<iframe src="https://html5.gamedistribution.com/4dfe529f898544ecab4d3682199bcaf5/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="600" height="800" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Weird Dance on Wednesday",
            "description": "A goth girl is going to a school prom. She wants to make a splash with her new dance. Rogue rehearsed this dance for a whole month. She came up with it herself, inspired by classic films. The gothic girl has prepared a gorgeous black dress, but something is missing. Certainly! How can you go to a ball without makeup? Help the goth girl to choose a make-up that reflects her inner world. Use bold and dark shades to emphasize the eyes and lips. A few freckles will make the look a little more romantic. Go to the ball - have fun and dance a weird dance on Wednesday!",
            "controls": "Depending on the gaming device, a computer mouse click or a simple touch on touch screens is used for control.",
            "embed": '<iframe src="https://html5.gamedistribution.com/5fb340f644374ca09be7d35a90f62ba9/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="800" height="600" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Wednesday Dark Academia",
            "description": "With Wednesday Dark Academia, you can choose from various unique and stylish outfits, accessories, and makeup options. Start with her makeup, creating a look that's perfect for school or the ballroom. Play dark lipstick and eyeshadow, and with a little bit of imagination, you can create a look that's all your own. Next, dress her up for a fun day at school, and then see what party look you can put together for her. Style her hair and pick the right accessories for a complete look.",
            "controls": "Use your mouse to play the game on a desktop, tap to play on mobile devices.",
            "embed": '<iframe src="https://html5.gamedistribution.com/37e2c1f9866e4864aa67164768af4f8d/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="1024" height="768" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Paper Doll Diary: Dress Up DIY",
            "description": "Welcome to Paper Doll Diary: Doll DressUp, where the timeless charm of DIY paper dolls meets the exhilarating world of fashion dress up! Step into a realm of creativity and style where you become the master stylist of your enchanting paper doll dress up. With an expansive wardrobe featuring over 1000 fashion items, including the latest in trendy attire, distinctive accessories, diverse hairstyles, and soothing ASMR makeup touches, your creative potential is limitless.",
            "controls": "Unleash your inner fashionista and transform your paper doll into a beacon of style. Whether you're assembling chic outfits or selecting the perfect accessories, each decision propels your paper doll into the spotlight, making her a true fashion icon. Your styling choices not only reflect your unique taste but also guide your doll's journey through thrilling adventures and challenges.",
            "embed": '<iframe src="https://html5.gamedistribution.com/6fcaa70b796547a698ddd10808527345/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="1080" height="1920" scrolling="none" frameborder="0"></iframe>'
        },
        {
            "title": "Worms Zone a Slithery Snake",
            "description": "Worms Zone is a game with a dynamic storyline. Start growing your worm right now. Having tried to get a real anaconda, a small worm never gets stuck in one place – he's ready to bite everyone. However, there is a danger to be eaten by a more successful player. The Worms are real gourmets. They love trying various gelatinous goodies and everything they meet on their route.",
            "controls": "Use the mouse to control the worm's direction and space bar to speed up it.",
            "embed": '<iframe src="https://html5.gamedistribution.com/5dd0b18fb81d49da82ff459f08737390/?gd_sdk_referrer_url=https://www.example.com/games/{game-path}" width="960" height="640" scrolling="none" frameborder="0"></iframe>'
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
    backup_file = f"data/games_backup_final_10_games_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
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
        game_id = game_info["title"].lower().replace(" ", "-").replace(":", "").replace("'", "").replace("-", "-") + "-gd"
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
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'game', 'play', 'player', 'games', 'your'}
        
        keywords = list(set([word for word in title_words + desc_words if len(word) > 3 and word not in common_words]))[:6]
        new_game["keywords"] = keywords
        new_game["tags"] = keywords[:5]
        
        games_data["games"].append(new_game)
        print(f"Added: {game_info['title']} (ID: {game_id})")
        added_count += 1
    
    # Update metadata
    games_data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    games_data["version"] = f"2.7-added-final-{added_count}-games"
    games_data["note"] = f"Added final {added_count} GameDistribution games from EMBED.md entries 21-30"
    
    # Save updated data
    try:
        with open("data/games.json", 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"\n成功！添加了 {added_count} 款最终游戏")
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