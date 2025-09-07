#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate health report for GitHub Actions
Creates markdown report of game health status
"""

import json
import os
from datetime import datetime

def load_json_file(filepath):
    """Safely load JSON file"""
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return None

def generate_health_report():
    """Generate comprehensive health report in markdown format"""
    
    # Load data files
    games_data = load_json_file('data/games.json')
    inactive_data = load_json_file('data/inactive_games.json')
    
    # Get latest health results
    today = datetime.now().strftime('%Y%m%d')
    health_results = load_json_file(f'scripts/results/summary_{today}.json')
    analytics_report = load_json_file(f'scripts/results/analytics_report_{today}.json')
    
    # Start building report
    report = []
    report.append("# Weekly Game Health Report")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    report.append("")
    
    # === SUMMARY SECTION ===
    report.append("## Summary")
    if games_data and health_results:
        total_active = len(games_data['games'])
        total_inactive = len(inactive_data.get('inactive_games', [])) if inactive_data else 0
        success_rate = health_results.get('success_rate', 'N/A')
        
        report.append(f"- **Active Games:** {total_active}")
        report.append(f"- **Inactive Games:** {total_inactive}")
        report.append(f"- **Success Rate:** {success_rate}")
        report.append(f"- **Last Health Check:** {health_results.get('check_time', 'N/A')}")
    else:
        report.append("⚠️ Unable to load game data or health results")
    
    report.append("")
    
    # === HEALTH STATUS ===
    if health_results:
        report.append("## Available Games")
        available_games = health_results.get('available_games', [])
        if available_games:
            for game in available_games:
                report.append(f"- **{game['title']}** ({game['category']}) - {game.get('url', 'N/A')}")
        else:
            report.append("None")
        
        report.append("")
        
        # Failed games
        unavailable_games = health_results.get('unavailable_games', [])
        if unavailable_games:
            report.append("## Failed Games")
            for game in unavailable_games:
                reason = game.get('reason', 'Unknown error')
                report.append(f"- **{game['title']}** ({game['category']}) - `{reason}`")
            report.append("")
    
    # === RECENTLY DISABLED ===
    if inactive_data:
        recent_disabled = []
        cutoff_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        
        for game in inactive_data.get('inactive_games', []):
            try:
                disabled_date = datetime.fromisoformat(game['disabled_date'].replace('Z', '+00:00'))
                if disabled_date.date() >= cutoff_date.date():
                    recent_disabled.append(game)
            except:
                pass
        
        if recent_disabled:
            report.append("## Recently Auto-Disabled")
            for game in recent_disabled:
                failure_count = game.get('failure_count', 'Unknown')
                reason = game.get('last_failure_reason', 'Multiple failures')
                report.append(f"- **{game['title']}** - {failure_count} failures ({reason})")
            report.append("")
    
    # === ANALYTICS STATUS ===
    if analytics_report:
        report.append("## Analytics Status")
        health_checks = analytics_report.get('health_checks', {})
        tracking_analysis = analytics_report.get('tracking_analysis', {})
        
        # Health status
        all_healthy = all(health_checks.values())
        health_icon = "[OK]" if all_healthy else "[WARNING]"
        report.append(f"{health_icon} **Overall Health:** {'Good' if all_healthy else 'Needs Attention'}")
        
        # Game tracking
        if tracking_analysis:
            report.append(f"- **Tracked Games:** {tracking_analysis.get('total_games', 'N/A')}")
            report.append(f"- **Self-Hosted Games:** {tracking_analysis.get('self_hosted_games', 'N/A')}")
        
        report.append("")
    
    # === RECOMMENDATIONS ===
    report.append("## Recommendations")
    
    # Game count recommendation
    current_games = len(games_data['games']) if games_data else 0
    if current_games < 10:
        report.append(f"- **Content Expansion:** Currently {current_games} active games. Consider adding 5-10 new verified games.")
    
    # Failure pattern analysis
    if health_results:
        failure_reasons = {}
        for game in health_results.get('unavailable_games', []):
            reason = game.get('reason', 'Unknown')
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        if failure_reasons:
            most_common = max(failure_reasons.items(), key=lambda x: x[1])
            report.append(f"- **Primary Issue:** {most_common[0]} ({most_common[1]} games affected)")
    
    # Auto-disable threshold check
    if inactive_data:
        threshold = inactive_data.get('auto_disable_threshold', 3)
        report.append(f"- **Auto-Disable:** Threshold set to {threshold} consecutive failures")
    
    report.append("")
    
    # === NEXT ACTIONS ===
    report.append("## Next Actions")
    report.append("1. Review failed games for potential URL updates")
    report.append("2. Monitor auto-disabled games for service restoration")
    report.append("3. Consider adding new games if active count < 10")
    report.append("4. Run manual health check if issues persist")
    
    report.append("")
    report.append("---")
    report.append("*Generated by automated health check system*")
    
    return "\n".join(report)

def main():
    report = generate_health_report()
    print(report)

if __name__ == "__main__":
    main()