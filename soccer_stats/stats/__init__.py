import math


def _to_min(m):
    time = m.replace('\'', '').split('+')
    return int(time[0]), int(time[1]) if len(time) == 2 else None


def minute_sort_key(x):
    # Handle range of minutes
    label, _ = x
    if ' - ' in label:
        lo, hi = label.split(' - ')
        lo, hi = _to_min(lo)[0], _to_min(hi)[0]
        return lo
    # Handle single minutes
    else:
        minute, extra = _to_min(label)
        extra = 0.0 if extra is None else float(extra) * 0.1
        return minute + extra


# home_goals = [g['minute'] for g in sort_game_goals(game['home_goals'])]
# away_goals = [g['minute'] for g in sort_game_goals(game['away_goals'])]
def sort_game_goals(goals):
    return sorted(goals, key=lambda x:
                  minute_sort_key((x.get('minute'), None)))


def _all_minutes_counter_struct():
    hf_a_mins = ['{}\''.format(x) for x in range(1, 46)]
    hf_a_extra_mins = ['45+{}\''.format(x) for x in range(1, 20)]
    hf_b_mins = ['{}\''.format(x) for x in range(46, 91)]
    hf_b_extra_mins = ['90+{}\''.format(x) for x in range(1, 20)]
    ot_a_mins = ['{}\''.format(x) for x in range(91, 106)]
    ot_a_extra_mins = ['105+{}\''.format(x) for x in range(1, 20)]
    ot_b_mins = ['{}\''.format(x) for x in range(106, 121)]
    ot_b_extra_mins = ['120+{}\''.format(x) for x in range(1, 20)]
    return {str(x): 0 for x in
            hf_a_mins + hf_a_extra_mins +
            hf_b_mins + hf_b_extra_mins +
            ot_a_mins + ot_a_extra_mins +
            ot_b_mins + ot_b_extra_mins}


def _bucket_counter(counter, n=2, start=1, end=90):
    ranges = []
    curr = start
    size = (end - start + 0.00001) / n
    while curr < end:
        ranges.append((math.ceil(curr), math.floor(curr + size)))
        curr += size
    buckets = {'{}\' - {}\''.format(lo, hi): 0 for (lo, hi) in ranges}
    for minute, count in counter.items():
        int_min, int_extra = _to_min(minute)
        if int_extra is None:
            for lo, hi in ranges:
                if lo <= int_min <= hi:
                    buckets['{}\' - {}\''.format(lo, hi)] += count
    return buckets


def all_goals_per_game_per_year(games):
    counter = {}
    for game in games:
        goals = game['home_score'] + game['away_score']
        old_goals, old_count = counter.get(game['year'], (0, 0))
        new_goals, new_count = old_goals + goals, old_count + 1
        counter[game['year']] = (new_goals, new_count)
    return {year: float(goals) / float(count)
            for year, (goals, count) in counter.items()}


def all_goals_per_minute(games, buckets=-1):
    counter = _all_minutes_counter_struct()
    for game in games:
        goals = game['home_goals'] + game['away_goals']
        minutes = [goal['minute'] for goal in goals]
        for minute in minutes:
            counter[minute] += 1
    return _bucket_counter(counter, n=buckets) if buckets > 0 else counter


def game_winning_goals_per_minute(games, buckets=-1):
    counter = _all_minutes_counter_struct()
    for game in games:
        home_goals = sort_game_goals(game['home_goals'])
        away_goals = sort_game_goals(game['away_goals'])
        winning_goal = None

        # Check that a team won (by a goal) and that the game
        # was previously tied before the goal occurred.
        if game['home_score'] - 1 == game['away_score']:
            if (not away_goals or
                    away_goals[-1]['minute'] < home_goals[-1]['minute']):
                winning_goal = home_goals[-1]
        elif game['away_score'] - 1 == game['home_score']:
            if (not home_goals or
                    home_goals[-1]['minute'] < away_goals[-1]['minute']):
                winning_goal = away_goals[-1]

        if winning_goal is not None:
            winning_minute = winning_goal['minute']
            counter[winning_minute] += 1
    return _bucket_counter(counter, n=buckets) if buckets > 0 else counter


def pk_goals_per_minute(games, buckets=-1):
    counter = _all_minutes_counter_struct()
    for game in games:
        goals = game['home_goals'] + game['away_goals']
        minutes = [goal['minute'] for goal in goals if goal['penalty']]
        for minute in minutes:
            counter[minute] += 1
    return _bucket_counter(counter, n=buckets) if buckets > 0 else counter
