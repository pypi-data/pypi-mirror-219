import finesse


def test_phase_level_change():
    # Issue 506
    model = finesse.Model()
    model.phase_level = 1
    assert model.phase_level == 1
    model.phase_level = 2
    assert model.phase_level == 2
