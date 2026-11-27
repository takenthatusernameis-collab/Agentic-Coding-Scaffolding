"""Probe candidate numeric helpers for undocumented OverflowError on huge ints."""

import cooldown_utils as cu
import duration_utils as du
import interval_utils as iu
import number_utils as nu
import semver_utils as sv

BIG = 10 ** 400
BIG2 = 2 ** 2000


def probe(label, fn):
    try:
        r = fn()
        print(f"OK      {label}: {r!r}")
    except OverflowError as e:
        print(f"OVERFLOW {label}: {e}")
    except ValueError as e:
        print(f"VALUE   {label}: {e}")
    except Exception as e:
        print(f"{type(e).__name__:8} {label}: {e}")


print("=== duration_utils ===")
probe("format_duration(BIG)", lambda: du.format_duration(BIG))
probe("format_duration(BIG2)", lambda: du.format_duration(BIG2))
probe("seconds_to_hms(BIG)", lambda: du.seconds_to_hms(BIG))
probe("hms_to_seconds(hours=BIG)", lambda: du.hms_to_seconds(hours=BIG))
probe("to_seconds(hours=BIG)", lambda: du.to_seconds(hours=BIG))
probe("to_seconds(milliseconds=BIG)", lambda: du.to_seconds(milliseconds=BIG))

print("=== interval_utils ===")
probe("normalize_interval(BIG, 5)", lambda: iu.normalize_interval(BIG, 5))
probe("interval_length((0, BIG))", lambda: iu.interval_length((0, BIG)))
probe("interval_midpoint((0, BIG))", lambda: iu.interval_midpoint((0, BIG)))
probe("interval_distance((0,1),(BIG,BIG+1))", lambda: iu.interval_distance((0, 1), (BIG, BIG + 1)))
probe("interval_shift((0,1), BIG)", lambda: iu.interval_shift((0, 1), BIG))
probe("interval_clamp(BIG, (0,1))", lambda: iu.interval_clamp(BIG, (0, 1)))

print("=== number_utils ===")
probe("percentage(BIG, 1)", lambda: nu.percentage(BIG, 1))
probe("map_range(BIG, 0, 1, 0, 1)", lambda: nu.map_range(BIG, 0, 1, 0, 1))
probe("safe_divide(BIG, 1)", lambda: nu.safe_divide(BIG, 1))
probe("is_close(BIG, BIG)", lambda: nu.is_close(BIG, BIG))
probe("round_half_up(BIG, 2)", lambda: nu.round_half_up(BIG, 2))
probe("format_number(BIG)", lambda: nu.format_number(BIG))
probe("lerp(BIG, BIG, 0.5)", lambda: nu.lerp(BIG, BIG, 0.5))
probe("lerp(0, BIG, 0.5)", lambda: nu.lerp(0, BIG, 0.5))
probe("round_to(BIG, 2)", lambda: nu.round_to(BIG, 2))
probe("is_integer(BIG)", lambda: nu.is_integer(BIG))

print("=== semver_utils ===")
probe("bump_major huge", lambda: sv.bump_major(f"{BIG}.0.0"))
probe("compare_semver huge", lambda: sv.compare_semver(f"{BIG}.0.0", "1.0.0"))

print("=== cooldown_utils ===")
probe("Cooldown(BIG)", lambda: cu.Cooldown(BIG))
probe("format_remaining(BIG)", lambda: cu.format_remaining(BIG))
