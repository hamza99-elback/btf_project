from pricing import get_total_price

if __name__ == "__main__":
    from parser import parse_input

    film_name = "Back to the Future 1"
    film1 = parse_input(film_name)

    film_name = "Back to the Future 2"
    film2 = parse_input(film_name)

    film_name = "Back to the Future 3"
    film3 = parse_input(film_name)

    film_name = "La chèvre"
    other_film1 = parse_input(film_name)

    film_name = "Fast & Furious"
    other_film2 = parse_input(film_name)

    scenario1_panier = [film1, film2, film3]
    scenario2_panier = [film1, film3]
    scenario3_panier = [film1]
    scenario4_panier = [film1, film2, film3, film2]
    scenario5_panier = [film1, film2, film3, other_film1]


    print("Scenario 1: ", get_total_price(scenario1_panier))
    print("Scenario 2: ", get_total_price(scenario2_panier))
    print("Scenario 3: ", get_total_price(scenario3_panier))
    print("Scenario 4: ", get_total_price(scenario4_panier))
    print("Scenario 5: ", get_total_price(scenario5_panier))