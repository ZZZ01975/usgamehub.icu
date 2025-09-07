#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Integrate new games into the main games database
Safely adds verified games from discovery results
"""

import json
import os
from datetime import datetime
import glob

def load_latest_discovery_results():
    """Load the most recent game discovery results"""
    pattern = 'scripts/results/game_discovery_*.json'
    discovery_files = glob.glob(pattern)
    
    if not discovery_files:
        print("No discovery results found. Run game_discovery.py first.")
        return None
    
    # Get the most recent file
    latest_file = max(discovery_files, key=os.path.getmtime)
    print(f"Loading discovery results from: {latest_file}")
    
    try:
        with open(latest_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading discovery results: {e}")
        return None

def load_current_games():
    """Load current games database"""
    try:
        with open('data/games.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading games database: {e}")
        return None

def check_for_duplicates(current_games, new_games):
    """Check for duplicate games by ID or similar titles"""
    current_ids = set(game['id'] for game in current_games['games'])
    current_titles = set(game['title'].lower() for game in current_games['games'])
    
    unique_games = []
    duplicates = []
    
    for game in new_games:
        is_duplicate = False
        
        # Check ID duplication
        if game['id'] in current_ids:
            duplicates.append((game, f"ID '{game['id']}' already exists"))
            is_duplicate = True
        
        # Check title similarity
        elif game['title'].lower() in current_titles:
            duplicates.append((game, f"Similar title '{game['title']}' already exists"))
            is_duplicate = True
        
        if not is_duplicate:
            unique_games.append(game)
    
    return unique_games, duplicates

def integrate_games(current_games, new_games, max_additions=5):
    """Integrate new games into the current database"""
    print(f"Integrating up to {max_additions} new games...")
    
    # Check for duplicates
    unique_games, duplicates = check_for_duplicates(current_games, new_games)
    
    if duplicates:
        print(f"\nSkipping {len(duplicates)} duplicate games:")
        for game, reason in duplicates:
            print(f"  - {game['title']}: {reason}")
    
    # Limit additions
    games_to_add = unique_games[:max_additions]
    
    if not games_to_add:
        print("No new games to add after duplicate check.")
        return current_games, []
    
    print(f"\nAdding {len(games_to_add)} new games:")
    for game in games_to_add:
        print(f"  - {game['title']} ({game['category']})")
    
    # Add new games to the database
    updated_games = current_games.copy()
    updated_games['games'].extend(games_to_add)
    
    # Update metadata
    updated_games['totalCount'] = len(updated_games['games'])
    updated_games['lastUpdated'] = datetime.now().isoformat()
    updated_games['version'] = f"{current_games.get('version', '2.1')}-expanded"
    
    # Update note
    added_titles = [game['title'] for game in games_to_add]
    updated_games['note'] = f"Added {len(games_to_add)} new games: {', '.join(added_titles[:3])}{'...' if len(games_to_add) > 3 else ''}"
    
    return updated_games, games_to_add

def backup_current_games():
    """Create a backup of the current games database"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'data/games_backup_before_expansion_{timestamp}.json'
    
    try:
        with open('data/games.json', 'r', encoding='utf-8') as src:
            with open(backup_file, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        print(f"Backup created: {backup_file}")
        return backup_file
    except Exception as e:
        print(f"Warning: Could not create backup: {e}")
        return None

def save_updated_games(updated_games):
    """Save the updated games database"""
    try:
        with open('data/games.json', 'w', encoding='utf-8') as f:
            json.dump(updated_games, f, indent=2, ensure_ascii=False)
        print("Games database updated successfully!")
        return True
    except Exception as e:
        print(f"Error saving updated games: {e}")
        return False

def generate_integration_report(added_games):
    """Generate a report of the integration process"""
    if not added_games:
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'scripts/results/integration_report_{timestamp}.txt'
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("GAME INTEGRATION REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Games Added: {len(added_games)}\n\n")
        
        f.write("NEW GAMES:\n")
        f.write("-" * 20 + "\n")
        for i, game in enumerate(added_games, 1):
            f.write(f"{i}. {game['title']}\n")
            f.write(f"   ID: {game['id']}\n")
            f.write(f"   Category: {game['category']}\n")
            f.write(f"   URL: {game['iframeUrl']}\n")
            f.write(f"   License: {game.get('license', 'Unknown')}\n")
            f.write(f"   Commercial Use: {game.get('commercial_use', 'Unknown')}\n")
            f.write(f"   Source: {game.get('source', 'Unknown')}\n\n")
        
        f.write("CATEGORIES DISTRIBUTION:\n")
        f.write("-" * 25 + "\n")
        categories = {}
        for game in added_games:
            cat = game['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for category, count in categories.items():
            f.write(f"{category}: {count} games\n")
    
    print(f"Integration report saved: {report_file}")

def main():
    if not os.path.exists('data/games.json'):
        print("Error: Please run from project root directory")
        return 1
    
    print("=" * 60)
    print("GAME INTEGRATION SYSTEM")
    print("=" * 60)
    
    # Load discovery results
    discovery_results = load_latest_discovery_results()
    if not discovery_results:
        return 1
    
    verified_games = [game for game in discovery_results['discovered_games'] if game.get('verified', False)]
    
    if not verified_games:
        print("No verified games found in discovery results.")
        return 1
    
    print(f"Found {len(verified_games)} verified games ready for integration")
    
    # Load current games database
    current_games = load_current_games()
    if not current_games:
        return 1
    
    print(f"Current games database has {len(current_games['games'])} games")
    
    # Create backup
    backup_file = backup_current_games()
    
    # Integrate games
    updated_games, added_games = integrate_games(current_games, verified_games, max_additions=5)
    
    if not added_games:
        print("No games were added. Integration complete.")
        return 0
    
    # Save updated database
    if save_updated_games(updated_games):
        print("\n" + "=" * 60)
        print("INTEGRATION COMPLETE")
        print("=" * 60)
        print(f"Games added: {len(added_games)}")
        print(f"Total games: {updated_games['totalCount']}")
        print(f"Database version: {updated_games.get('version', 'Unknown')}")
        
        # Generate report
        generate_integration_report(added_games)
        
        print(f"\n🎉 Successfully expanded game library!")
        print("Run the health check script to verify all games are working.")
        
        return 0
    else:
        print("Failed to save updated games database.")
        return 1

if __name__ == "__main__":
    exit(main())