import json
import csv

with open("todays.txt", encoding="utf-8") as f:
    raw = json.load(f)

# Build player lookup by id
players = {
    x["id"]: x["attributes"]
    for x in raw["included"]
    if x["type"] == "new_player"
}

rows = []
for proj in raw["data"]:
    attrs = proj["attributes"]
    rels = proj["relationships"]

    player_id = rels.get("new_player", {}).get("data", {}).get("id")
    player = players.get(player_id, {})

    rows.append({
        "id": proj["id"],
        "player_name": player.get("display_name", ""),
        "team": player.get("team", ""),
        "position": player.get("position", ""),
        "combo": player.get("combo", False),
        "stat_type": attrs.get("stat_type", ""),
        "line_score": attrs.get("line_score", ""),
        "flash_sale_line": attrs.get("flash_sale_line_score", ""),
        "odds_type": attrs.get("odds_type", ""),
        "is_taco": attrs.get("discount_name") == "taco",
        "discount_pct": attrs.get("discount_percentage", ""),
        "is_promo": attrs.get("is_promo", False),
        "projection_type": attrs.get("projection_type", ""),
        "description": attrs.get("description", ""),
        "start_time": attrs.get("start_time", ""),
        "status": attrs.get("status", ""),
    })

with open("todays.csv", "w", newline="", encoding="utf-8", errors="replace") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Written {len(rows)} rows to todays.csv")
