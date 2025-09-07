#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地验证脚本 - 检测所有功能是否正常工作
在推送到GitHub之前运行此脚本确保一切正常
"""

import json
import os
import sys
import requests
from datetime import datetime
import subprocess

class LocalValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def log_error(self, message):
        self.errors.append(f"[ERROR] {message}")
        print(f"[ERROR] {message}")
    
    def log_warning(self, message):
        self.warnings.append(f"[WARN] {message}")
        print(f"[WARN] {message}")
    
    def log_success(self, message):
        print(f"[OK] {message}")

    def check_file_structure(self):
        """检查必要文件是否存在"""
        print("\n=== 检查文件结构 ===")
        
        required_files = [
            'data/games.json',
            'data/game-schema.json',
            'data/categories.json',
            'index.html',
            'game.html',
            'js/games.js',
            'js/analytics.js',
            '.github/workflows/weekly-health-check.yml',
            'scripts/check_games.py',
            'scripts/auto_disable_games.py',
            'scripts/game_discovery.py'
        ]
        
        missing_files = []
        for file_path in required_files:
            if not os.path.exists(file_path):
                missing_files.append(file_path)
                self.log_error(f"Missing file: {file_path}")
            else:
                self.log_success(f"Found: {file_path}")
        
        if not missing_files:
            self.log_success("All required files present")
        
        return len(missing_files) == 0
    
    def validate_json_schema(self):
        """验证JSON数据完整性"""
        print("\n=== 验证JSON Schema ===")
        
        try:
            # 使用ajv-cli验证
            result = subprocess.run(['ajv', 'validate', '-s', 'data/game-schema.json', '-d', 'data/games.json'], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                self.log_success("JSON Schema validation passed")
                return True
            else:
                self.log_error(f"JSON Schema validation failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_error(f"Failed to run JSON validation: {e}")
            return False
    
    def check_games_data_quality(self):
        """检查游戏数据质量"""
        print("\n=== 检查游戏数据质量 ===")
        
        try:
            with open('data/games.json', 'r', encoding='utf-8') as f:
                games_data = json.load(f)
            
            games = games_data.get('games', [])
            self.log_success(f"Found {len(games)} games in database")
            
            # 检查必需字段
            required_fields = ['id', 'title', 'description', 'category', 'iframeUrl', 
                             'license', 'commercial_use', 'ad_allowed', 'source_url']
            
            for i, game in enumerate(games):
                game_id = game.get('id', f'game-{i}')
                
                for field in required_fields:
                    if field not in game:
                        self.log_error(f"Game {game_id} missing required field: {field}")
                
                # 检查描述长度
                desc = game.get('description', '')
                if len(desc) < 100:
                    self.log_warning(f"Game {game_id} description too short ({len(desc)} chars)")
                
                # 检查评分范围
                rating = game.get('rating', 0)
                if not (1 <= rating <= 5):
                    self.log_error(f"Game {game_id} invalid rating: {rating}")
            
            # 检查合规字段
            commercial_count = sum(1 for g in games if g.get('commercial_use', False))
            ad_count = sum(1 for g in games if g.get('ad_allowed', False))
            
            self.log_success(f"Commercial use allowed: {commercial_count}/{len(games)} games")
            self.log_success(f"Ads allowed: {ad_count}/{len(games)} games")
            
            return True
            
        except Exception as e:
            self.log_error(f"Failed to validate games data: {e}")
            return False
    
    def test_iframe_compatibility(self, sample_size=3):
        """测试部分游戏的iframe兼容性"""
        print(f"\n=== 测试游戏兼容性 (抽样{sample_size}款) ===")
        
        try:
            with open('data/games.json', 'r', encoding='utf-8') as f:
                games_data = json.load(f)
            
            games = games_data.get('games', [])
            test_games = games[:sample_size]  # 测试前几款游戏
            
            session = requests.Session()
            session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            compatible_count = 0
            for game in test_games:
                game_id = game.get('id', 'unknown')
                iframe_url = game.get('iframeUrl', '')
                
                try:
                    response = session.head(iframe_url, timeout=10, allow_redirects=True)
                    
                    if response.status_code >= 400:
                        self.log_warning(f"Game {game_id}: HTTP {response.status_code}")
                        continue
                    
                    # 检查X-Frame-Options
                    xfo = response.headers.get('X-Frame-Options', '').upper()
                    if 'DENY' in xfo or 'SAMEORIGIN' in xfo:
                        self.log_warning(f"Game {game_id}: X-Frame-Options blocking")
                        continue
                    
                    self.log_success(f"Game {game_id}: iframe compatible")
                    compatible_count += 1
                    
                except Exception as e:
                    self.log_warning(f"Game {game_id}: Connection failed - {str(e)[:50]}")
            
            self.log_success(f"Compatibility test: {compatible_count}/{len(test_games)} games working")
            return True
            
        except Exception as e:
            self.log_error(f"Failed to test compatibility: {e}")
            return False
    
    def check_analytics_integration(self):
        """检查GA集成"""
        print("\n=== 检查Google Analytics集成 ===")
        
        try:
            # 检查index.html中的GA代码
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'G-P13WZKJZ3H' in content:
                self.log_success("Google Analytics tracking ID found")
            else:
                self.log_error("Google Analytics tracking ID missing")
                return False
            
            # 检查analytics.js
            if os.path.exists('js/analytics.js'):
                with open('js/analytics.js', 'r', encoding='utf-8') as f:
                    analytics_content = f.read()
                
                if 'gtag' in analytics_content and 'trackGameLoad' in analytics_content:
                    self.log_success("Analytics.js properly configured")
                else:
                    self.log_warning("Analytics.js missing some functions")
            else:
                self.log_error("Analytics.js file missing")
                return False
            
            return True
            
        except Exception as e:
            self.log_error(f"Failed to check analytics: {e}")
            return False
    
    def validate_github_workflow(self):
        """验证GitHub Actions工作流配置"""
        print("\n=== 验证GitHub Actions配置 ===")
        
        try:
            workflow_file = '.github/workflows/weekly-health-check.yml'
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查关键配置
            required_elements = [
                'cron: \'0 3 * * 1\'',  # 每周一运行
                'python scripts/check_games.py',
                'python scripts/auto_disable_games.py',
                'git add data/games.json',
                'git commit'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                for element in missing_elements:
                    self.log_error(f"Workflow missing: {element}")
                return False
            else:
                self.log_success("GitHub Actions workflow properly configured")
                return True
                
        except Exception as e:
            self.log_error(f"Failed to validate workflow: {e}")
            return False
    
    def run_full_validation(self):
        """运行完整验证"""
        print("=" * 60)
        print("US GAME HUB - 本地验证工具")
        print("=" * 60)
        
        all_checks = [
            self.check_file_structure(),
            self.validate_json_schema(),
            self.check_games_data_quality(),
            self.test_iframe_compatibility(),
            self.check_analytics_integration(),
            self.validate_github_workflow()
        ]
        
        print("\n" + "=" * 60)
        print("验证结果总结")
        print("=" * 60)
        
        passed = sum(all_checks)
        total = len(all_checks)
        
        print(f"通过检查: {passed}/{total}")
        
        if self.errors:
            print(f"\n发现 {len(self.errors)} 个错误:")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n发现 {len(self.warnings)} 个警告:")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if passed == total and len(self.errors) == 0:
            print("\n[SUCCESS] 所有检查通过！可以安全推送到GitHub")
            return True
        else:
            print("\n[FAILED] 请修复上述问题后重新运行验证")
            return False

def main():
    if not os.path.exists('data/games.json'):
        print("错误：请在项目根目录运行此脚本")
        return 1
    
    validator = LocalValidator()
    success = validator.run_full_validation()
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())