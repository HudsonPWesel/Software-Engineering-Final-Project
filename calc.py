PERCENT_OF_FLYERS = 0.005
MARKET_SHARE = 0.02


def calc_number_of_flyers(
    source_metro_pop, dest_metro_pop, total_reachable_pop_excluding_source
):
    daily_flyers = source_metro_pop * PERCENT_OF_FLYERS
    panther_flyers = daily_flyers * MARKET_SHARE

    dest_share = dest_metro_pop / total_reachable_pop_excluding_source
    return panther_flyers * dest_share


print(calc_number_of_flyers(1_000_000, 10_000_000, 175_000_000))
