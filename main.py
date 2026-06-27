from src import extract, transform, load, visualize


def run():
    # 1. Extract
    raw = extract.fetch_shots()

    # 2. Transform
    shots = transform.clean_shots(raw)
    zones = transform.zone_efficiency(shots)

    print("\n[summary] zone efficiency")
    print(zones.to_string(index=False))

    # 3. Load
    load.save_processed(shots, zones)

    # 4. Visualize
    visualize.plot_shot_chart(shots)

    print("\n[done] pipeline complete")


if __name__ == "__main__":
    run()