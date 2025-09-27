#!/usr/bin/env python3
import os, glob, json
from modules.topology_builder import build_topology_from_files
from modules.report_generator import generate_report
from modules.visualizer import visualize_topology
from modules.recommendation import analyze_topology   # ✅ new import

def main():
    # Step 1: Find all .txt config files in src/configs
    files = sorted(glob.glob("src/configs/*.txt"))
    if not files:
        print("❌ No .txt configuration files found in src/configs/")
        return

    print(f"✅ Found {len(files)} config file(s).")

    # Step 2: Build topology
    topo = build_topology_from_files(files)

    os.makedirs("output", exist_ok=True)

    # Step 3: Save topology.json
    with open("output/topology.json", "w") as f:
        json.dump(topo, f, indent=2)
    print("✅ Wrote output/topology.json")

    # Step 4: Generate human-readable report
    generate_report(topo, files, outfile="output/report.txt")
    print("✅ Wrote output/report.txt")

    # Step 5: Visualize topology
    visualize_topology(topo, outfile="output/topology.png")
    print("✅ Wrote output/topology.png")

    # Step 6: Analyze configs for warnings & recommendations (verbose mode ON)
    analyze_topology(topo, outfile="output/recommendations.txt", verbose=True)
    print("✅ Wrote output/recommendations.txt")

    print("\n🎉 Done. Check the output/ directory for results:")
    print(" - topology.json")
    print(" - report.txt")
    print(" - topology.png")
    print(" - recommendations.txt")

if __name__ == "__main__":
    main()

