#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏URL探活检测脚本 - 检查iframe兼容性和可用性
包含三道保险丝：超时重试、重定向处理、日期归档
"""

import requests
import json
import csv
import time
import os
from datetime import datetime
from urllib.parse import urlparse

class GameChecker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
    
    def check_iframe_compatibility(self, url, max_retries=2):
        """
        检查URL是否支持iframe嵌入，带重试机制
        
        Args:
            url: 要检查的游戏URL
            max_retries: 最大重试次数
            
        Returns:
            tuple: (can_embed, reason, status_code, final_url)
        """
        print(f"  Checking: {url}")
        
        for attempt in range(max_retries + 1):
            try:
                # 设置10秒超时
                response = self.session.head(url, timeout=10, allow_redirects=True)
                
                # 获取最终URL（处理重定向）
                final_url = response.url
                status_code = response.status_code
                
                # 如果有重定向，再次检查最终URL的headers
                if response.history:
                    print(f"    Redirect detected: {url} -> {final_url}")
                    try:
                        response = self.session.head(final_url, timeout=10)
                    except:
                        pass  # 如果重定向URL检查失败，使用原始response
                
                headers = response.headers
                
                # 检查HTTP状态码
                if status_code >= 400:
                    return False, f"HTTP {status_code} Error", status_code, final_url
                
                # 检查X-Frame-Options
                xfo = headers.get('X-Frame-Options', '').upper()
                if 'DENY' in xfo:
                    return False, "X-Frame-Options: DENY", status_code, final_url
                elif 'SAMEORIGIN' in xfo:
                    return False, "X-Frame-Options: SAMEORIGIN", status_code, final_url
                
                # 检查Content-Security-Policy
                csp = headers.get('Content-Security-Policy', '')
                if 'frame-ancestors' in csp.lower():
                    if "'none'" in csp or 'none' in csp:
                        return False, "CSP frame-ancestors 'none'", status_code, final_url
                    elif "'self'" in csp and 'usgamehub.icu' not in csp:
                        return False, "CSP frame-ancestors 'self' only", status_code, final_url
                
                # 检查域名变化（可能的商业劫持）
                original_domain = urlparse(url).netloc
                final_domain = urlparse(final_url).netloc
                if original_domain != final_domain:
                    # 允许www子域名差异
                    if not (original_domain.replace('www.', '') == final_domain.replace('www.', '')):
                        return False, f"Domain changed: {original_domain} -> {final_domain}", status_code, final_url
                
                return True, "OK - iframe compatible", status_code, final_url
                
            except requests.exceptions.Timeout:
                if attempt < max_retries:
                    print(f"    Timeout, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(2)
                    continue
                return False, "Timeout after retries", 0, url
                
            except requests.exceptions.ConnectionError as e:
                if attempt < max_retries:
                    print(f"    Connection error, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(2)
                    continue
                return False, f"Connection error: {str(e)[:100]}", 0, url
                
            except Exception as e:
                if attempt < max_retries:
                    print(f"    Other error, retrying ({attempt + 1}/{max_retries})...")
                    time.sleep(2)
                    continue
                return False, f"Error: {str(e)[:100]}", 0, url
        
        return False, "Max retries reached", 0, url

def load_games_data():
    """加载游戏数据"""
    try:
        with open('data/games.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 错误: 找不到 data/games.json 文件")
        return None
    except json.JSONDecodeError:
        print("❌ 错误: games.json 格式不正确")
        return None

def batch_check_games():
    """批量检测游戏可用性"""
    print("Starting batch game URL compatibility check...")
    
    # 加载游戏数据
    games_data = load_games_data()
    if not games_data:
        return
    
    games = games_data.get('games', [])
    if not games:
        print("Error: No game data found")
        return
    
    print(f"Total games to check: {len(games)}")
    print("-" * 60)
    
    checker = GameChecker()
    results = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    successful_count = 0
    failed_count = 0
    
    for i, game in enumerate(games, 1):
        print(f"[{i}/{len(games)}] 检测: {game['title']}")
        
        can_embed, reason, status_code, final_url = checker.check_iframe_compatibility(game['iframeUrl'])
        
        result = {
            'id': game['id'],
            'title': game['title'],
            'category': game['category'],
            'original_url': game['iframeUrl'],
            'final_url': final_url,
            'can_embed': can_embed,
            'reason': reason,
            'status_code': status_code,
            'check_time': timestamp,
            'featured': game.get('featured', False)
        }
        
        results.append(result)
        
        if can_embed:
            successful_count += 1
            print(f"  [OK] {reason}")
        else:
            failed_count += 1
            print(f"  [FAIL] {reason}")
        
        # 避免请求过快
        time.sleep(1)
        print()
    
    # 保存详细结果到CSV（按日期归档）
    today = datetime.now().strftime("%Y%m%d")
    detailed_filename = f'scripts/results/check_results_detailed_{today}.csv'
    
    # 确保结果目录存在
    os.makedirs('scripts/results', exist_ok=True)
    
    with open(detailed_filename, 'w', newline='', encoding='utf-8') as f:
        if results:
            fieldnames = results[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
    
    # 生成简化的可用游戏列表
    available_games = [r for r in results if r['can_embed']]
    unavailable_games = [r for r in results if not r['can_embed']]
    
    summary_filename = f'scripts/results/summary_{today}.json'
    summary = {
        'check_time': timestamp,
        'total_games': len(games),
        'available_count': successful_count,
        'unavailable_count': failed_count,
        'success_rate': f"{(successful_count/len(games)*100):.1f}%",
        'available_games': [
            {
                'id': g['id'], 
                'title': g['title'], 
                'url': g['original_url'],
                'category': g['category']
            } for g in available_games
        ],
        'unavailable_games': [
            {
                'id': g['id'], 
                'title': g['title'], 
                'reason': g['reason'],
                'category': g['category']
            } for g in unavailable_games
        ]
    }
    
    with open(summary_filename, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # 打印总结报告
    print("=" * 60)
    print("Detection completed! Summary report:")
    print(f"Total games: {len(games)}")
    print(f"Available games: {successful_count} ({successful_count/len(games)*100:.1f}%)")
    print(f"Unavailable games: {failed_count} ({failed_count/len(games)*100:.1f}%)")
    print(f"\nDetailed results saved to: {detailed_filename}")
    print(f"Summary report saved to: {summary_filename}")
    
    # 显示可用游戏列表
    if available_games:
        print(f"\nAvailable games ({len(available_games)}):")
        for game in available_games:
            print(f"  - {game['title']} ({game['category']})")
    
    # 显示不可用游戏的主要原因
    if unavailable_games:
        print(f"\nMain issues with unavailable games:")
        reason_count = {}
        for game in unavailable_games:
            reason = game['reason']
            reason_count[reason] = reason_count.get(reason, 0) + 1
        
        for reason, count in sorted(reason_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {reason}: {count} games")
    
    print("\nSuggested next steps:")
    if successful_count < 10:
        print("  1. Current available games are few, suggest adding self-hosted open source games")
        print("  2. Consider implementing hybrid display strategy (iframe + new window)")
    if failed_count > 20:
        print("  1. Many games unavailable, need to batch replace game sources")
        print("  2. Suggest running Playwright script to further verify actual loading of available games")
    
    return summary

if __name__ == "__main__":
    # 确保在正确的目录下运行
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
            exit(1)
    
    batch_check_games()