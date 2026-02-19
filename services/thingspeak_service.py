import requests
from services.environment_index import co2_to_quality
from services.db import insert_reading

THINGSPEAK_CHANNELS = [
    {
        "name": "Toronto Air Quality Station",
        "channel_id": 1766576,
        "co2_field": "field1",
        "temp_field": "field2",
        "humidity_field": "field3"
    }
]

# In-memory cache for simulation
_simulation_cache = {}
_simulation_index = {}

def _load_channel_history(channel):
    url = f"https://api.thingspeak.com/channels/{channel['channel_id']}/feeds.json?results=100"
    res = requests.get(url, timeout=5)
    data = res.json()
    feeds = data.get("feeds", [])

    _simulation_cache[channel["channel_id"]] = feeds
    _simulation_index[channel["channel_id"]] = 0

def fetch_latest_data(simulate=True):
    results = []

    for ch in THINGSPEAK_CHANNELS:
        cid = ch["channel_id"]

        try:
            if simulate:
                # Load once
                if cid not in _simulation_cache:
                    _load_channel_history(ch)

                feeds = _simulation_cache[cid]
                if not feeds:
                    continue

                i = _simulation_index[cid]
                feed = feeds[i]

                # Move pointer forward (looping)
                _simulation_index[cid] = (i + 1) % len(feeds)
            else:
                url = f"https://api.thingspeak.com/channels/{cid}/feeds.json?results=1"
                res = requests.get(url, timeout=5)
                data = res.json()
                feed = data["feeds"][0]

            co2 = float(feed.get(ch["co2_field"])) if feed.get(ch["co2_field"]) else None
            temp = float(feed.get(ch["temp_field"])) if feed.get(ch["temp_field"]) else None
            hum = float(feed.get(ch["humidity_field"])) if feed.get(ch["humidity_field"]) else None

            quality = co2_to_quality(co2)

            reading = {
                "name": ch["name"],
                "co2": co2,
                "temperature": temp,
                "humidity": hum,
                "latitude": 43.77591,   # from channel metadata (static)
                "longitude": -79.493176,
                "timestamp": feed["created_at"],
                "quality": quality["category"],
                "color": quality["color"],
                "score": quality["score"]
            }

            insert_reading(reading)
            results.append(reading)

        except Exception as e:
            print(f"Error fetching channel {cid}: {e}")

    return results
