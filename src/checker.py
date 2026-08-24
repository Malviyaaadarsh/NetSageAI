from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, Iterable, List, Mapping


@dataclass(frozen=True)
class Rule:
	rule_id: str
	title: str
	pattern: str
	root_cause: str
	osi_layer: str
	next_command: str
	fix_steps: List[str]
	base_confidence: float


RULES: List[Rule] = [
	Rule(
		rule_id="R-IF-DOWN",
		title="Interface administratively down",
		pattern=r"administratively down|\bshutdown\b",
		root_cause="Interface or sub-interface is shut down.",
		osi_layer="Layer 2/3",
		next_command="show ip interface brief",
		fix_steps=[
			"configure terminal",
			"interface <affected-interface>",
			"no shutdown",
		],
		base_confidence=0.95,
	),
	Rule(
		rule_id="R-DHCP-POOL-EXHAUST",
		title="DHCP pool exhaustion",
		pattern=r"apipa|leased\s+\d+;\s*zero available|pool exhaustion",
		root_cause="DHCP scope is exhausted or unavailable.",
		osi_layer="Layer 7",
		next_command="show ip dhcp pool",
		fix_steps=[
			"Review DHCP pool size and exclusions",
			"Increase pool range or release stale leases",
		],
		base_confidence=0.9,
	),
	Rule(
		rule_id="R-DNS-MISCONFIG",
		title="DNS misconfiguration",
		pattern=r"name-server.*not active|no ip domain-lookup|cannot open .*\.com|dns",
		root_cause="DNS service or DNS path is misconfigured.",
		osi_layer="Layer 7",
		next_command="show run | include name-server|show hosts",
		fix_steps=[
			"Configure valid DNS servers on gateway/client",
			"Verify DNS reachability and resolver service",
		],
		base_confidence=0.78,
	),
	Rule(
		rule_id="R-ACL-BLOCK",
		title="ACL blocking intended traffic",
		pattern=r"access-list .* deny|missing port 21|missing port 443|overly permissive acl",
		root_cause="ACL policy does not match intended traffic rules.",
		osi_layer="Layer 3/4",
		next_command="show access-lists",
		fix_steps=[
			"Review ACL order and implicit deny",
			"Permit required traffic and re-apply ACL",
		],
		base_confidence=0.88,
	),
	Rule(
		rule_id="R-NAT-MISCONFIG",
		title="NAT rule or direction missing",
		pattern=r"missing overload|missing ip nat inside|nat.*not working",
		root_cause="NAT translation rule or interface direction is incomplete.",
		osi_layer="Layer 3",
		next_command="show run | section ip nat",
		fix_steps=[
			"Add missing PAT overload or static NAT command",
			"Ensure inside/outside is configured on interfaces",
		],
		base_confidence=0.92,
	),
	Rule(
		rule_id="R-TRUNK-VLAN",
		title="Trunk VLAN mismatch or missing VLAN",
		pattern=r"trunk.*missing|allowed vlan.*missing|native vlan mismatch|wrong access vlan",
		root_cause="VLAN or trunk configuration mismatch blocks traffic forwarding.",
		osi_layer="Layer 2",
		next_command="show interfaces trunk",
		fix_steps=[
			"Align trunk mode, native VLAN, and allowed VLAN list",
			"Assign endpoints to correct access VLAN",
		],
		base_confidence=0.9,
	),
	Rule(
		rule_id="R-GATEWAY-SUBNET",
		title="Default gateway/subnet mismatch",
		pattern=r"default gateway.*misconfiguration|outside subnet boundary|gateway.*outside",
		root_cause="Host gateway does not belong to the host subnet or is misconfigured.",
		osi_layer="Layer 3",
		next_command="ipconfig /all",
		fix_steps=[
			"Set correct default gateway for the host subnet",
			"Validate subnet mask and host IP",
		],
		base_confidence=0.89,
	),
	Rule(
		rule_id="R-ROUTING-CTRL",
		title="Routing control-plane mismatch",
		pattern=r"hello-interval|passive-interface|missing subnets keyword|invalid static route next-hop",
		root_cause="Routing protocol or static route parameters are inconsistent.",
		osi_layer="Layer 3",
		next_command="show ip route|show ip ospf neighbor",
		fix_steps=[
			"Align protocol timers/flags and passive interfaces",
			"Correct invalid next-hop and redistribute options",
		],
		base_confidence=0.86,
	),
	Rule(
		rule_id="R-DUP-IP",
		title="Duplicate IP conflict",
		pattern=r"duplicate address|dup_addr",
		root_cause="At least two nodes are configured with the same IP address.",
		osi_layer="Layer 3",
		next_command="show ip arp",
		fix_steps=[
			"Identify conflicting hosts",
			"Assign unique IP and clear ARP entries if needed",
		],
		base_confidence=0.97,
	),
	Rule(
		rule_id="R-DHCP-RELAY",
		title="Missing DHCP relay",
		pattern=r"missing ip helper-address|dhcp relay failing",
		root_cause="DHCP relay (ip helper-address) is missing on routed client interface.",
		osi_layer="Layer 3/7",
		next_command="show run interface <client-gateway-if>",
		fix_steps=[
			"Configure ip helper-address <dhcp-server-ip>",
			"Verify UDP relay reachability",
		],
		base_confidence=0.93,
	),
]


def _to_text(value: object) -> str:
	if value is None:
		return ""
	return str(value)


def _extract_evidence(text: str, pattern: str) -> str:
	match = re.search(pattern, text, flags=re.IGNORECASE)
	if not match:
		return "No direct evidence match found."
	start = max(0, match.start() - 45)
	end = min(len(text), match.end() + 90)
	snippet = text[start:end].strip()
	return " ".join(snippet.split())


def run_rule_engine(show_outputs: str) -> List[Dict[str, object]]:
	findings: List[Dict[str, object]] = []
	haystack = _to_text(show_outputs)

	for rule in RULES:
		if re.search(rule.pattern, haystack, flags=re.IGNORECASE):
			findings.append(
				{
					"rule_id": rule.rule_id,
					"title": rule.title,
					"root_cause": rule.root_cause,
					"osi_layer": rule.osi_layer,
					"confidence": round(rule.base_confidence, 2),
					"evidence": _extract_evidence(haystack, rule.pattern),
					"next_command": rule.next_command,
					"fix_steps": rule.fix_steps,
				}
			)

	findings.sort(key=lambda row: row["confidence"], reverse=True)
	return findings


def diagnose_with_rules(case: Mapping[str, object]) -> Dict[str, object]:
	show_outputs = _to_text(case.get("show_outputs"))
	findings = run_rule_engine(show_outputs)

	if findings:
		primary = findings[0]
		return {
			"status": "ERRORS_DETECTED",
			"primary_finding": primary,
			"findings": findings,
			"summary": f"{len(findings)} rule(s) matched. Top match: {primary['title']}",
		}

	return {
		"status": "NO_STRONG_RULE_MATCH",
		"primary_finding": {
			"rule_id": "R-NONE",
			"title": "No deterministic match",
			"root_cause": "No high-confidence deterministic signature matched this output.",
			"osi_layer": _to_text(case.get("osi_layer")) or "Unknown",
			"confidence": 0.35,
			"evidence": "No static regex rule matched the provided show_outputs.",
			"next_command": "show run",
			"fix_steps": ["Collect more evidence before remediation."],
		},
		"findings": [],
		"summary": "No deterministic signature detected; escalate to LLM inference.",
	}


def run_batch(cases: Iterable[Mapping[str, object]]) -> List[Dict[str, object]]:
	output: List[Dict[str, object]] = []
	for case in cases:
		output.append(
			{
				"case_id": _to_text(case.get("case_id")),
				"checker": diagnose_with_rules(case),
			}
		)
	return output

