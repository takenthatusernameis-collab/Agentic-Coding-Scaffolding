"""Tests for ipaddress_utils."""

import unittest

import ipaddress_utils
from ipaddress_utils import (
    AddressValueError,
    IPv4Address,
    IPv4Interface,
    IPv4Network,
    IPv6Address,
    IPv6Interface,
    IPv6Network,
    NetmaskValueError,
    address_version,
    address_within,
    common_prefix_length,
    from_packed,
    ip_address,
    ip_interface,
    ip_network,
    is_valid_address,
    is_valid_interface,
    is_valid_network,
    network_hosts,
    network_overlaps,
    next_address,
    previous_address,
    sort_addresses,
    subnets,
    summarize_addresses,
    to_packed,
)

LAST_IPV4 = "255.255.255.255"
FIRST_IPV4 = "0.0.0.0"
LAST_IPV6 = "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"
FIRST_IPV6 = "::"


class TestAddressParsing(unittest.TestCase):
    """Verify the helpers that build the objects of the standard library."""

    def test_ip_address_reads_a_text(self):
        address = ip_address("192.0.2.1")
        self.assertIsInstance(address, IPv4Address)
        self.assertEqual(str(address), "192.0.2.1")

    def test_ip_address_reads_an_ipv6_text(self):
        address = ip_address("2001:db8::1")
        self.assertIsInstance(address, IPv6Address)
        self.assertEqual(str(address), "2001:db8::1")

    def test_ip_address_reads_an_integer(self):
        self.assertEqual(str(ip_address(3221225985)), "192.0.2.1")

    def test_ip_address_reads_packed_bytes(self):
        self.assertEqual(str(ip_address(b"\xc0\x00\x02\x01")), "192.0.2.1")

    def test_ip_address_rejects_an_unknown_type(self):
        with self.assertRaises(TypeError):
            ip_address(None)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ip_address(1.5)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            ip_address(["192.0.2.1"])  # type: ignore[list-item]

    def test_ip_address_rejects_a_boolean(self):
        with self.assertRaises(TypeError):
            ip_address(True)  # type: ignore[arg-type]

    def test_ip_address_rejects_an_invalid_text(self):
        with self.assertRaises(ValueError):
            ip_address("192.0.2.300")
        with self.assertRaises(ValueError):
            ip_address("not an address")

    def test_ip_network_reads_a_text(self):
        network = ip_network("192.0.2.0/24")
        self.assertIsInstance(network, IPv4Network)
        self.assertEqual(str(network), "192.0.2.0/24")

    def test_ip_network_reads_a_pair(self):
        network = ip_network(("192.0.2.0", 24))
        self.assertEqual(str(network), "192.0.2.0/24")

    def test_ip_network_masks_the_host_bits_when_it_is_not_strict(self):
        network = ip_network("192.0.2.1/24", strict=False)
        self.assertEqual(str(network), "192.0.2.0/24")

    def test_ip_network_rejects_the_host_bits_when_it_is_strict(self):
        with self.assertRaises(ValueError):
            ip_network("192.0.2.1/24")

    def test_ip_network_rejects_an_unknown_type(self):
        with self.assertRaises(TypeError):
            ip_network(None)  # type: ignore[arg-type]

    def test_ip_network_rejects_a_non_boolean_strict_flag(self):
        with self.assertRaises(TypeError):
            ip_network("192.0.2.0/24", strict="yes")  # type: ignore[arg-type]

    def test_ip_network_rejects_a_pair_of_the_wrong_size(self):
        with self.assertRaises(ValueError):
            ip_network(("192.0.2.0", 24, 1))  # type: ignore[arg-type]

    def test_ip_network_rejects_a_prefix_length_that_is_not_an_integer(self):
        with self.assertRaises(TypeError):
            ip_network(("192.0.2.0", "24"))  # type: ignore[arg-type]

    def test_ip_interface_reads_a_text(self):
        interface = ip_interface("192.0.2.1/24")
        self.assertIsInstance(interface, IPv4Interface)
        self.assertEqual(str(interface), "192.0.2.1/24")

    def test_ip_interface_reads_an_ipv6_text(self):
        interface = ip_interface("2001:db8::1/64")
        self.assertIsInstance(interface, IPv6Interface)
        self.assertEqual(str(interface), "2001:db8::1/64")

    def test_ip_interface_reads_a_pair(self):
        self.assertEqual(str(ip_interface(("192.0.2.1", 24))), "192.0.2.1/24")

    def test_ip_interface_rejects_an_unknown_type(self):
        with self.assertRaises(TypeError):
            ip_interface(None)  # type: ignore[arg-type]


class TestValidityChecks(unittest.TestCase):
    """Verify the checks that never raise."""

    def test_is_valid_address_accepts_a_valid_address(self):
        self.assertTrue(is_valid_address("192.0.2.1"))
        self.assertTrue(is_valid_address("2001:db8::1"))
        self.assertTrue(is_valid_address(3232235777))
        self.assertTrue(is_valid_address(b"\xc0\x00\x02\x01"))

    def test_is_valid_address_rejects_an_invalid_address(self):
        self.assertFalse(is_valid_address("192.0.2.300"))
        self.assertFalse(is_valid_address(""))
        self.assertFalse(is_valid_address(None))
        self.assertFalse(is_valid_address(True))
        self.assertFalse(is_valid_address(1.5))

    def test_is_valid_network_accepts_a_valid_network(self):
        self.assertTrue(is_valid_network("192.0.2.0/24"))
        self.assertTrue(is_valid_network("2001:db8::/32"))

    def test_is_valid_network_rejects_a_network_with_host_bits(self):
        self.assertFalse(is_valid_network("192.0.2.1/24"))

    def test_is_valid_network_rejects_an_unknown_type(self):
        self.assertFalse(is_valid_network(None))
        self.assertFalse(is_valid_network(True))

    def test_is_valid_interface_accepts_a_valid_interface(self):
        self.assertTrue(is_valid_interface("192.0.2.1/24"))
        self.assertTrue(is_valid_interface("2001:db8::1/64"))

    def test_is_valid_interface_rejects_an_invalid_interface(self):
        self.assertFalse(is_valid_interface("192.0.2.1/99"))
        self.assertFalse(is_valid_interface(None))


class TestPackedForm(unittest.TestCase):
    """Verify the packed form of an address."""

    def test_to_packed_returns_four_bytes_for_ipv4(self):
        packed = to_packed("192.0.2.1")
        self.assertEqual(packed, b"\xc0\x00\x02\x01")
        self.assertEqual(len(packed), 4)

    def test_to_packed_returns_sixteen_bytes_for_ipv6(self):
        packed = to_packed("2001:db8::1")
        self.assertEqual(len(packed), 16)

    def test_to_packed_rejects_an_invalid_address(self):
        with self.assertRaises(ValueError):
            to_packed("not an address")

    def test_from_packed_reads_an_ipv4_address(self):
        address = from_packed(b"\xc0\x00\x02\x01")
        self.assertIsInstance(address, IPv4Address)
        self.assertEqual(str(address), "192.0.2.1")

    def test_from_packed_reads_an_ipv6_address(self):
        address = from_packed(b"\x00" * 15 + b"\x01")
        self.assertIsInstance(address, IPv6Address)
        self.assertEqual(str(address), "::1")

    def test_from_packed_round_trips_an_address(self):
        self.assertEqual(from_packed(to_packed("2001:db8::1")), ip_address("2001:db8::1"))

    def test_from_packed_rejects_a_wrong_length(self):
        with self.assertRaises(ValueError):
            from_packed(b"\x00" * 5)

    def test_from_packed_rejects_an_unknown_type(self):
        with self.assertRaises(TypeError):
            from_packed("192.0.2.1")  # type: ignore[arg-type]


class TestVersion(unittest.TestCase):
    """Verify the version of an address."""

    def test_address_version_reports_four(self):
        self.assertEqual(address_version("192.0.2.1"), 4)

    def test_address_version_reports_six(self):
        self.assertEqual(address_version("2001:db8::1"), 6)

    def test_address_version_rejects_an_invalid_address(self):
        with self.assertRaises(ValueError):
            address_version("not an address")


class TestNetworkHosts(unittest.TestCase):
    """Verify the hosts of a network."""

    def test_network_hosts_skips_the_network_and_the_broadcast_address(self):
        hosts = network_hosts(ip_network("192.0.2.0/29"))
        expected = [f"192.0.2.{index}" for index in range(1, 7)]
        self.assertEqual([str(host) for host in hosts], expected)

    def test_network_hosts_of_a_network_of_two_addresses_holds_both(self):
        hosts = network_hosts(ip_network("192.0.2.0/31"))
        self.assertEqual([str(host) for host in hosts], ["192.0.2.0", "192.0.2.1"])

    def test_network_hosts_of_a_single_address_holds_that_address(self):
        hosts = network_hosts(ip_network("192.0.2.1/32"))
        self.assertEqual([str(host) for host in hosts], ["192.0.2.1"])

    def test_network_hosts_of_an_ipv6_network(self):
        hosts = network_hosts(ip_network("2001:db8::/126"))
        self.assertEqual(
            [str(host) for host in hosts],
            ["2001:db8::1", "2001:db8::2", "2001:db8::3"],
        )

    def test_network_hosts_stops_at_the_limit(self):
        hosts = network_hosts(ip_network("192.0.2.0/24"), limit=3)
        self.assertEqual([str(host) for host in hosts], ["192.0.2.1", "192.0.2.2", "192.0.2.3"])

    def test_network_hosts_of_an_empty_limit_holds_nothing(self):
        self.assertEqual(network_hosts(ip_network("192.0.2.0/24"), limit=0), [])

    def test_network_hosts_rejects_a_value_that_is_not_a_network(self):
        with self.assertRaises(TypeError):
            network_hosts("192.0.2.0/24")  # type: ignore[arg-type]

    def test_network_hosts_rejects_an_unknown_limit(self):
        with self.assertRaises(TypeError):
            network_hosts(ip_network("192.0.2.0/24"), limit="3")  # type: ignore[arg-type]

    def test_network_hosts_rejects_a_negative_limit(self):
        with self.assertRaises(ValueError):
            network_hosts(ip_network("192.0.2.0/24"), limit=-1)


class TestSubnets(unittest.TestCase):
    """Verify the subnets of a network."""

    def test_subnets_splits_the_network_by_one_bit(self):
        found = subnets(ip_network("192.0.2.0/24"))
        self.assertEqual([str(network) for network in found], ["192.0.2.0/25", "192.0.2.128/25"])

    def test_subnets_splits_the_network_by_two_bits(self):
        found = subnets(ip_network("192.0.2.0/24"), prefixlen_diff=2)
        self.assertEqual(len(found), 4)
        self.assertEqual(str(found[0]), "192.0.2.0/26")

    def test_subnets_accepts_a_new_prefix_length(self):
        found = subnets(ip_network("192.0.2.0/24"), new_prefix=26)
        self.assertEqual(len(found), 4)
        self.assertEqual(str(found[-1]), "192.0.2.192/26")

    def test_subnets_of_an_ipv6_network(self):
        found = subnets(ip_network("2001:db8::/32"))
        self.assertEqual(
            [str(network) for network in found],
            ["2001:db8::/33", "2001:db8:8000::/33"],
        )

    def test_subnets_rejects_both_prefix_arguments(self):
        with self.assertRaises(ValueError):
            subnets(ip_network("192.0.2.0/24"), prefixlen_diff=2, new_prefix=26)

    def test_subnets_rejects_a_value_that_is_not_a_network(self):
        with self.assertRaises(TypeError):
            subnets("192.0.2.0/24")  # type: ignore[arg-type]

    def test_subnets_rejects_a_prefix_length_that_is_not_an_integer(self):
        with self.assertRaises(TypeError):
            subnets(ip_network("192.0.2.0/24"), prefixlen_diff="2")  # type: ignore[arg-type]


class TestSummarizeAddresses(unittest.TestCase):
    """Verify the summary of a list of networks."""

    def test_summarize_addresses_merges_two_sibling_networks(self):
        found = summarize_addresses([ip_network("192.0.2.0/24"), ip_network("192.0.3.0/24")])
        self.assertEqual([str(network) for network in found], ["192.0.2.0/23"])

    def test_summarize_addresses_replaces_a_network_that_holds_another(self):
        found = summarize_addresses([ip_network("192.0.2.0/24"), ip_network("192.0.2.0/25")])
        self.assertEqual([str(network) for network in found], ["192.0.2.0/24"])

    def test_summarize_addresses_turns_an_address_into_a_single_host_network(self):
        found = summarize_addresses([ip_address("192.0.2.1")])
        self.assertEqual([str(network) for network in found], ["192.0.2.1/32"])

    def test_summarize_addresses_of_an_empty_list_holds_nothing(self):
        self.assertEqual(summarize_addresses([]), [])

    def test_summarize_addresses_rejects_mixed_versions(self):
        with self.assertRaises(ValueError):
            summarize_addresses([ip_network("192.0.2.0/24"), ip_network("2001:db8::/32")])

    def test_summarize_addresses_rejects_an_unknown_type(self):
        with self.assertRaises(TypeError):
            summarize_addresses(["192.0.2.0/24"])  # type: ignore[list-item]


class TestComparisons(unittest.TestCase):
    """Verify the comparisons between addresses and networks."""

    def test_network_overlaps_of_two_networks_of_the_same_range(self):
        self.assertTrue(network_overlaps(ip_network("192.0.2.0/24"), ip_network("192.0.2.128/25")))
        self.assertFalse(network_overlaps(ip_network("192.0.2.0/24"), ip_network("192.0.3.0/24")))

    def test_network_overlaps_of_two_versions_is_false(self):
        self.assertFalse(network_overlaps(ip_network("192.0.2.0/24"), ip_network("2001:db8::/32")))

    def test_network_overlaps_rejects_a_value_that_is_not_a_network(self):
        with self.assertRaises(TypeError):
            network_overlaps("192.0.2.0/24", ip_network("192.0.3.0/24"))  # type: ignore[arg-type]

    def test_address_within_finds_the_address(self):
        self.assertTrue(address_within(ip_address("192.0.2.1"), ip_network("192.0.2.0/24")))
        self.assertFalse(address_within(ip_address("192.0.3.1"), ip_network("192.0.2.0/24")))

    def test_address_within_of_two_versions_is_false(self):
        self.assertFalse(address_within(ip_address("2001:db8::1"), ip_network("192.0.2.0/24")))

    def test_address_within_rejects_a_value_that_is_not_an_address(self):
        with self.assertRaises(TypeError):
            address_within("192.0.2.1", ip_network("192.0.2.0/24"))  # type: ignore[arg-type]

    def test_common_prefix_length_of_one_address_is_the_whole_address(self):
        self.assertEqual(common_prefix_length([ip_address("192.0.2.1")]), 32)

    def test_common_prefix_length_of_neighbours(self):
        found = common_prefix_length([ip_address("192.0.2.1"), ip_address("192.0.2.2")])
        self.assertEqual(found, 30)

    def test_common_prefix_length_of_an_ipv6_pair(self):
        found = common_prefix_length([ip_address("2001:db8::1"), ip_address("2001:db8::2")])
        self.assertEqual(found, 126)

    def test_common_prefix_length_of_different_addresses(self):
        found = common_prefix_length([ip_address("10.0.0.1"), ip_address("11.0.0.1")])
        self.assertEqual(found, 7)

    def test_common_prefix_length_rejects_an_empty_list(self):
        with self.assertRaises(ValueError):
            common_prefix_length([])

    def test_common_prefix_length_rejects_mixed_versions(self):
        with self.assertRaises(ValueError):
            common_prefix_length([ip_address("192.0.2.1"), ip_address("2001:db8::1")])

    def test_common_prefix_length_rejects_a_value_that_is_not_an_address(self):
        with self.assertRaises(TypeError):
            common_prefix_length(["192.0.2.1"])  # type: ignore[list-item]


class TestNeighbours(unittest.TestCase):
    """Verify the neighbours of an address."""

    def test_next_address_steps_forward(self):
        self.assertEqual(str(next_address(ip_address("192.0.2.1"))), "192.0.2.2")

    def test_next_address_of_an_ipv6_address(self):
        self.assertEqual(str(next_address(ip_address("2001:db8::1"))), "2001:db8::2")

    def test_next_address_of_the_last_address_raises(self):
        with self.assertRaises(ValueError):
            next_address(ip_address(LAST_IPV4))
        with self.assertRaises(ValueError):
            next_address(ip_address(LAST_IPV6))

    def test_previous_address_steps_back(self):
        self.assertEqual(str(previous_address(ip_address("192.0.2.1"))), "192.0.2.0")

    def test_previous_address_of_an_ipv6_address(self):
        self.assertEqual(str(previous_address(ip_address("2001:db8::1"))), "2001:db8::")

    def test_previous_address_of_the_first_address_raises(self):
        with self.assertRaises(ValueError):
            previous_address(ip_address(FIRST_IPV4))
        with self.assertRaises(ValueError):
            previous_address(ip_address(FIRST_IPV6))

    def test_the_neighbours_reject_a_value_that_is_not_an_address(self):
        with self.assertRaises(TypeError):
            next_address("192.0.2.1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            previous_address("192.0.2.1")  # type: ignore[arg-type]


class TestSortAddresses(unittest.TestCase):
    """Verify the order of a list of addresses."""

    def test_sort_addresses_orders_by_version_and_value(self):
        found = sort_addresses(
            [ip_address("2001:db8::1"), ip_address("192.0.2.1"), ip_address("10.0.0.1")]
        )
        self.assertEqual(
            [str(address) for address in found],
            ["10.0.0.1", "192.0.2.1", "2001:db8::1"],
        )

    def test_sort_addresses_of_an_empty_list_holds_nothing(self):
        self.assertEqual(sort_addresses([]), [])

    def test_sort_addresses_rejects_a_value_that_is_not_an_address(self):
        with self.assertRaises(TypeError):
            sort_addresses(["192.0.2.1"])  # type: ignore[list-item]


class TestModuleContract(unittest.TestCase):
    """Verify the public interface of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(len(ipaddress_utils.__all__), len(set(ipaddress_utils.__all__)))
        self.assertEqual(ipaddress_utils.__all__, sorted(ipaddress_utils.__all__))
        for name in ipaddress_utils.__all__:
            self.assertTrue(hasattr(ipaddress_utils, name), name)

    def test_the_classes_are_the_classes_of_the_standard_library(self):
        import ipaddress

        self.assertIs(IPv4Address, ipaddress.IPv4Address)
        self.assertIs(IPv6Address, ipaddress.IPv6Address)
        self.assertIs(IPv4Network, ipaddress.IPv4Network)
        self.assertIs(IPv6Network, ipaddress.IPv6Network)
        self.assertIs(IPv4Interface, ipaddress.IPv4Interface)
        self.assertIs(IPv6Interface, ipaddress.IPv6Interface)

    def test_the_errors_are_the_errors_of_the_standard_library(self):
        import ipaddress

        self.assertIs(AddressValueError, ipaddress.AddressValueError)
        self.assertIs(NetmaskValueError, ipaddress.NetmaskValueError)


if __name__ == "__main__":
    unittest.main()
