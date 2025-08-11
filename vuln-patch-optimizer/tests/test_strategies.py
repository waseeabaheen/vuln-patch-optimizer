from vpo.patch.strategies import plan_waves

def test_plan_sizes():
    items = [{"severity":5,"cvss":9.0} for _ in range(10)] + [{"severity":3,"cvss":6.0} for _ in range(5)]
    waves = plan_waves(items, waves=3, policy="balanced")
    assert len(waves) == 3
    assert sum(len(w) for w in waves) == 15
