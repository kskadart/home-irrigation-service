
def to_moisture_percent(raw: int, dry_raw: int, wet_raw: int) -> float:
    raw = max(min(raw, dry_raw), wet_raw)
    return (dry_raw - raw) / (dry_raw - wet_raw)


def test_calibration_mapping():
    dry_raw = 21000
    wet_raw = 11000

    assert to_moisture_percent(dry_raw, dry_raw, wet_raw) == 0.0
    assert to_moisture_percent(wet_raw, dry_raw, wet_raw) == 1.0

    mid = (dry_raw + wet_raw) // 2
    mid_pct = to_moisture_percent(mid, dry_raw, wet_raw)
    assert 0.45 < mid_pct < 0.55
