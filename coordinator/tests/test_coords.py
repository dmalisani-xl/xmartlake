from app.game import make_absolute_coord


def test_relative_same():
    resp = make_absolute_coord(original_value=(50,40), relative_position=(3,3))
    assert resp == (50, 40)


def test_relative_00():
    resp = make_absolute_coord(original_value=(50,40), relative_position=(0,0))
    assert resp == (47, 37)


def test_relative_66():
    resp = make_absolute_coord(original_value=(50,40), relative_position=(6,6))
    assert resp == (53, 43)


def test_relative_limit_1():
    resp = make_absolute_coord(original_value=(0,0), relative_position=(0,0))
    assert resp == (0, 0)


def test_relative_limit_2():
    resp = make_absolute_coord(original_value=(0,20), relative_position=(0,0))
    assert resp == (0, 17)


def test_relative_limit_3():
    resp = make_absolute_coord(original_value=(20,0), relative_position=(0,0))
    assert resp == (17, 0)