"""
-----------------
Network Hardening
-----------------

Network hardening refers to the configuration and tools used to protect a system from network-based threats. This can consist of using system firewalls, intrusion detection systems, and secure protocols.

See :kevlar-code:`600`.
"""

import re
import subprocess
import shutil
from typing import List, Optional

import pytest

from .decorators import full_version_only


@full_version_only
def test_dnssec_is_enabled() -> None:
    """
    DNSSEC enforcement should be enabled.
    =====================================

    DNSSEC is a standard that protects DNS lookups from spoofing or cache
    poisoning attacks. Without DNSSEC, there is no guarantee that the IP
    address the DNS server returned has not been maliciously altered.
    """
    ...


@full_version_only
def test_dns_over_tls_is_enabled() -> None:
    """
    DNS-over-TLS should be enabled.
    ===============================

    Encrypting DNS using standard TLS ensures attackers cannot view or alter
    domain name lookups.
    """
    ...


@full_version_only
def test_resolv_conf_uses_loopback() -> None:
    """
    ``/etc/resolv.conf`` should be configured to make secure DNS queries.
    =====================================================================

    By default a populated ``/etc/resolv.conf`` file will make insecure
    DNS queries.
    """
    ...


def _run(cmdline: List[str]) -> "subprocess.CompletedProcess[str]":
    """
    Run a command, capture output, and also make sure the output appears in the
    log.
    """
    result = subprocess.run(cmdline, text=True, capture_output=True)
    print(result.stdout)
    return result


IPTABLES_DIRECTION_INBOUND = "INPUT"
IPTABLES_DIRECTION_OUTBOUND = "OUTPUT"


def _get_iptables_policy(direction: str) -> Optional[str]:
    # Make sure we're not running iptables-nft, which is just nftables by
    # another name, but really using the legacy interface.

    if shutil.which("iptables-legacy"):
        iptables = "iptables-legacy"
    elif shutil.which("iptables-nft"):
        return None
    else:
        iptables = "iptables"

    try:
        result = _run([iptables, "-L", direction])
    except OSError:
        return None

    if result.returncode != 0:
        return None

    match = re.search(rf"Chain {re.escape(direction)} \(policy (\w+)\)", result.stdout)
    if match and match.group(1) == "DROP":
        return "drop"
    else:
        # Anything that is not DROP, we will treat as ACCEPT
        return "accept"


NFT_DIRECTION_INBOUND = "input"
NFT_DIRECTION_OUTBOUND = "output"


def _get_nftables_policy(direction: str) -> Optional[str]:
    try:
        result = _run(["nft", "-n", "list", "chains"])
    except OSError:
        return None

    if result.returncode != 0:
        return None

    policies = re.findall(
        rf"type filter hook {re.escape(direction)}.*policy (accept|drop)", result.stdout
    )

    # A single 'drop' will take precedence over any number of 'accepts', so
    # we only need to verify that one is present to be equivalent to a global
    # drop policy. An empty list is equivalent to "accept".
    if "drop" in policies:
        return "drop"
    return "accept"


def test_inbound_firewall_present() -> None:
    """
    A system should be protected by an inbound firewall.
    ====================================================

    All systems should have an operational inbound firewall to mitigate
    attacker surveillance and other malicious activity.
    """
    #
    # There are two failure scenarios that can be tested.
    # "No inbouund firewall", do not install nftables or iptables
    # "Firewall is configured to accept...", default INPUT policy is ACCEPT
    #
    # The test will pass if either iptables or nftables are installed and
    # default input policy is DROP:
    #
    # You can install iptables by adding IMAGE_INSTALL:append = " iptables"
    # You can install nftables by adding WRTEMPLATE += " feature/simple-firewall"
    #
    # You can change the default INPUT policy when using iptables:
    #
    # iptables --policy INPUT DROP
    #
    # You can change the default INPUT policy when using nft by editing
    # /etc/nftables.d/10-inbound.conf and changing:
    #
    # type filter hook input priority 0; policy drop;
    #
    # to
    #
    # type filter hook input priority 0; policy accept;
    #
    # Then restarting nftables (systemctl restart nftables)
    #
    iptables_policy = _get_iptables_policy(IPTABLES_DIRECTION_INBOUND)
    nftables_policy = _get_nftables_policy(NFT_DIRECTION_INBOUND)

    if iptables_policy is None and nftables_policy is None:
        pytest.fail("No inbound firewall enabled.")

    # It's probably not a good idea to use both iptables and nftables together,
    # but it will work just fine with a bit of care. If either one has a drop
    # policy, then the system is sufficiently locked down.
    assert (
        iptables_policy == "drop" or nftables_policy == "drop"
    ), "The system is **not** protected by an inbound firewall."


def test_outbound_firewall_present() -> None:
    """
    A system should be protected by an outbound firewall.
    =====================================================

    All systems should have an operational outbound firewall to mitigate
    efforts by an attacker to communicate with remote access tools, pivot to
    other systems, or perform denial of service attacks.
    """
    #
    # There is one failure scenario that can be tested.
    # "No outbouund firewall", do not install nftables or iptables
    #
    iptables_policy = _get_iptables_policy(IPTABLES_DIRECTION_OUTBOUND)
    nftables_policy = _get_nftables_policy(NFT_DIRECTION_OUTBOUND)

    if iptables_policy is None and nftables_policy is None:
        pytest.fail("No outbound firewall enabled.")
    assert (
        iptables_policy == "drop" or nftables_policy == "drop"
    ), "The system is **not** protected by an outbound firewall."


@full_version_only
def test_disallow_unencrypted_http() -> None:
    """
    Unencrypted Outbound web traffic should not be permitted.
    =========================================================

    All web traffic should be encrypted to prevent eavesdropping and tampering,
    even over the local network.
    """
    ...


@full_version_only
def test_disallow_unencrypted_mqtt() -> None:
    """
    Unencrypted Outbound MQTT traffic should not be permitted.
    ==========================================================

    All MQTT traffic should be encrypted to prevent eavesdropping and
    tampering, even over the local network.
    """
    ...
