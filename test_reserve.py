from reserve import Restaurant

def test_reserve_success():
    restaurant = Restaurant(10, 4)
    assert restaurant.reserve(4) is True

def test_reservve_fail():
    restaurant = Restaurant(2, 3)
    assert restaurant.reserve(8) is False
