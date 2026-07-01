from app import greet, add


def test_greet():
    assert greet() == "Library Management System"


def test_add():
    assert add(5, 3) == 8
