
import os
from datetime import datetime

def generate_report(topo, parsed_files, outfile="output/report.txt"):
    lines = []
    lines.append("TOPOLOGY CREATION REPORT")
    lines.append("========================")
    lines.append(f"Generated at: {datetime.now().isoformat()}")
    lines.append("")

    lines.append("[1] Parsed configuration files:")
    for f in parsed_files:
        lines.append(f"    - {f}")
    lines.append("")

    lines.append("[2] Routers discovered:")
    for r in topo["routers"].keys():
        lines.append(f"    - {r}")
    lines.append("")

    lines.append("[3] Interfaces and IPs:")
    for rname, dev in topo["routers"].items():
        lines.append(f"    {rname}:")
        for intf, data in dev["interfaces"].items():
            ip = data.get("ip") or "unset"
            mask = data.get("mask") or ""
            shut = "shutdown" if data.get("shutdown") else "up"
            lines.append(f"        - {intf}: {ip} {mask} [{shut}]")
    lines.append("")

    lines.append("[4] Links inferred from shared subnets:")
    if topo["links"]:
        for link in topo["links"]:
            ep = link["endpoints"]
            lines.append(f"    - {ep[0]['router']}:{ep[0]['intf']}  <-->  {ep[1]['router']}:{ep[1]['intf']}   ({link['subnet']})")
    else:
        lines.append("    - None")
    lines.append("")

    lines.append("[5] LANs detected (single-router subnets):")
    if topo["lans"]:
        for lan in topo["lans"]:
            lines.append(f"    - {lan['router']}:{lan['intf']}   ({lan['subnet']})")
    else:
        lines.append("    - None")
    lines.append("")

    lines.append("[6] OSPF Summary:")
    for rname, dev in topo["routers"].items():
        ospf = dev.get("routing", {}).get("ospf")
        if ospf:
            rid = ospf.get("router_id") or "not set"
            nets = ", ".join([f"{n['network']} {n['wildcard']} area {n['area']}" for n in ospf.get("networks", [])]) or "no networks"
            lines.append(f"    - {rname}: process {ospf.get('process')} rid {rid} | {nets}")
        else:
            lines.append(f"    - {rname}: OSPF not configured")
    lines.append("")

    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, "w") as f:
        f.write("\n".join(lines))
