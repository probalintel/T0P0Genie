
import os
from ipaddress import IPv4Network, IPv4Address, ip_network
from modules.parser import parse_file, dotted_mask_to_prefix

def interface_network(ip: str, mask: str):
    if not ip or not mask:
        return None
    try:
        prefix = dotted_mask_to_prefix(mask)
        return ip_network(f"{ip}/{prefix}", strict=False)
    except Exception:
        return None

def build_topology_from_files(file_paths):
    """
    Build a unified topology dict from multiple Cisco config .txt files.
    Detects router nodes, their interfaces, and infers links by shared subnets.
    """
    topo = {"routers": {}, "links": [], "lans": []}
    # Parse all devices
    for path in file_paths:
        dev = parse_file(path)
        name = dev.get("hostname") or os.path.splitext(os.path.basename(path))[0]
        topo["routers"][name] = dev

    # Build subnet -> [(router, intf)] map
    subnet_map = {}
    for rname, dev in topo["routers"].items():
        for intf, data in dev["interfaces"].items():
            net = interface_network(data.get("ip"), data.get("mask"))
            if net:
                subnet_map.setdefault(str(net), []).append({"router": rname, "intf": intf})

    # Create links for subnets shared by 2+ routers; otherwise mark as LAN
    for net_str, endpoints in subnet_map.items():
        if len(endpoints) >= 2:
            # Create pairwise links (for 2, it'll be one; for >2, make full mesh edges)
            for i in range(len(endpoints)):
                for j in range(i+1, len(endpoints)):
                    topo["links"].append({
                        "subnet": net_str,
                        "endpoints": [
                            {"router": endpoints[i]["router"], "intf": endpoints[i]["intf"]},
                            {"router": endpoints[j]["router"], "intf": endpoints[j]["intf"]},
                        ]
                    })
        else:
            # Likely a LAN hanging off a single router
            topo["lans"].append({
                "subnet": net_str,
                "router": endpoints[0]["router"],
                "intf": endpoints[0]["intf"]
            })
    return topo
