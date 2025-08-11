from vpo.metrics import exposure_reduction, estimate_mttr_improvement, sla_compliance

def test_exposure_reduction():
    assert exposure_reduction(100, 65) == 35.0

def test_mttr_improvement():
    imp = estimate_mttr_improvement(30, 3)
    assert 0 <= imp <= 100

def test_sla_compliance():
    val = sla_compliance([{"severity":5}], 14, [[{"severity":5}]])
    assert 90.0 <= val <= 100.0
