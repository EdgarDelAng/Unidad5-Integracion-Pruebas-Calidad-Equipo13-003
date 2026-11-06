from src.domain import Order


def test_no_se_puede_confirmar_dos_veces():
    order = Order(total=200, vip=False)
    order.confirm()
    try:
        order.confirm()
    except ValueError as exc:
        assert str(exc) == "already confirmed"
    else:
        raise AssertionError("La segunda confirmación debe rechazarse")
