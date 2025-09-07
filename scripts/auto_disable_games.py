#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auto-disable games script for US Game Hub
Automatically disables games that fail health checks repeatedly
"""

import json
import os
from datetime import datetime, timedelta

class AutoGameDisabler:
    def __init__(self):
        self.failure_threshold = int(os.getenv('FAILURE_THRESHOLD', '3'))
        self.games_file = 'data/games.json'
        self.inactive_file = 'data/inactive_games.json'
        self.results_dir = 'scripts/results'
        
    def load_games_data(self):
        """Load current games data"""
        try:
            with open(self.games_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: {self.games_file} not found")
            return None
    
    def load_inactive_data(self):
        """Load or create inactive games data"""
        if os.path.exists(self.inactive_file):
            try:
                with open(self.inactive_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        
        # Create new inactive games structure
        return {
            'inactive_games': [],
            'failure_history': {},
            'last_updated': datetime.now().isoformat(),
            'auto_disable_threshold': self.failure_threshold
        }
    
    def get_latest_health_results(self):
        """Get the latest health check results"""
        today = datetime.now().strftime('%Y%m%d')
        results_file = f'{self.results_dir}/summary_{today}.json'
        
        if os.path.exists(results_file):
            try:
                with open(results_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                pass
        
        print(f"Warning: No recent health check results found at {results_file}")
        return None
    
    def update_failure_history(self, inactive_data, health_results):
        """Update failure history for games"""
        if not health_results:
            return inactive_data
        
        # Get failed games from latest results
        failed_games = health_results.get('unavailable_games', [])
        available_games = health_results.get('available_games', [])
        
        # Reset failure count for games that are now working
        for game in available_games:
            game_id = game.get('id')
            if game_id in inactive_data['failure_history']:
                print(f"Game {game_id} is now working - resetting failure count")
                inactive_data['failure_history'][game_id] = {
                    'count': 0,
                    'last_success': datetime.now().isoformat(),
                    'last_failure': None
                }
        
        # Update failure count for failed games
        for game in failed_games:
            game_id = game.get('id')
            if game_id not in inactive_data['failure_history']:
                inactive_data['failure_history'][game_id] = {
                    'count': 0,
                    'first_failure': None,
                    'last_failure': None,
                    'last_success': None
                }
            
            # Increment failure count
            failure_info = inactive_data['failure_history'][game_id]
            failure_info['count'] += 1
            failure_info['last_failure'] = datetime.now().isoformat()
            
            if failure_info['first_failure'] is None:
                failure_info['first_failure'] = datetime.now().isoformat()
            
            print(f"Game {game_id} failed ({failure_info['count']}/{self.failure_threshold}): {game.get('reason', 'Unknown error')}")
        
        return inactive_data
    
    def disable_failed_games(self, games_data, inactive_data):
        """Disable games that exceed failure threshold"""
        if not games_data:
            return games_data, inactive_data, []
        
        disabled_games = []
        active_games = []
        
        for game in games_data['games']:
            game_id = game['id']
            failure_info = inactive_data['failure_history'].get(game_id, {})
            failure_count = failure_info.get('count', 0)
            
            if failure_count >= self.failure_threshold:
                # Move to inactive list
                disabled_game = {
                    'id': game_id,
                    'title': game['title'],
                    'category': game['category'],
                    'disabled_date': datetime.now().isoformat(),
                    'failure_count': failure_count,
                    'last_failure_reason': failure_info.get('reason', 'Multiple failures'),
                    'original_data': game  # Keep original data for potential restoration
                }
                
                inactive_data['inactive_games'].append(disabled_game)
                disabled_games.append(disabled_game)
                
                print(f"[DISABLED] {game['title']} - {failure_count} consecutive failures")
                
            else:
                # Keep active
                active_games.append(game)
        
        # Update games data with only active games
        if disabled_games:
            games_data['games'] = active_games
            games_data['totalCount'] = len(active_games)
            games_data['lastUpdated'] = datetime.now().isoformat()
            games_data['version'] = f"{games_data.get('version', '2.1')}-auto-cleaned"
            
            # Add note about auto-disabled games
            disabled_titles = [g['title'] for g in disabled_games]
            games_data['note'] = f"Auto-disabled {len(disabled_games)} games due to repeated failures: {', '.join(disabled_titles[:3])}{'...' if len(disabled_games) > 3 else ''}"
        
        inactive_data['last_updated'] = datetime.now().isoformat()
        
        return games_data, inactive_data, disabled_games
    
    def save_data(self, games_data, inactive_data):
        """Save updated data files"""
        # Save games data
        if games_data:
            with open(self.games_file, 'w', encoding='utf-8') as f:
                json.dump(games_data, f, indent=2, ensure_ascii=False)
        
        # Save inactive data
        with open(self.inactive_file, 'w', encoding='utf-8') as f:
            json.dump(inactive_data, f, indent=2, ensure_ascii=False)
    
    def process(self):
        """Main processing function"""
        print("Starting auto-disable games process...")
        print(f"Failure threshold: {self.failure_threshold}")
        
        # Load data
        games_data = self.load_games_data()
        inactive_data = self.load_inactive_data()
        health_results = self.get_latest_health_results()
        
        if not games_data:
            print("Error: Could not load games data")
            return False
        
        print(f"Loaded {len(games_data['games'])} active games")
        print(f"Loaded {len(inactive_data.get('inactive_games', []))} previously inactive games")
        
        # Update failure history
        inactive_data = self.update_failure_history(inactive_data, health_results)
        
        # Disable games that exceed threshold
        original_count = len(games_data['games'])
        games_data, inactive_data, disabled_games = self.disable_failed_games(games_data, inactive_data)
        
        # Save updated data
        self.save_data(games_data, inactive_data)
        
        # Print summary
        print("\n" + "=" * 50)
        print("AUTO-DISABLE PROCESS COMPLETE")
        print("=" * 50)
        print(f"Original active games: {original_count}")
        print(f"Final active games: {len(games_data['games'])}")
        print(f"Games disabled this run: {len(disabled_games)}")
        print(f"Total inactive games: {len(inactive_data['inactive_games'])}")
        
        if disabled_games:
            print("\nDisabled games:")
            for game in disabled_games:
                print(f"  - {game['title']} ({game['category']})")
        
        # Check if we're running low on games
        if len(games_data['games']) < 5:
            print(f"\n⚠️  WARNING: Only {len(games_data['games'])} active games remaining!")
            print("Consider adding new games or investigating failures.")
        
        return len(disabled_games) > 0

def main():
    if not os.path.exists('data/games.json'):
        print("Warning: data/games.json not found in current directory")
        print("Attempting to find the file...")
        
        # 尝试寻找正确的路径
        possible_paths = [
            'data/games.json',
            '../data/games.json',
            '../../data/games.json',
            './data/games.json'
        ]
        
        found = False
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Found games.json at: {path}")
                # 切换到包含data目录的目录
                if '/' in path:
                    os.chdir(os.path.dirname(path.replace('/data/games.json', '')))
                found = True
                break
        
        if not found:
            print("Error: Could not locate data/games.json file")
            print("Current directory:", os.getcwd())
            print("Directory contents:", os.listdir('.'))
            return 1
    
    disabler = AutoGameDisabler()
    changes_made = disabler.process()
    
    # Return exit code based on whether changes were made
    return 0

if __name__ == "__main__":
    exit(main())