def co2_to_quality(co2_ppm):
    if co2_ppm is None:
        return {"category": "No Data", "color": "#9ca3af", "score": None}

    if co2_ppm <= 420:
        return {"category": "Very Low", "color": "#22c55e", "score": 10}   # green
    elif co2_ppm <= 450:
        return {"category": "Low", "color": "#84cc16", "score": 25}       # lime
    elif co2_ppm <= 480:
        return {"category": "Normal", "color": "#facc15", "score": 45}    # yellow
    elif co2_ppm <= 510:
        return {"category": "Elevated", "color": "#fb923c", "score": 65}  # orange
    else:
        return {"category": "High", "color": "#ef4444", "score": 85}      # red
