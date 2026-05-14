#!/usr/bin/env python3
"""
龙虾集群 - 通用搜索工具（国内可用方案）
多引擎自动切换：搜狗 -> Bing -> 百度
"""

import urllib.request, urllib.parse, sys, re

def search(query, num=5):
    """多引擎搜索"""
    engines = [
        ("搜狗", f"https://www.sogou.com/web?query={urllib.parse.quote(query)}"),
        ("Bing中国", f"https://cn.bing.com/search?q={urllib.parse.quote(query)}&count={num}"),
        ("百度", f"https://www.baidu.com/s?wd={urllib.parse.quote(query)}&rn={num}"),
    ]
    
    for name, url in engines:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            })
            resp = urllib.request.urlopen(req, timeout=10)
            html = resp.read().decode('utf-8', errors='replace')
            # 提取标题和链接
            results = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', html)
            clean = [(t.strip(), u) for u, t in results if t.strip()]
            if clean:
                print(f"✅ {name}搜索成功: {query[:30]}")
                for i, (title, url) in enumerate(clean[:num]):
                    print(f"  {i+1}. {title[:60]}")
                    print(f"     {url[:80]}")
                return
        except Exception as e:
            print(f"  ⏳ {name}不可用: {str(e)[:30]}...")
    print("❌ 所有搜索引擎均不可用")

if __name__ == '__main__':
    query = ' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'A股今日行情'
    search(query)
