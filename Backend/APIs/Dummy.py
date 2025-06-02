from fastapi import FastAPI, HTTPException
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.library.parameters import SeasonAll

app = FastAPI()

@app.get("/")
def root():
    return {"message": "NBA API Dummy Backend is running"}

@app.get("/player/{player_name}")
def get_player_stats(player_name: str):
    # Search for the player
    matched_players = players.find_players_by_full_name(player_name)

    if not matched_players:
        raise HTTPException(status_code=404, detail="Player not found")

    player = matched_players[0]
    player_id = player["id"]
    #new comment 
    # Fetch career stats
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        career_data = career.get_dict()
        stats = career_data['resultSets'][0]['rowSet']
        headers = career_data['resultSets'][0]['headers']

        recent_stats = dict(zip(headers, stats[-1]))  # Latest season

        return {
            "player_id": player_id,
            "full_name": player["full_name"],
            "team": player.get("team_id"),
            "recent_season_stats": recent_stats
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {e}")