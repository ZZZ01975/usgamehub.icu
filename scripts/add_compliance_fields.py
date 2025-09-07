#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add compliance fields to existing games
Updates games.json with license, commercial_use, ad_allowed, source_url fields
"""

import json
from datetime import datetime

def add_compliance_fields():
    """Add compliance fields to all games in the database"""
    
    # Load current games data
    with open('data/games.json', 'r', encoding='utf-8') as f:
        games_data = json.load(f)
    
    print(f"Loading {len(games_data['games'])} games...")
    
    # Define compliance data for each game
    compliance_mapping = {
        'monster-survivors': {
            'license': 'unknown',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://cloud.onlinegames.io'
        },
        '2048-game': {
            'license': 'unknown',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://2048game.com'
        },
        'bubble-shooter': {
            'license': 'unknown',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://bubbleshooter.net'
        },
        'endless-runner': {
            'license': 'unknown',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://html5games.com'
        },
        'racing-car': {
            'license': 'unknown',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://html5games.com'
        },
        'racing-rivals': {
            'license': 'unknown',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://html5games.com'
        },
        '2048-classic-hosted': {
            'license': 'MIT',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://github.com/gabrielecirulli/2048'
        },
        'snake-classic-hosted': {
            'license': 'MIT',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'https://github.com/patorjk/JavaScript-Snake'
        },
        'tic-tac-toe-hosted': {
            'license': 'custom',
            'commercial_use': True,
            'ad_allowed': True,
            'source_url': 'custom_implementation'
        }
    }
    
    # Update each game with compliance fields
    updated_count = 0
    for game in games_data['games']:
        game_id = game['id']
        
        if game_id in compliance_mapping:
            compliance_data = compliance_mapping[game_id]
            
            # Add compliance fields
            game['license'] = compliance_data['license']
            game['commercial_use'] = compliance_data['commercial_use']
            game['ad_allowed'] = compliance_data['ad_allowed']
            game['source_url'] = compliance_data['source_url']
            
            print(f"Updated: {game['title']} - License: {compliance_data['license']}")
            updated_count += 1
        else:
            print(f"Warning: No compliance data for game ID: {game_id}")
    
    # Update metadata
    games_data['lastUpdated'] = datetime.now().isoformat()
    games_data['version'] = "2.2-compliance-ready"
    games_data['note'] = f"Added compliance fields (license, commercial_use, ad_allowed) to all {updated_count} games"
    
    # Save updated games data
    with open('data/games.json', 'w', encoding='utf-8') as f:
        json.dump(games_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Compliance fields added to {updated_count} games")
    print("📝 Games database is now ready for AdSense audit!")
    
    # Print summary by license type
    license_summary = {}
    for game in games_data['games']:
        license_type = game.get('license', 'unknown')
        license_summary[license_type] = license_summary.get(license_type, 0) + 1
    
    print("\n📊 License Distribution:")
    for license_type, count in license_summary.items():
        print(f"  - {license_type}: {count} games")
    
    # Print commercial usage status
    commercial_games = sum(1 for game in games_data['games'] if game.get('commercial_use', False))
    ad_allowed_games = sum(1 for game in games_data['games'] if game.get('ad_allowed', False))
    
    print(f"\n🏢 Commercial Status:")
    print(f"  - Commercial use allowed: {commercial_games}/{len(games_data['games'])} games")
    print(f"  - Ads allowed: {ad_allowed_games}/{len(games_data['games'])} games")

if __name__ == "__main__":
    add_compliance_fields()