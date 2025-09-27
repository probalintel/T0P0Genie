import os

def analyze_device(dev, verbose=False):
    """
    Analyze a single device configuration dict (from parser.py).
    Returns warnings + recommendations.
    """
    warnings = []
    recommendations = []

    hostname = dev.get("hostname", "Unknown")
    if verbose: print(f"\n🔎 Analyzing {hostname}...")

    # --- Interface Checks ---
    for intf, data in dev.get("interfaces", {}).items():
        ip = data.get("ip")
        mask = data.get("mask")

        if not ip:
            warnings.append(f"[{hostname}] {intf} has no IP configured.")
            if verbose: print(f" ⚠️ {intf} has no IP configured.")

        if data.get("shutdown"):
            recommendations.append(f"[{hostname}] {intf} is shutdown. Enable only if needed.")
            if verbose: print(f" 🔒 {intf} is shutdown (secure if unused).")

        if mask and mask == "255.255.255.255":
            warnings.append(f"[{hostname}] {intf} uses /32 mask — unusual for LAN/WAN.")
            if verbose: print(f" ⚠️ {intf} has /32 mask (check).")

        mtu = data.get("mtu")
        if mtu:
            if int(mtu) < 1400:
                warnings.append(f"[{hostname}] {intf} has low MTU {mtu}, may cause fragmentation.")
                if verbose: print(f" ⚠️ {intf} MTU too low ({mtu}).")

    # --- OSPF Checks ---
    ospf = dev.get("routing", {}).get("ospf")
    if ospf:
        if verbose: print(f" ✅ OSPF detected (process {ospf.get('process')}).")

        if not ospf.get("router_id"):
            warnings.append(f"[{hostname}] OSPF router-id not set explicitly (best practice).")
            if verbose: print(" ⚠️ OSPF router-id not set.")

        if not ospf.get("networks"):
            warnings.append(f"[{hostname}] OSPF configured but no networks advertised.")
            if verbose: print(" ⚠️ OSPF has no networks configured.")

        for net in ospf.get("networks", []):
            if net["area"] != 0:
                recommendations.append(f"[{hostname}] Consider multi-area OSPF only if network is large.")
    else:
        recommendations.append(f"[{hostname}] No dynamic routing (OSPF/EIGRP). Use static if very small network.")
        if verbose: print(" ℹ️ No OSPF/EIGRP detected.")

    # --- Security Checks (basic) ---
    if not dev.get("enable_secret"):
        warnings.append(f"[{hostname}] No enable secret set — insecure!")
        if verbose: print(" ⚠️ Missing enable secret.")

    if not dev.get("service_password_encryption"):
        recommendations.append(f"[{hostname}] Enable 'service password-encryption' to protect plain-text passwords.")
        if verbose: print(" 🔒 Recommend enabling password encryption.")

    if not dev.get("vty_password"):
        warnings.append(f"[{hostname}] VTY lines without password/login — remote access insecure!")
        if verbose: print(" ⚠️ VTY password missing.")

    return warnings, recommendations


def recommend_protocol(topo):
    """
    Suggest a routing protocol based on network size and topology.
    """
    num_routers = len(topo.get("routers", {}))
    if num_routers <= 2:
        return "Static routing is sufficient (small network)."
    elif num_routers <= 5:
        return "OSPF or EIGRP recommended (small-to-medium)."
    elif num_routers <= 15:
        return "EIGRP or OSPF multi-area recommended (scales better)."
    else:
        return "Consider OSPF multi-area or BGP (large/enterprise)."


def analyze_topology(topo, outfile="output/recommendations.txt", verbose=False):
    """
    Main function: analyze full topology and write recommendations.
    """
    all_warnings = []
    all_recs = []

    if verbose: print("\n🚀 Starting Network Audit...\n")

    for rname, dev in topo.get("routers", {}).items():
        w, r = analyze_device(dev, verbose=verbose)
        all_warnings.extend(w)
        all_recs.extend(r)

    # Protocol suggestion
    proto_suggestion = recommend_protocol(topo)
    all_recs.append(f"[GLOBAL] {proto_suggestion}")
    if verbose: print(f"\n🌍 Protocol Suggestion: {proto_suggestion}")

    # Write report
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, "w") as f:
        f.write("NETWORK RECOMMENDATION REPORT\n")
        f.write("=============================\n\n")
        f.write("⚠️ WARNINGS (potential misconfigs):\n")
        if all_warnings:
            for w in all_warnings:
                f.write(f" - {w}\n")
        else:
            f.write(" - None\n")
        f.write("\n")

        f.write("💡 RECOMMENDATIONS:\n")
        for r in all_recs:
            f.write(f" - {r}\n")

    if verbose:
        print("\n✅ Audit complete. Detailed report saved to", outfile)

    return outfile

