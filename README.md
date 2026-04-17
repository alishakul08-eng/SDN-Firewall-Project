# SDN-Firewall Project

## Student Information

- Alisha Kulshrestha -- PES1UG24CS049
- University: PES University

------------------------------------------------------------------------

# Project Overview

This project implements a Granular Layer-4 SDN Firewall using the Ryu controller and Mininet. The system demonstrates the core SDN principle of decoupling the control and data planes to enforce security policies at the network edge.

Key functionalities include:
- Centralized Management: Security logic resides in the Ryu controller.
- Dynamic Policy Enforcement: Pushing OpenFlow 1.3 rules to switch hardware.
- Protocol Filtering: Selective blocking of TCP Port 80 (HTTP) while permitting ICMP.
- Identity Awareness: Filtering based on unique Host MAC addresses.

------------------------------------------------------------------------

# Build and Run Instructions

## Prerequisites
Ensure Ryu and Mininet are installed on your Ubuntu VM.

------------------------------------------------------------------------

## Start the Controller
In a dedicated terminal, launch the firewall application:

ryu-manager firewall.py

------------------------------------------------------------------------

## Start the Network Topology
In a second terminal, launch the Mininet environment:

sudo mn --controller=remote,ip=127.0.0.1,port=6633 --mac

------------------------------------------------------------------------

## Verify Flow Tables
Check the hardware-level rules pushed by the controller:

mininet> sh ovs-ofctl -O OpenFlow13 dump-flows s1

------------------------------------------------------------------------

## Cleanup
Always clear the Mininet state after execution:

sudo mn -c

------------------------------------------------------------------------

# Proof of Execution (Screenshots and Logs)

![Flow Table](screenshots/flow_table.png)
Flow Tables: Output confirms the installation of high-priority flow rules (Priority 30) for TCP Port 80, ensuring unauthorized traffic is dropped at the switch level.

![Connectivity](screenshots/connectivity.png)
Ping Results: h1 ping h2 shows a 0% packet loss, confirming that general network connectivity is maintained for allowed protocols.

![Observation](screenshots/observation.png)
Performance Metrics: The iperf results show high-speed throughput (19.4 Gbits/sec), proving the firewall logic does not bottleneck the network performance.

![Blocking Controller](screenshots/blocking_controller.png)
Controller Status: The Ryu controller terminal shows the active monitoring and instantiation of the firewall application.

![Blocking Mininet](screenshots/blocking_mininet.jpg)
Functional Correctness: The Mininet console shows the h1 curl command hanging, demonstrating successful blocking of HTTP traffic for the unauthorized host.

------------------------------------------------------------------------

# Engineering Analysis

1. Flow Rule Logic
The firewall uses a Match-Action pipeline. When a packet matches the criteria (Src MAC: h1, Proto: TCP, Dst Port: 80), the action list is left empty, forcing the switch to drop the packet at the hardware level.

2. Priority Management
We assigned a Priority of 30 to security rules. This ensures they are evaluated before the default learning-switch rules (Priority 0), preventing unauthorized packets from being forwarded.

3. Performance and Latency
Testing showed an average RTT of 0.117 ms. This indicates that proactive rule installation minimizes the performance impact typically associated with SDN controllers.

------------------------------------------------------------------------

# Design Decisions and Tradeoffs

Tradeoff: Proactive vs. Reactive Rules
- Choice: Proactive.
- Reason: Rules are installed at handshake to avoid the PacketIn delay, ensuring the firewall does not bottleneck the network.

Tradeoff: Silent Drop vs. Reject
- Choice: Silent Drop.
- Reason: By not sending an ICMP unreachable message, we increase security by not acknowledging the firewalls presence to potential attackers.

------------------------------------------------------------------------

# References and Citations

1. Ryu SDN Framework: Official Documentation 
2. OpenFlow Switch Specification: Version 1.3.0
3. Mininet Walkthrough: SimpleSwitch13 implementation guides.

------------------------------------------------------------------------

# Conclusion

This project successfully fulfills the requirement for a functional SDN Firewall. By utilizing Python and the OpenFlow protocol, we achieved granular control over network traffic, proving that software-defined logic can effectively replace rigid hardware security configurations.
