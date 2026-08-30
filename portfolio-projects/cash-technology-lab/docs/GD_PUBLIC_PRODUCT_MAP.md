# G+D Public Product Capability Map

This document records the **publicly documented product capabilities** used as domain references when designing the independent `cash-technology-lab` project.

No proprietary implementation detail, source code, firmware, protocol, credential, license key, or non-public document is included.

## Banknote processing systems

| Public product | Publicly described capabilities used as domain reference | Lab mapping |
| --- | --- | --- |
| BPS C1 | Counting/authentication, denomination/series/orientation sorting, up to ten currencies, fitness sorting, serial-number reading, up to 1,300 notes/min | `bps-c1` profile, processing modes, reject path, serial capture |
| BPS C2-4 evo | Four output compartments plus reject, denomination/orientation/fitness sorting, 1,050 notes/min | `bps-c2-4` profile and multi-stacker routing |
| BPS C6 | Up to 72,000 notes/hour, modular design, up to 20 output stackers, connectivity to cash-management software | `bps-c6` profile and device-gateway boundary |
| BPS M3 / M evo | Heavy-duty processing up to 76,000 notes/hour; M evo software platform | `bps-m3` high-throughput simulation profile |
| BPS M5 / M evo | 24/7 commercial operation and up to 120,000 notes/hour; integrated software/security platform | `bps-m5` high-throughput profile and monitoring concepts |
| BPS M7 / M evo | High-speed central-bank processing up to 120,000 notes/hour, serial-number reading, advanced sensor/classification functions | `bps-m7` profile and serial-capture workflow |

## Public software / ecosystem concepts

### Compass Cash Center

Public G+D material describes capabilities including:

- end-to-end cash-management visibility
- receiving and deposit workflows
- inventory management
- order and ATM-related workflows in applicable variants
- cash-center automation
- full track-and-trace
- real-time operational KPIs
- reporting
- role-based access
- integration with G+D and third-party cash-processing devices through standard interfaces

**Lab mapping:** processing-session summaries, future deposit reconciliation, fleet KPIs, device gateway, audit trail, and planned role model.

### BPS M evo software

Public G+D material describes M evo as a common software platform for BPS M systems with a modern user interface, configuration capabilities, security mechanisms, integrated firewall, and encrypted data transmission.

**Lab mapping:** no clone is attempted. The project instead demonstrates separation of UI/business logic/device transport and secure integration boundaries.

### BPS Eco-Remote

Public G+D material identifies Eco-Remote as a remote-management solution in the BPS ecosystem.

**Lab mapping:** `monitor.py` demonstrates original health/KPI/alert concepts for a simulated device fleet.

### BPS Eco-Protect

Public G+D material identifies Eco-Protect as an industrial firewall product in the BPS ecosystem.

**Lab mapping:** this project does not implement or emulate the firewall. Security boundaries are represented only as architectural concerns.

## Public sources

- https://www.gi-de.com/en/currency-technology/currency-management/scalable-cash-cycle-solutions/banknote-processing-systems/bps-c1
- https://www.gi-de.com/en/currency-technology/currency-management/scalable-cash-cycle-solutions/banknote-processing-systems/bps-c2-family
- https://www.gi-de.com/en/payment/cash/scalable-cash-cycle-solutions/banknote-processing-systems/bps-c6
- https://www.gi-de.com/en/currency-technology/currency-management/scalable-cash-cycle-solutions/banknote-processing-systems/bps-m3
- https://www.gi-de.com/en/currency-technology/currency-management/scalable-cash-cycle-solutions/banknote-processing-systems/bps-m5
- https://www.gi-de.com/en/currency-technology/currency-management/scalable-cash-cycle-solutions/banknote-processing-systems/bps-m7
- https://www.gi-de.com/en/currency-technology/currency-management/digital-solutions/commercial-banks-cash-management-software/compass-cash-center

## Trademark / affiliation notice

G+D and all named G+D products belong to their respective rights holder. This educational portfolio project is independent and unofficial.
