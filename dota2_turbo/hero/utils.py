def calculate_tier(winrate):
    if winrate >= 53.5:
        tier = "S"
    elif winrate >= 51.5:
        tier = "A"
    elif winrate >= 49.5:
        tier = "B"
    elif winrate >= 47.5:
        tier = "C"
    else:
        tier = "D"
    return tier
