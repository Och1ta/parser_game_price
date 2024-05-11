import requests
from bs4 import BeautifulSoup


def parser_games_steam(url: str, game_name: str):
    """..."""
    response = requests.get(url)

    bs = BeautifulSoup(response.text, 'html.parser')

    find_name = bs.find(
        'div',
        class_='col search_name ellipsis'
    )
    find_url = bs.find(
        'a',
        class_='search_result_row ds_collapse_flag'
    )

    game_title = find_name.find('span', class_='title').text.strip()
    game_url = find_url.get('href')

    if game_name.lower() in game_title.lower():
        game_price_full = bs.find(
            'div',
            class_='discount_final_price'
        ).text.strip()

        if any(char.isdigit() for char in game_price_full):
            game_price = float(game_price_full.split(' ')[0].replace(',', '.'))
        else:
            game_price = 0

        return game_title, game_price, game_url
    else:
        return 'Game not found'
