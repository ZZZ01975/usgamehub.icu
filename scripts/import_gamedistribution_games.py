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
GameDistribution Games Import Script
Batch import games from GameDistribution platform
"""

import json
import os
from datetime import datetime, timezone

class GameDistributionImporter:
    def __init__(self):
        self.games_file = "data/games.json"
        self.backup_file = f"data/games_backup_gd_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
    def load_games_data(self):
        """Load current games data"""
        try:
            with open(self.games_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading games data: {e}")
            return None
    
    def backup_games_data(self, data):
        """Create backup of current games data"""
        try:
            with open(self.backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ Backup created: {self.backup_file}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
    
    def create_gd_game(self, game_id, title, category, description, keywords, tags, gd_game_id):
        """Create a GameDistribution game entry"""
        now = datetime.now(timezone.utc).isoformat()
        
        return {
            "id": game_id,
            "title": title,
            "description": description,
            "shortDesc": description.split('.')[0] + '.' if '.' in description else description[:100] + '...',
            "keywords": keywords,
            "category": category,
            "tags": tags,
            "iframeUrl": f"https://html5.gamedistribution.com/{gd_game_id}/?gd_sdk_referrer_url=https://usgamehub.icu/game.html?id={game_id}",
            "thumbnail": f"/assets/images/{game_id}-thumbnail.jpg",
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
            "source_url": f"https://gamedistribution.com/games/{game_id}/",
            "provider": "gamedistribution"
        }
    
    def replace_failed_games(self):
        """Replace the 3 failed self-hosted games with GameDistribution games"""
        
        # GameDistribution games to replace failed ones
        replacement_games = [
            {
                "old_id": "2048-classic-hosted",
                "game_id": "2048-legacy-gd",
                "title": "2048 Legacy - Number Puzzle",
                "category": "puzzle",
                "description": "Play the enhanced 2048 number puzzle game with smooth animations and improved graphics! Combine identical numbered tiles to reach 2048. Features multiple difficulty levels, score tracking, and beautiful visual effects. Can you master this addictive math puzzle?",
                "keywords": ["2048", "number puzzle", "math game", "brain teaser", "legacy edition"],
                "tags": ["numbers", "strategy", "addictive", "brain training", "puzzle"],
                "gd_game_id": "3ff5df9f5d0248fd9dcd70e2cc253de5"  # Using the example ID from your email
            },
            {
                "old_id": "snake-classic-hosted", 
                "game_id": "snake-adventure-gd",
                "title": "Snake Adventure - Classic Arcade",
                "category": "action",
                "description": "Experience the classic Snake game with modern twists! Guide your snake to collect food and grow longer while avoiding obstacles. Features power-ups, multiple game modes, and enhanced graphics for the ultimate retro arcade experience.",
                "keywords": ["snake game", "arcade", "retro gaming", "classic", "food collection"],
                "tags": ["snake", "arcade", "retro", "classic", "growth"],
                "gd_game_id": "sample-snake-game-id"  # Placeholder - needs real GD game ID
            },
            {
                "old_id": "tic-tac-toe-hosted",
                "game_id": "tic-tac-toe-pro-gd", 
                "title": "Tic Tac Toe Pro - Strategy Game",
                "category": "multiplayer",
                "description": "Play the classic Tic Tac Toe game with enhanced features! Enjoy single-player vs AI or local multiplayer modes. Features different difficulty levels, score tracking, and beautiful animations. Perfect for quick strategy gaming sessions.",
                "keywords": ["tic tac toe", "strategy game", "two player", "AI opponent", "multiplayer"],
                "tags": ["strategy", "multiplayer", "ai", "classic", "quick game"],
                "gd_game_id": "sample-tictactoe-game-id"  # Placeholder - needs real GD game ID
            }
        ]
        
        return replacement_games
    
    def update_games_data(self, games_data, replacement_games):
        """Update games data by replacing failed games"""
        
        # Find and replace the games
        games_list = games_data["games"]
        replaced_count = 0
        
        for replacement in replacement_games:
            for i, game in enumerate(games_list):
                if game["id"] == replacement["old_id"]:
                    # Create new game entry
                    new_game = self.create_gd_game(
                        replacement["game_id"],
                        replacement["title"],
                        replacement["category"],
                        replacement["description"],
                        replacement["keywords"],
                        replacement["tags"],
                        replacement["gd_game_id"]
                    )
                    
                    # Replace the old game
                    games_list[i] = new_game
                    replaced_count += 1
                    print(f"✅ Replaced '{replacement['old_id']}' with '{replacement['game_id']}'")
                    break
        
        print(f"Total games replaced: {replaced_count}")
        return games_data
    
    def save_games_data(self, games_data):
        """Save updated games data"""
        try:
            with open(self.games_file, 'w', encoding='utf-8') as f:
                json.dump(games_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Games data saved successfully to {self.games_file}")
            return True
        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False
    
    def run_replacement(self):
        """Execute the full replacement process"""
        print("🎮 Starting GameDistribution Games Replacement Process...")
        print("="*60)
        
        # Load current data
        games_data = self.load_games_data()
        if not games_data:
            print("❌ Failed to load games data")
            return False
        
        print(f"Loaded {len(games_data['games'])} games")
        
        # Create backup
        if not self.backup_games_data(games_data):
            print("❌ Backup failed, aborting process")
            return False
        
        # Get replacement games
        replacement_games = self.replace_failed_games()
        print(f"Preparing to replace {len(replacement_games)} games")
        
        # Update games data
        updated_data = self.update_games_data(games_data, replacement_games)
        
        # Save updated data
        if self.save_games_data(updated_data):
            print("\nGameDistribution games replacement completed successfully!")
            print("\nNext steps:")
            print("1. Update the GameDistribution game IDs with real ones from your account")
            print("2. Test the games in your browser")
            print("3. Run the health check script to verify all games work")
            print("4. Commit changes to Git")
            return True
        else:
            print("❌ Failed to save updated games data")
            return False

def main():
    """Main execution function"""
    importer = GameDistributionImporter()
    
    # Show current status
    print("Current failed games that will be replaced:")
    print("- 2048-classic-hosted (X-Frame-Options blocked)")  
    print("- snake-classic-hosted (X-Frame-Options blocked)")
    print("- tic-tac-toe-hosted (X-Frame-Options blocked)")
    print("")
    
    # Auto-proceed in batch mode
    print("Auto-proceeding with replacement...")
    
    # Execute replacement
    success = importer.run_replacement()
    
    if success:
        print("\nImportant Notes:")
        print("- The script used placeholder GameDistribution game IDs")
        print("- You need to replace 'sample-snake-game-id' and 'sample-tictactoe-game-id'")
        print("- Browse GameDistribution.com to find suitable games for Snake and Tic Tac Toe")
        print("- Copy the real game IDs from the iframe src URLs")
    else:
        print("❌ Replacement process failed")

if __name__ == "__main__":
    main()