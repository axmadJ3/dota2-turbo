def calculate_rating_change(win, kills, deaths, assists):
    return (20 if win else -20) + kills * 4 - deaths * 4 + assists * 1
