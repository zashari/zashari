#!/usr/bin/env python3
"""
Script to update README.md with GitHub stats from github-user-stats.json
"""
import json
import re
import os
from datetime import datetime

def format_number(num):
    """Format large numbers with K/M suffixes"""
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)

def update_readme_with_stats():
    # Check if stats file exists
    if not os.path.exists('github-user-stats.json'):
        print("github-user-stats.json not found. Stats collection may not have completed.")
        return
    
    # Read stats JSON
    with open('github-user-stats.json', 'r') as f:
        stats = json.load(f)
    
    # Read README
    with open('README.md', 'r') as f:
        readme_content = f.read()
    
    # Format stats section
    stats_section = f"""## 📊 GitHub Stats

<div align="center">

| Metric | Value |
|:---:|:---:|
| **Total Contributions** | {format_number(stats.get('totalContributions', 0))} |
| **Total Commits** | {format_number(stats.get('totalCommits', 0))} |
| **Total Pull Requests** | {format_number(stats.get('totalPullRequests', 0))} |
| **Total Stars Earned** | {format_number(stats.get('starCount', 0))} |
| **Total Forks** | {format_number(stats.get('forkCount', 0))} |
| **Repository Views** | {format_number(stats.get('repoViews', 0))} |
| **Lines of Code Changed** | {format_number(stats.get('linesOfCodeChanged', 0))} |
| **Lines Added** | {format_number(stats.get('linesAdded', 0))} |
| **Lines Deleted** | {format_number(stats.get('linesDeleted', 0))} |
| **Open Issues** | {format_number(stats.get('openIssues', 0))} |
| **Closed Issues** | {format_number(stats.get('closedIssues', 0))} |

### 🎯 Top Languages

"""
    
    # Add top languages
    top_languages = stats.get('topLanguages', [])[:5]
    if top_languages:
        lang_badges = []
        for lang in top_languages:
            lang_name = lang.get('languageName', '')
            lang_color = lang.get('color', '#000000').lstrip('#')
            lang_badges.append(f"![{lang_name}](https://img.shields.io/badge/{lang_name}-{lang_color}?style=flat-square&logo={lang_name.lower()}&logoColor=white)")
        
        stats_section += " ".join(lang_badges) + "\n\n"
    
    # Add last updated timestamp
    fetched_at = stats.get('fetchedAt', 0)
    if fetched_at:
        dt = datetime.fromtimestamp(fetched_at / 1000)
        stats_section += f"*Last updated: {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}*\n"
    
    stats_section += "\n</div>\n"
    
    # Replace or insert stats section in README
    # Pattern to match existing stats section (if any)
    stats_pattern = r'## 📊 GitHub Stats.*?</div>\n'
    
    if re.search(stats_pattern, readme_content, re.DOTALL):
        # Replace existing stats section
        readme_content = re.sub(stats_pattern, stats_section, readme_content, flags=re.DOTALL)
    else:
        # Insert stats section after social links and before "These are my contributions"
        social_pattern = r'(</p>\n\n)(## These are my contributions)'
        if re.search(social_pattern, readme_content):
            readme_content = re.sub(
                social_pattern,
                r'\1' + stats_section + r'\n\n\2',
                readme_content
            )
        else:
            # If pattern not found, add before "These are my contributions"
            contributions_pattern = r'(## These are my contributions)'
            if re.search(contributions_pattern, readme_content):
                readme_content = re.sub(
                    contributions_pattern,
                    stats_section + r'\n\n\1',
                    readme_content
                )
            else:
                # Last resort: add at the end
                readme_content += "\n\n" + stats_section
    
    # Write updated README
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("README updated with GitHub stats!")

if __name__ == '__main__':
    update_readme_with_stats()

