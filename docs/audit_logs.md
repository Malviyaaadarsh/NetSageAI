# NetSage AI Audit Log

This file records human review decisions for AI diagnoses.

## 2026-08-24T08:52:00Z - NET-001
- Decision: Edited
- Reviewer: demo-seed
- AI Root Cause: Draft AI diagnosis for NET-001
- AI Confidence: 0.55
- Agreement: False
- Reviewer Fix: Sub-interface administratively down
- Reviewer Reason: Seeded correction entry for Responsible AI evidence.

## 2026-08-24T08:52:00Z - NET-002
- Decision: Rejected
- Reviewer: demo-seed
- AI Root Cause: Draft AI diagnosis for NET-002
- AI Confidence: 0.55
- Agreement: False
- Reviewer Fix: DHCP Scope Pool Exhaustion
- Reviewer Reason: Seeded correction entry for Responsible AI evidence.

## 2026-08-24T08:52:00Z - NET-003
- Decision: Edited
- Reviewer: demo-seed
- AI Root Cause: Draft AI diagnosis for NET-003
- AI Confidence: 0.55
- Agreement: False
- Reviewer Fix: DNS service disabled on client subnet gateway
- Reviewer Reason: Seeded correction entry for Responsible AI evidence.

## 2026-08-24T08:52:00Z - NET-004
- Decision: Rejected
- Reviewer: demo-seed
- AI Root Cause: Draft AI diagnosis for NET-004
- AI Confidence: 0.55
- Agreement: False
- Reviewer Fix: OSPF Hello Timer Mismatch
- Reviewer Reason: Seeded correction entry for Responsible AI evidence.

## 2026-08-24T08:52:00Z - NET-005
- Decision: Edited
- Reviewer: demo-seed
- AI Root Cause: Draft AI diagnosis for NET-005
- AI Confidence: 0.55
- Agreement: False
- Reviewer Fix: Extended ACL blocking HTTP traffic
- Reviewer Reason: Seeded correction entry for Responsible AI evidence.

## 2026-08-24T08:52:59Z - NET-013
- Decision: Accepted
- Reviewer: operator
- AI Root Cause: Switch port FastEthernet0/10 is incorrectly assigned to VLAN 14 instead of VLAN 40.
- AI Confidence: 0.95
- Agreement: True
- Reviewer Fix: configure terminal
interface FastEthernet0/10
switchport access vlan 40
- Reviewer Reason: 

