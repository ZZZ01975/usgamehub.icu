#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GamePix游戏验证脚本
批量验证筛选游戏的URL可用性和iframe兼容性
"""

import json
import requests
import time
import concurrent.futures
from urllib.parse import urlparse
import sys

def load_games(json_path):
    """加载游戏JSON文件"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data['games']
    except Exception as e:
        print(f"加载游戏文件失败: {e}")
        return []

def test_game_url(game):
    """测试单个游戏URL的可用性"""
    try:
        url = game['iframeUrl']
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 发送HEAD请求
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        
        result = {
            'id': game['id'],
            'title': game['title'],
            'url': url,
            'status_code': response.status_code,
            'success': response.status_code == 200,
            'headers': dict(response.headers),
            'iframe_blocked': False,
            'error': None
        }
        
        # 检查X-Frame-Options头
        x_frame_options = response.headers.get('X-Frame-Options', '').upper()
        if x_frame_options in ['DENY', 'SAMEORIGIN']:
            result['iframe_blocked'] = True
            result['success'] = False
            result['error'] = f"X-Frame-Options: {x_frame_options}"
        
        # 检查Content-Security-Policy
        csp = response.headers.get('Content-Security-Policy', '')
        if 'frame-ancestors' in csp and "'none'" in csp:
            result['iframe_blocked'] = True
            result['success'] = False
            result['error'] = "CSP frame-ancestors restriction"
        
        return result
        
    except requests.exceptions.Timeout:
        return {
            'id': game['id'],
            'title': game['title'], 
            'url': game['iframeUrl'],
            'status_code': 0,
            'success': False,
            'error': 'Timeout'
        }
    except requests.exceptions.RequestException as e:
        return {
            'id': game['id'],
            'title': game['title'],
            'url': game['iframeUrl'],
            'status_code': 0,
            'success': False,
            'error': str(e)
        }

def validate_games_batch(games, max_workers=10):
    """批量验证游戏"""
    print(f"开始验证 {len(games)} 个游戏...")
    print("=" * 60)
    
    results = []
    successful = 0
    failed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交所有任务
        future_to_game = {executor.submit(test_game_url, game): game for game in games}
        
        # 收集结果
        for i, future in enumerate(concurrent.futures.as_completed(future_to_game), 1):
            try:
                result = future.result()
                results.append(result)
                
                if result['success']:
                    successful += 1
                    status = "✓ 成功"
                else:
                    failed += 1
                    status = f"✗ 失败 ({result['error'] or result['status_code']})"
                
                print(f"[{i:2d}/{len(games)}] {result['title'][:30]:30} {status}")
                
            except Exception as e:
                print(f"验证出错: {e}")
        
    print("\n" + "=" * 60)
    print(f"验证完成: {successful} 成功, {failed} 失败")
    print(f"成功率: {successful/len(games)*100:.1f}%")
    
    return results

def filter_working_games(games, validation_results):
    """根据验证结果过滤可用游戏"""
    working_games = []
    failed_games = []
    
    # 创建结果映射
    result_map = {r['id']: r for r in validation_results}
    
    for game in games:
        result = result_map.get(game['id'])
        if result and result['success']:
            working_games.append(game)
        else:
            failed_games.append({
                'game': game,
                'error': result['error'] if result else 'No validation result'
            })
    
    return working_games, failed_games

def save_results(working_games, failed_games, output_path, failed_path):
    """保存验证结果"""
    try:
        # 保存可用游戏
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({'games': working_games}, f, ensure_ascii=False, indent=2)
        
        # 保存失败记录
        with open(failed_path, 'w', encoding='utf-8') as f:
            json.dump({'failed_games': failed_games}, f, ensure_ascii=False, indent=2)
        
        print(f"\n保存 {len(working_games)} 个可用游戏到: {output_path}")
        print(f"保存 {len(failed_games)} 个失败记录到: {failed_path}")
        
        return True
    except Exception as e:
        print(f"保存失败: {e}")
        return False

def generate_report(working_games, failed_games):
    """生成验证报告"""
    total = len(working_games) + len(failed_games)
    success_rate = len(working_games) / total * 100 if total > 0 else 0
    
    print("\n" + "=" * 80)
    print("GamePix游戏验证报告")
    print("=" * 80)
    
    print(f"总游戏数: {total}")
    print(f"验证成功: {len(working_games)} 个")
    print(f"验证失败: {len(failed_games)} 个")
    print(f"成功率: {success_rate:.1f}%")
    
    if working_games:
        print("\n🟢 可用游戏分类统计:")
        categories = {}
        for game in working_games:
            cat = game['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} 个游戏")
    
    if failed_games:
        print("\n🔴 失败游戏错误统计:")
        errors = {}
        for item in failed_games:
            error = item['error']
            errors[error] = errors.get(error, 0) + 1
        
        for error, count in sorted(errors.items(), key=lambda x: x[1], reverse=True):
            print(f"  {error}: {count} 个游戏")
    
    # 推荐配置
    print("\n🔧 推荐iframe配置:")
    print("sandbox=\"allow-scripts allow-same-origin allow-popups allow-forms allow-pointer-lock\"")
    print("allow=\"accelerometer; autoplay; fullscreen; gyroscope\"")
    
    return {
        'total': total,
        'working': len(working_games),
        'failed': len(failed_games),
        'success_rate': success_rate
    }

def main():
    """主函数"""
    print("GamePix游戏验证工具")
    print("=" * 50)
    
    # 文件路径
    input_path = "data/games_gamepix_filtered.json"
    output_path = "data/games_gamepix_validated.json"
    failed_path = "data/games_gamepix_failed.json"
    
    # 加载游戏
    games = load_games(input_path)
    if not games:
        print("没有游戏需要验证")
        return False
    
    print(f"加载了 {len(games)} 个游戏")
    
    # 验证游戏
    validation_results = validate_games_batch(games)
    
    # 过滤可用游戏
    working_games, failed_games = filter_working_games(games, validation_results)
    
    # 保存结果
    if save_results(working_games, failed_games, output_path, failed_path):
        # 生成报告
        report = generate_report(working_games, failed_games)
        
        if report['success_rate'] >= 80:
            print("\n🎉 验证成功! 游戏可用性达到要求")
        else:
            print(f"\n⚠️  验证完成，但成功率偏低 ({report['success_rate']:.1f}%)")
            print("建议检查失败游戏并寻找替代方案")
        
        return True
    else:
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)