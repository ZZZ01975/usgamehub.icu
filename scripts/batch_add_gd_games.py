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
Batch Add GameDistribution Games Script
Based on the 10 games from your EMBED spreadsheet
"""

import json
from datetime import datetime, timezone

def main():
    print("GameDistribution Batch Games Import")
    print("="*50)
    
    # 10 GameDistribution games from your spreadsheet
    # Please verify and update these game IDs and details
    new_games = [
        {
            "id": "buckshot-roulette-gd",
            "title": "Buckshot Roulette",
            "category": "action",
            "description": "Do you dare to bet your life on an exciting roulette wheel showdown? Buckshot Roulette is a gun simulator that combines strategy, shooting and survival. Instead of a pistol, a powerful shotgun was used. Every pull of the trigger is a choice of fate. The winner lives, the loser dies.",
            "keywords": ["buckshot", "roulette", "gun", "survival", "strategy"],
            "tags": ["shooting", "survival", "strategy", "roulette", "intense"],
            "gd_game_id": "87c64328223642f3f8ac0dddfcb41611e"
        },
        {
            "id": "catch-the-goose-gd", 
            "title": "Catch The Goose",
            "category": "puzzle",
            "description": "Catch The Goose is a puzzle elimination mini-game. Players can tap identical items to automatically send them to the bottom slot - when three matching items gather, they get eliminated. Successfully clear all items to catch a mischievous goose.",
            "keywords": ["goose", "puzzle", "match 3", "elimination", "casual"],
            "tags": ["puzzle", "matching", "casual", "elimination", "cute"],
            "gd_game_id": "698157ec8128471e91e2f32e4bc350ee"
        },
        {
            "id": "sort-puzzle-nuts-bolts-gd",
            "title": "Sort Puzzle - Nuts and Bolts", 
            "category": "puzzle",
            "description": "Play Sort Puzzle - Nuts and Bolts, a free and addictive sorting game! Train your brain by stacking nuts of the same color. Simple yet challenging, it's the perfect casual game to relax and sharpen your logic skills.",
            "keywords": ["sorting", "puzzle", "nuts", "bolts", "logic"],
            "tags": ["sorting", "logic", "brain training", "colorful", "casual"],
            "gd_game_id": "1181e80fccb44318a69756c736bfbda7"
        },
        {
            "id": "daycare-tycoon-gd",
            "title": "DayCare Tycoon",
            "category": "strategy", 
            "description": "Are you ready to build your dream business empire and be a great babysitter in this money tycoon simulator? Dive into the world of daycare games and experience the joy of managing your own thriving idle tycoon games.",
            "keywords": ["tycoon", "daycare", "management", "business", "simulation"],
            "tags": ["tycoon", "management", "business", "simulation", "idle"],
            "gd_game_id": "d9f930a985ba4d2fb94100f6daee6b8"
        },
        {
            "id": "stickman-gun-shooter-gd",
            "title": "Stickman Gun Shooter",
            "category": "action",
            "description": "Get ready to dive into a unique shooting experience with Stickman Gun Shooter! Control an expert shooter as you use a spinning gun to defeat Stickmans. The game combines realistic ragdoll physics with exciting gameplay.",
            "keywords": ["stickman", "shooter", "gun", "ragdoll", "physics"],
            "tags": ["stickman", "shooting", "physics", "action", "ragdoll"],
            "gd_game_id": "2e53f90d22e74cef93eb9ac353315cd"
        },
        {
            "id": "spider-solitaire-gd",
            "title": "Spider Solitaire",
            "category": "cards",
            "description": "Challenge yourself with this captivating solitaire inspired by the classic Spider card game! Arrange all the cards on the table into complete sequences of the same suit (from King to Ace), testing your logic, strategy, and patience.",
            "keywords": ["spider", "solitaire", "cards", "strategy", "classic"],
            "tags": ["solitaire", "cards", "strategy", "classic", "patience"],
            "gd_game_id": "1f86f0a810f9496d80c703123fc4472"
        },
        {
            "id": "horror-playtime-escape-gd",
            "title": "Horror Playtime Room Escape",
            "category": "puzzle",
            "description": "Challenge your brain to break through the fog of horror. Enter a mysterious story where you're trapped in horrible rooms full of puzzles. Use your brain to solve hidden things and uncover the truth of horror stories.",
            "keywords": ["horror", "escape", "puzzle", "mystery", "room escape"],
            "tags": ["horror", "escape", "puzzle", "mystery", "scary"],
            "gd_game_id": "defe26a924f04941b0bac2c418af27a8"
        },
        {
            "id": "nsr-street-racing-gd",
            "title": "NSR Street Car Racing",
            "category": "action",
            "description": "Hit the Streets & Dominate the Race! Jump into heart-pounding street racing action! Customize powerful cars, master drifts, unleash nitro boosts, and challenge real players in multiplayer races and intense 1v1 duels.",
            "keywords": ["racing", "street", "cars", "multiplayer", "drift"],
            "tags": ["racing", "cars", "street", "multiplayer", "drift"],
            "gd_game_id": "d632553ef7264d99aa4383100073a6dc3"
        },
        {
            "id": "save-the-daddy-gd", 
            "title": "Save the Daddy",
            "category": "puzzle",
            "description": "Get ready to unlock a world of tricky puzzles and brain teasers in Save the Daddy. Pull the pin in the right order and help the man escape from dangerous monsters & obstacles safely and thoughtfully.",
            "keywords": ["puzzle", "pin", "rescue", "brain teaser", "logic"],
            "tags": ["puzzle", "rescue", "pin pulling", "brain teaser", "logic"],
            "gd_game_id": "9cc53fd9cbba4dc8bcb40f72fd9325cf"
        },
        {
            "id": "geometry-arrow-2-gd",
            "title": "Geometry Arrow 2",  
            "category": "action",
            "description": "Geometry Arrow 2 is the fast-paced sequel to the original rhythm arcade hit! Navigate through 6 dynamic levels, dodging obstacles that move to the beat. Switch between the Arrow and the all-new Wheel character.",
            "keywords": ["geometry", "arrow", "rhythm", "arcade", "music"],
            "tags": ["rhythm", "arcade", "geometry", "music", "obstacles"],
            "gd_game_id": "93ec13ded90f4ef8b46b91f765494scd"
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
    backup_file = f"data/games_backup_batch_gd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Backup failed: {e}")
        return
    
    # Add new games
    current_games = len(games_data["games"])
    added_count = 0
    
    for new_game in new_games:
        # Check if game already exists
        exists = any(game["id"] == new_game["id"] for game in games_data["games"])
        if exists:
            print(f"Skipping {new_game['id']} - already exists")
            continue
            
        # Create full game entry
        now = datetime.now(timezone.utc).isoformat()
        game_entry = {
            "id": new_game["id"],
            "title": new_game["title"],
            "description": new_game["description"],
            "shortDesc": new_game["description"].split('.')[0] + '.' if '.' in new_game["description"] else new_game["description"][:100] + '...',
            "keywords": new_game["keywords"],
            "category": new_game["category"],
            "tags": new_game["tags"],
            "iframeUrl": f"https://html5.gamedistribution.com/{new_game['gd_game_id']}/?gd_sdk_referrer_url=https://usgamehub.icu/game.html?id={new_game['id']}",
            "thumbnail": f"/assets/images/{new_game['id']}-thumbnail.jpg",
            "rating": 4.5,
            "playCount": 0,
            "featured": False,
            "regionBlock": [],
            "controls": "Follow on-screen instructions or use keyboard/mouse controls",
            "tips": "Read the game instructions before starting for better gameplay experience",
            "createdAt": now,
            "updatedAt": now,
            "embeddable": True,
            "verified_date": datetime.now().strftime('%Y-%m-%d'),
            "license": "commercial_allowed",
            "commercial_use": True,
            "ad_allowed": True,
            "source_url": f"https://gamedistribution.com/games/{new_game['id']}/",
            "provider": "gamedistribution"
        }
        
        # Add to games list
        games_data["games"].append(game_entry)
        added_count += 1
        print(f"Added: {new_game['title']}")
    
    # Update metadata
    games_data["totalCount"] = len(games_data["games"])
    games_data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    games_data["version"] = "2.3-gamedistribution-batch"
    
    # Save updated data
    try:
        with open("data/games.json", 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"\nSuccess! Added {added_count} new GameDistribution games")
        print(f"Total games: {current_games} -> {len(games_data['games'])}")
        print("\nNext steps:")
        print("1. Run health check to verify all games work")
        print("2. Update Snake and Tic-Tac-Toe placeholders with real games")
        print("3. Test the games on your website")
    except Exception as e:
        print(f"Save failed: {e}")

if __name__ == "__main__":
    main()