from models import Film

def get_bttf_reduction_rate(films_list: list[Film]) -> float:
    """
    Calculate the reduction rate based on the number of different films in the list.
    The more different films, the higher the reduction rate.

    :param films_list: List of films to calculate the reduction for.
    :return: Reduction rate as a float.
    """

    unique_films = set(film.volume for film in films_list if film.film_type == "bttf")
    num_unique_films = len(unique_films)

    if num_unique_films == 2:
        return 0.10  # 10% reduction for 2 different films
    elif num_unique_films == 3:
        return 0.20  # 20% reduction for 3 different films
    else:
        return 0.0   # No reduction for less than 2 different films
    

def get_total_price(films_list: list[Film]) -> float:
    """
    Calculate the total price for a list of films, applying the appropriate reduction.

    :param films_list: List of films to calculate the total price for.
    :return: Total price after applying reduction.
    """
    # split films into groups of different films

    others = [film for film in films_list if film.film_type == "other"]
    bttf = [film for film in films_list if film.film_type == "bttf"]

    bttf_reduction_rate = get_bttf_reduction_rate(bttf)
    total_others_price = sum(film.price for film in others)
    total_bttf_price = sum(film.price for film in bttf)* (1 - bttf_reduction_rate)


    total_price = total_others_price + total_bttf_price
    return total_price
