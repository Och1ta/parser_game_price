import requests
from bs4 import BeautifulSoup


def price_game_steam(URL, game_name):
    response = requests.get(URL)

    bs = BeautifulSoup(response.text, 'html.parser')

    find_game = bs.find('div', class_='col search_name ellipsis')

    game_title = find_game.find('span', class_='title').text.strip()

    if game_name == game_title.lower():
        game_price = bs.find('div', class_='discount_final_price').text.strip()
        return game_title, game_price
    else:
        return 'Game not found'


def url_game_steam(URL):
    response = requests.get(URL)

    bs = BeautifulSoup(response.text, 'html.parser')

    find_game = bs.find('a', class_='search_result_row ds_collapse_flag')

    game_title = find_game.get('href')

    return game_title


if __name__ == '__main__':
    game_name = input('>>>')
    URL = f'https://store.steampowered.com/search/?term={game_name}'

    print(price_game_steam(URL, game_name))
    print(url_game_steam(URL))
