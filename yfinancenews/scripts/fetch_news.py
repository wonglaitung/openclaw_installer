#!/usr/bin/env python3
"""
Stock News Fetcher using Yahoo Finance API

Fetches news related to a stock from Yahoo Finance API.
Returns structured JSON data with news information.

Usage:
    python3 fetch_news.py <stock_code> [--limit N]
    python3 fetch_news.py AAPL
    python3 fetch_news.py MSFT --limit 10
    python3 fetch_news.py 1398.HK
"""

import sys
import json
import requests
from datetime import datetime
import argparse

def fetch_yahoo_finance_news(symbol, limit=5):
    """
    Fetch news data for a stock from Yahoo Finance API.

    Uses Yahoo Finance's public API endpoint.
    """
    try:
        # Yahoo Finance API endpoint for news
        url = f"https://query2.finance.yahoo.com/v1/finance/search?q={symbol}&quotesCount=0&newsCount={limit}"

        # Headers to mimic browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        # Make request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Check for errors
        if data.get('error'):
            raise ValueError(f"Yahoo Finance API error: {data['error']}")

        # Extract news from response
        news_items = data.get('news', [])

        if not news_items:
            return {"news": [], "message": "No news found for this stock"}

        # Process each news item
        processed_news = []
        for item in news_items:
            # Parse publish time (Unix timestamp in milliseconds)
            publish_time = item.get('providerPublishTime', 0)
            if publish_time:
                publish_time = datetime.fromtimestamp(publish_time / 1000).isoformat()
            else:
                publish_time = item.get('published', 'Unknown')

            # Get related symbols
            related_symbols = item.get('relatedSymbols', [])
            symbol_list = [sym.get('symbol', '') for sym in related_symbols]

            news_item = {
                "title": item.get('title', 'No title'),
                "summary": item.get('summary', ''),
                "link": item.get('link', ''),
                "source": item.get('publisher', 'Unknown'),
                "published": publish_time,
                "related_symbols": symbol_list
            }

            processed_news.append(news_item)

        return {
            "symbol": symbol,
            "news_count": len(processed_news),
            "news": processed_news
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except ValueError as e:
        return {"error": f"Data parsing error: {str(e)}"}
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}

def format_output(news_data):
    """Format news data for display."""
    if 'error' in news_data:
        return f"❌ Error: {news_data['error']}"

    if 'message' in news_data:
        return f"ℹ️ {news_data['message']}"

    symbol = news_data.get('symbol', 'Unknown')
    news_count = news_data.get('news_count', 0)
    news_items = news_data.get('news', [])

    output = []
    output.append(f"📰 {symbol} 最新新闻 ({news_count} 条)")
    output.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    output.append("")

    for idx, item in enumerate(news_items, 1):
        output.append(f"{idx}. 📰 {item['title']}")
        output.append(f"   📝 {item['summary'][:200]}..." if len(item['summary']) > 200 else f"   📝 {item['summary']}")
        output.append(f"   🌐 来源: {item['source']}")
        output.append(f"   🕐 时间: {item['published']}")
        output.append(f"   🔗 链接: {item['link']}")
        if item['related_symbols']:
            output.append(f"   📊 相关股票: {', '.join(item['related_symbols'])}")
        output.append("")

    return '\n'.join(output)

def main():
    """Main function to fetch and display news data."""
    parser = argparse.ArgumentParser(description='Fetch stock news from Yahoo Finance')
    parser.add_argument('stock_code', help='Stock code (e.g., AAPL, MSFT, 1398.HK)')
    parser.add_argument('--limit', type=int, default=5, help='Number of news items to fetch (default: 5)')

    args = parser.parse_args()

    stock_code = args.stock_code.upper()
    limit = args.limit

    print(f"🔍 Fetching news for: {stock_code}")
    print(f"📰 News limit: {limit}")
    print()

    # Fetch news from Yahoo Finance
    news_data = fetch_yahoo_finance_news(stock_code, limit)

    # Output JSON
    print("📋 JSON Data:")
    print(json.dumps(news_data, indent=2, ensure_ascii=False))
    print()

    # Output formatted display
    print("📰 Formatted Output:")
    print(format_output(news_data))

if __name__ == "__main__":
    main()