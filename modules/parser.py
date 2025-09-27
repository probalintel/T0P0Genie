
import re
from ipaddress import IPv4Network, IPv4Address

HOSTNAME_RE = re.compile(r'^\s*hostname\s+(\S+)', re.IGNORECASE)
INTF_RE = re.compile(r'^\s*interface\s+(\S+)', re.IGNORECASE)
IP_ADDR_RE = re.compile(r'^\s*ip\s+address\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', re.IGNORECASE)
SHUT_RE = re.compile(r'^\s*shutdown\s*$', re.IGNORECASE)
ROUTER_OSPF_RE = re.compile(r'^\s*router\s+ospf\s+(\d+)', re.IGNORECASE)
ROUTER_ID_RE = re.compile(r'^\s*router-id\s+(\d+\.\d+\.\d+\.\d+)', re.IGNORECASE)
NETWORK_RE = re.compile(r'^\s*network\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+area\s+(\d+)', re.IGNORECASE)

def dotted_mask_to_prefix(mask: str) -> int:
    parts = [int(x) for x in mask.split('.')]
    bits = ''.join(f'{p:08b}' for p in parts)
    return bits.count('1')

def parse_config_text(lines):
    """
    Parse Cisco IOS running-config text lines.
    Returns a dict with hostname, interfaces, and routing (OSPF).
    """
    device = {
        "hostname": None,
        "interfaces": {},     # {intf: {"ip": "x.x.x.x", "mask": "x.x.x.x", "shutdown": bool}}
        "routing": {}         # {"ospf": {"process": N, "router_id": str|None, "networks":[{"network":..., "wildcard":..., "area":...}]}}
    }

    current_intf = None
    in_router_ospf = False

    for raw in lines:
        line = raw.rstrip()

        m = HOSTNAME_RE.match(line)
        if m:
            device["hostname"] = m.group(1)
            continue

        m = INTF_RE.match(line)
        if m:
            current_intf = m.group(1)
            device["interfaces"].setdefault(current_intf, {"ip": None, "mask": None, "shutdown": False})
            in_router_ospf = False
            continue

        if current_intf:
            m = IP_ADDR_RE.match(line)
            if m:
                device["interfaces"][current_intf]["ip"] = m.group(1)
                device["interfaces"][current_intf]["mask"] = m.group(2)
                continue
            m = SHUT_RE.match(line)
            if m:
                device["interfaces"][current_intf]["shutdown"] = True
                continue

        m = ROUTER_OSPF_RE.match(line)
        if m:
            in_router_ospf = True
            device["routing"].setdefault("ospf", {"process": int(m.group(1)), "router_id": None, "networks": []})
            current_intf = None
            continue

        if in_router_ospf:
            m = ROUTER_ID_RE.match(line)
            if m:
                device["routing"]["ospf"]["router_id"] = m.group(1)
                continue
            m = NETWORK_RE.match(line)
            if m:
                device["routing"]["ospf"]["networks"].append({
                    "network": m.group(1),
                    "wildcard": m.group(2),
                    "area": int(m.group(3))
                })
                continue

    return device

def parse_file(path: str):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    return parse_config_text(lines)
