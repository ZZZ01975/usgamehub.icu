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
Update GameDistribution games with correct IDs from EMBED.md
This will fix the 404 errors by using the actual game IDs from GameDistribution platform
"""

import json
from datetime import datetime, timezone

def main():
    print("Updating GameDistribution Games with Correct IDs")
    print("="*55)
    
    # Correct game data from EMBED.md
    game_updates = [
        {
            "id": "buckshot-roulette-gd",
            "correct_gd_id": "87c6432822364f3f8ac0dddfcb41611e",
            "title": "Buckshot Roulette",
            "category": "action",
            "description": "Do you dare to bet your life on an exciting roulette wheel showdown? Buckshot Roulette is a gun simulator that combines strategy, shooting and survival. Instead of a pistol, a powerful shotgun was used. Every pull of the trigger is a choice of fate. The winner lives, the loser dies. You will begin a Turn-Based shooting roulette game. Each round will have a fixed number of bullets and blanks.",
            "controls": "Mouse click or tap to play",
            "keywords": ["buckshot", "roulette", "gun", "survival", "strategy", "turn-based"],
            "tags": ["shooting", "survival", "strategy", "roulette", "intense", "turn-based"]
        },
        {
            "id": "daycare-tycoon-gd", 
            "correct_gd_id": "d9f930a985ba4d2fb94100f6daeee6b8",
            "title": "DayCare Tycoon",
            "category": "strategy",
            "description": "Are you ready to build your dream business empire and be a great babysitter in this money tycoon simulator? Dive into the world of daycare games and experience the joy of managing your own thriving idle tycoon games. From welcoming adorable babies to creating a safe and happy environment, this game offers everything you need to grow your daycare business into a successful venture.",
            "controls": "Your daycare business awaits – take care of a baby and become a rich babysitter in this daycare games!",
            "keywords": ["tycoon", "daycare", "management", "business", "simulation", "idle"],
            "tags": ["tycoon", "management", "business", "simulation", "idle", "babies"]
        },
        {
            "id": "stickman-gun-shooter-gd",
            "correct_gd_id": "2e53f90d22e74cef93eb9ac3533155cd", 
            "title": "Stickman Gun Shooter",
            "category": "action",
            "description": "Get ready to dive into a unique shooting experience with Stickman Gun Shooter! Enjoy an experience that invites you to take control of an expert shooter as you use a spinning gun to defeat fun Stickmans. The game combines realistic ragdoll physics with exciting and simple gameplay - your goal will be to destroy the yellow Stickmans that get in your way, overcoming different levels with different challenges and obstacles, while demonstrating your sniper skills!",
            "controls": "Easy to understand; Nice and addictive gameplay; Shooter Physics; Awesome HD Graphics; Challenging levels, Use the mouse or touch to play",
            "keywords": ["stickman", "shooter", "gun", "ragdoll", "physics", "sniper"],
            "tags": ["stickman", "shooting", "physics", "action", "ragdoll", "sniper"]
        },
        {
            "id": "spider-solitaire-gd",
            "correct_gd_id": "1f86f0a810f9496d80c7031238fc4472",
            "title": "Spider Solitaire", 
            "category": "cards",
            "description": "Challenge yourself with this captivating solitaire inspired by the classic Spider card game! Arrange all the cards on the table into complete sequences of the same suit (from King to Ace), testing your logic, strategy, and patience. Choose your difficulty level, play with one, two, or all four suits, and prove your skills with the deck. Every move counts—can you complete all the sequences before running out of options?",
            "controls": "The goal is to complete descending sequences of the same suit, from King to Ace. You can move cards or stacks in descending order, even if they are of different suits. Once a complete sequence of the same suit is formed, it will be removed from the table. If no moves are available, deal new cards by tapping the deck at the top. Choose your difficulty: - Easy: 1 suit - Medium: 2 suits - Hard: 4 suits Complete all sequences to win the game!",
            "keywords": ["spider", "solitaire", "cards", "strategy", "classic", "patience"],
            "tags": ["solitaire", "cards", "strategy", "classic", "patience", "spider"]
        },
        {
            "id": "nsr-street-racing-gd",
            "correct_gd_id": "d632553ef7264d99aa438310073a6dc3",
            "title": "NSR Street Car Racing",
            "category": "action", 
            "description": "Hit the Streets & Dominate the Race! Jump into heart-pounding street racing action! Customize powerful cars, master drifts, unleash nitro boosts, and challenge real players in multiplayer races and intense 1v1 duels. Become a street-racing legend! Ready, Set, Drift!",
            "controls": "Game Controls: • Steer: Use A/D or Left/Right Arrow keys to steer. • Accelerate: Hold W or Up Arrow to speed up. • Brake/Reverse: Press S or Down Arrow to brake or reverse. • Drift: Tap and hold Spacebar for stylish drifting around corners. • Nitro Boost: Press Shift for an explosive burst of speed! Get behind the wheel and dominate the streets!",
            "keywords": ["racing", "street", "cars", "multiplayer", "drift", "nitro"],
            "tags": ["racing", "cars", "street", "multiplayer", "drift", "nitro"]
        },
        {
            "id": "geometry-arrow-2-gd",
            "correct_gd_id": "93ec13ded90f4ef8b46b91f7654945cd",
            "title": "Geometry Arrow 2",
            "category": "action",
            "description": "Geometry Arrow 2 is the fast-paced sequel to the original rhythm arcade hit! Navigate through 6 dynamic levels, dodging obstacles that move to the beat. Switch between the Arrow and the all-new Wheel character, each with unique mechanics. Unlock achievements and customize your Arrow and Wheel with different skins, particles, and block textures. Time your moves, feel the rhythm, and reach the portal in perfect sync!",
            "controls": "Goal: Reach the portal without crashing into obstacles. How to play: Select any of the 6 levels from the main menu. Tap/click at the right moment to dodge obstacles in sync with the music. Each level includes both Arrow and Wheel segments. Controls: PC Press SPACEBAR or LEFT MOUSE BUTTON to move or jump. Press ESC to exit the level. Mobile Tap the screen to move or jump in rhythm. Quick reactions and precise timing are key to success!",
            "keywords": ["geometry", "arrow", "rhythm", "arcade", "music", "obstacles"],
            "tags": ["rhythm", "arcade", "geometry", "music", "obstacles", "beat"]
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
    backup_file = f"data/games_backup_id_fixes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"Backup created: {backup_file}")
    except Exception as e:
        print(f"Backup failed: {e}")
        return
    
    # Update games with correct IDs and enhanced information
    updated_count = 0
    
    for update_info in game_updates:
        for game in games_data["games"]:
            if game["id"] == update_info["id"]:
                # Update game ID in URL
                old_url = game.get("iframeUrl", "")
                new_url = f"https://html5.gamedistribution.com/{update_info['correct_gd_id']}/?gd_sdk_referrer_url=https://usgamehub.icu/game.html?id={update_info['id']}"
                
                # Update all fields
                game["iframeUrl"] = new_url
                game["title"] = update_info["title"]
                game["description"] = update_info["description"]
                game["controls"] = update_info["controls"]
                game["keywords"] = update_info["keywords"]
                game["tags"] = update_info["tags"]
                game["category"] = update_info["category"]
                game["shortDesc"] = update_info["description"].split('.')[0] + '.' if '.' in update_info["description"] else update_info["description"][:100] + '...'
                game["updatedAt"] = datetime.now(timezone.utc).isoformat()
                
                print(f"Updated {update_info['title']}: {update_info['correct_gd_id']}")
                updated_count += 1
                break
    
    # Update metadata
    games_data["lastUpdated"] = datetime.now(timezone.utc).isoformat()
    games_data["version"] = "2.4-corrected-gamedistribution-ids"
    games_data["note"] = f"Fixed {updated_count} GameDistribution game IDs with correct values from EMBED.md"
    
    # Save updated data
    try:
        with open("data/games.json", 'w', encoding='utf-8') as f:
            json.dump(games_data, f, indent=2, ensure_ascii=False)
        print(f"\nSuccess! Updated {updated_count} GameDistribution games with correct IDs")
        print("\nUpdated games:")
        for update in game_updates:
            print(f"  - {update['title']}: {update['correct_gd_id']}")
        print("\nNext steps:")
        print("1. Run health check to verify all games now work")
        print("2. Test games on your website")
        print("3. Continue adding more games using EMBED.md format")
    except Exception as e:
        print(f"Save failed: {e}")

if __name__ == "__main__":
    main()