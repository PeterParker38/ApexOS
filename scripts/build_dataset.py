import fastf1
import pandas as pd

from f1.data import ROOT, load_race_laps

YEARS = [2023]
OUT = ROOT / "data" / "processed" / "laps.parquet"


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames, failed = [], []

    for year in YEARS:
        schedule = fastf1.get_event_schedule(year, include_testing=False)
        for rnd in schedule["RoundNumber"]:
            try:
                frames.append(load_race_laps(year, int(rnd)))
                print(f"OK    {year} round {rnd}")
            except Exception as e:
                failed.append((year, int(rnd), repr(e)))
                print(f"FAIL  {year} round {rnd}: {e!r}")

    df = pd.concat(frames, ignore_index=True)
    n_dup = df.duplicated(["Year", "Round", "Driver", "LapNumber"]).sum()
    assert n_dup == 0, f"{n_dup} duplicate driver-laps"

    df.to_parquet(OUT, index=False)
    print(f"\nSaved {len(df)} laps from {len(frames)} races to {OUT}")
    print(f"Failed: {failed}")


if __name__ == "__main__":
    main()