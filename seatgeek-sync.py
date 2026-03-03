#!/usr/bin/env python3
"""Pull SeatGeek pricing data for all Optimus events and output JSON."""

import urllib.request
import urllib.parse
import json
import sys
import os

CLIENT_ID = os.environ.get("SEATGEEK_CLIENT_ID", "NTY0MTU4MDB8MTc3MjExNDg0NS4xNzA2OTQ")
CLIENT_SECRET = os.environ.get("SEATGEEK_CLIENT_SECRET", "03205de686d5329f79635c095b128094154412213aa04e37d07871d4ae162b26")

def search_events(query, per_page=5):
    """Search SeatGeek events by query."""
    params = urllib.parse.urlencode({
        "q": query,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "per_page": per_page,
        "sort": "datetime_utc.asc",
    })
    url = f"https://api.seatgeek.com/2/events?{params}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
        return {"events": []}

def search_performer(query):
    """Search SeatGeek performers by query."""
    params = urllib.parse.urlencode({
        "q": query,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "per_page": 3,
    })
    url = f"https://api.seatgeek.com/2/performers?{params}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            # Return highest-scored performer
            performers = data.get("performers", [])
            if performers:
                return max(performers, key=lambda p: p.get("score", 0))
    except Exception as e:
        print(f"  Error: {e}", file=sys.stderr)
    return None

# Artists/events to look up
searches = [
    {"name": "Metallica", "query": "metallica sphere"},
    {"name": "Jason Aldean", "query": "jason aldean"},
    {"name": "Joji", "query": "joji"},
    {"name": "Sting", "query": "sting 3.0"},
    {"name": "Maya Hawke", "query": "maya hawke"},
    {"name": "Charley Crockett", "query": "charley crockett"},
    {"name": "Creed", "query": "creed bush mystic lake"},
    {"name": "Tucker Wetmore", "query": "tucker wetmore red rocks"},
    {"name": "Billy Strings", "query": "billy strings"},
    {"name": "Outside Lands", "query": "outside lands 2026"},
    {"name": "MLB All-Star Game", "query": "mlb all star game 2026"},
    {"name": "MJ Lenderman", "query": "mj lenderman"},
]

results = {}
for s in searches:
    print(f"Searching: {s['name']}...", file=sys.stderr)
    events = search_events(s["query"])
    performer = search_performer(s["name"])
    
    event_list = []
    for e in events.get("events", [])[:5]:
        stats = e.get("stats", {})
        venue = e.get("venue", {})
        event_list.append({
            "id": e["id"],
            "date": e.get("datetime_local", "")[:10],
            "venue": venue.get("name", ""),
            "city": venue.get("city", ""),
            "state": venue.get("state", ""),
            "url": e.get("url", ""),
            "lowest_price": stats.get("lowest_price"),
            "average_price": stats.get("average_price"),
            "highest_price": stats.get("highest_price"),
            "listing_count": stats.get("listing_count"),
            "score": e.get("score", 0),
        })
    
    results[s["name"]] = {
        "events": event_list,
        "performer_score": performer.get("score", 0) if performer else 0,
        "performer_url": performer.get("url", "") if performer else "",
        "performer_id": performer.get("id", 0) if performer else 0,
    }

print(json.dumps(results, indent=2))
