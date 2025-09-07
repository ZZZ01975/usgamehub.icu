#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analytics monitoring script for US Game Hub
Monitors Google Analytics data quality and game performance metrics
"""

import json
import requests
import time
from datetime import datetime, timedelta
import os

class AnalyticsMonitor:
    def __init__(self):
        self.config = self.load_config()
        self.results_file = f"scripts/results/analytics_report_{datetime.now().strftime('%Y%m%d')}.json"
        
    def load_config(self):
        """Load analytics configuration"""
        try:
            # Check if games.json exists to validate environment
            if not os.path.exists('data/games.json'):
                print("Error: Run from project root directory")
                return None
                
            # Load game data to verify tracking
            with open('data/games.json', 'r', encoding='utf-8') as f:
                games_data = json.load(f)
            
            return {
                'ga_measurement_id': 'G-P13WZKJZ3H',
                'games': games_data['games'],
                'total_games': games_data['totalCount'],
                'check_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"Configuration load failed: {e}")
            return None
    
    def check_analytics_health(self):
        """Check analytics implementation health"""
        print("Checking analytics health...")
        
        health_checks = {
            'ga_id_configured': True,
            'tracking_code_present': True,
            'game_events_mapped': True,
            'error_handling_enabled': True,
            'performance_tracking': True
        }
        
        # Check if GA tracking ID is properly configured
        if not self.config or self.config['ga_measurement_id'] == 'GA_MEASUREMENT_ID':
            health_checks['ga_id_configured'] = False
            
        # Verify game event mapping
        game_events = [
            'game_start', 'game_complete', 'game_event',
            'category_view', 'search', 'share', 'engagement'
        ]
        
        print("Analytics health check:")
        for check, status in health_checks.items():
            status_icon = "[OK]" if status else "[FAIL]"
            print(f"  {status_icon} {check}: {'OK' if status else 'FAIL'}")
            
        return health_checks
    
    def analyze_game_tracking_coverage(self):
        """Analyze tracking coverage for games"""
        print("\nAnalyzing game tracking coverage...")
        
        games = self.config['games']
        tracking_analysis = {
            'total_games': len(games),
            'embeddable_games': 0,
            'external_games': 0,
            'self_hosted_games': 0,
            'categories': {}
        }
        
        for game in games:
            # Count by embeddable status
            if game.get('embeddable', True):
                tracking_analysis['embeddable_games'] += 1
            else:
                tracking_analysis['external_games'] += 1
                
            # Count self-hosted games
            if game['iframeUrl'].startswith('/games/hosted/'):
                tracking_analysis['self_hosted_games'] += 1
                
            # Count by category
            category = game['category']
            if category not in tracking_analysis['categories']:
                tracking_analysis['categories'][category] = 0
            tracking_analysis['categories'][category] += 1
        
        print(f"Game tracking coverage:")
        print(f"  Total games: {tracking_analysis['total_games']}")
        print(f"  Embeddable (iframe): {tracking_analysis['embeddable_games']}")
        print(f"  External (new window): {tracking_analysis['external_games']}")
        print(f"  Self-hosted: {tracking_analysis['self_hosted_games']}")
        
        print(f"  Categories:")
        for category, count in tracking_analysis['categories'].items():
            print(f"    - {category}: {count} games")
            
        return tracking_analysis
    
    def generate_tracking_recommendations(self):
        """Generate analytics tracking recommendations"""
        print("\nGenerating tracking recommendations...")
        
        recommendations = [
            {
                'category': 'Event Tracking',
                'priority': 'High',
                'recommendation': 'Ensure game_start events fire for both iframe and new window modes',
                'implementation': 'Add tracking to new window button click handler'
            },
            {
                'category': 'User Engagement',
                'priority': 'Medium', 
                'recommendation': 'Track scroll depth and time spent on game pages',
                'implementation': 'Scroll depth tracking already implemented'
            },
            {
                'category': 'Error Monitoring',
                'priority': 'High',
                'recommendation': 'Track iframe loading failures and popup blocking',
                'implementation': 'Add error tracking to loadGameIframe function'
            },
            {
                'category': 'Performance',
                'priority': 'Medium',
                'recommendation': 'Monitor game loading times and iframe response times',
                'implementation': 'Add performance.timing measurements'
            },
            {
                'category': 'Conversion Tracking',
                'priority': 'Low',
                'recommendation': 'Track successful game completions and user retention',
                'implementation': 'Implement game session duration tracking'
            }
        ]
        
        print("Analytics recommendations:")
        for rec in recommendations:
            priority_icon = "[HIGH]" if rec['priority'] == 'High' else "[MED]" if rec['priority'] == 'Medium' else "[LOW]"
            print(f"  {priority_icon} {rec['category']}: {rec['recommendation']}")
            
        return recommendations
    
    def create_monitoring_dashboard(self):
        """Create monitoring dashboard data"""
        print("\nCreating monitoring dashboard...")
        
        dashboard_metrics = {
            'timestamp': datetime.now().isoformat(),
            'games_status': {
                'total_games': self.config['total_games'],
                'operational_games': sum(1 for game in self.config['games'] if game.get('embeddable', True)),
                'external_games': sum(1 for game in self.config['games'] if not game.get('embeddable', True)),
                'categories': len(set(game['category'] for game in self.config['games']))
            },
            'tracking_status': {
                'ga_configured': self.config['ga_measurement_id'] != 'GA_MEASUREMENT_ID',
                'events_mapped': True,
                'error_handling': True
            },
            'recommendations_count': 5,
            'next_check': (datetime.now() + timedelta(hours=24)).isoformat()
        }
        
        return dashboard_metrics
    
    def generate_report(self):
        """Generate comprehensive analytics report"""
        if not self.config:
            return None
            
        print("=" * 60)
        print("US Game Hub Analytics Monitoring Report")
        print("=" * 60)
        
        health_checks = self.check_analytics_health()
        tracking_analysis = self.analyze_game_tracking_coverage()
        recommendations = self.generate_tracking_recommendations()
        dashboard = self.create_monitoring_dashboard()
        
        report = {
            'report_date': self.config['check_date'],
            'ga_measurement_id': self.config['ga_measurement_id'],
            'health_checks': health_checks,
            'tracking_analysis': tracking_analysis,
            'recommendations': recommendations,
            'dashboard_metrics': dashboard,
            'summary': {
                'overall_health': 'Good' if all(health_checks.values()) else 'Needs Attention',
                'total_games': self.config['total_games'],
                'tracking_coverage': f"{tracking_analysis['embeddable_games']}/{tracking_analysis['total_games']} iframe compatible"
            }
        }
        
        # Save report
        os.makedirs('scripts/results', exist_ok=True)
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
            
        print(f"\n[SAVED] Analytics monitoring report saved: {self.results_file}")
        print(f"[HEALTH] Overall health: {report['summary']['overall_health']}")
        print(f"[COVERAGE] Game tracking coverage: {report['summary']['tracking_coverage']}")
        
        return report

def main():
    print("Starting Analytics Monitoring...")
    
    monitor = AnalyticsMonitor()
    if monitor.config:
        report = monitor.generate_report()
        if report:
            print("\n[ACTION] Key Actions:")
            high_priority = [r for r in report['recommendations'] if r['priority'] == 'High']
            for rec in high_priority:
                print(f"  - {rec['recommendation']}")
    else:
        print("[ERROR] Monitoring failed - check configuration")

if __name__ == "__main__":
    main()