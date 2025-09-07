#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean Schema Conflicts
Remove fields not defined in the JSON Schema from games.json
"""

import json
from datetime import datetime

def clean_conflicting_fields():
    """Remove fields that are not in the JSON Schema"""
    
    # Fields to remove (not in schema)
    fields_to_remove = ['source', 'discovered_date', 'verified']
    
    # Load current games data
    with open('data/games.json', 'r', encoding='utf-8') as f:
        games_data = json.load(f)
    
    print(f"Processing {len(games_data['games'])} games...")
    
    cleaned_count = 0
    for game in games_data['games']:
        cleaned_fields = []
        
        for field in fields_to_remove:
            if field in game:
                del game[field]
                cleaned_fields.append(field)
        
        if cleaned_fields:
            print(f"Cleaned {game['title']}: removed {cleaned_fields}")
            cleaned_count += 1
    
    # Update metadata
    games_data['lastUpdated'] = datetime.now().isoformat()
    games_data['note'] = f"Schema compliance: removed conflicting fields from {cleaned_count} games"
    
    # Save cleaned data
    with open('data/games.json', 'w', encoding='utf-8') as f:
        json.dump(games_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Cleaned {cleaned_count} games")
    print("Removed fields: source, discovered_date, verified")
    print("Games database is now schema compliant")

if __name__ == "__main__":
    clean_conflicting_fields()