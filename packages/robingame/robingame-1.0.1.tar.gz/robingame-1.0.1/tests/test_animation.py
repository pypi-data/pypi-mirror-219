import pytest
from robingame.animation import ease_in, ease_out, ease_in_out


@pytest.mark.parametrize(
    "func",
    [
        ease_in,
        ease_out,
        ease_in_out,
    ],
)
def test_ease_functions(func):
    assert func(x=0, start=3, stop=10, num=50) == 3
    assert func(x=50, start=3, stop=10, num=50) == 10
    with pytest.raises(ValueError) as e:
        func(x=51, start=3, stop=10, num=50)

    assert str(e.value) == "x=51 is greater than num=50"
