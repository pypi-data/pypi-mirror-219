"""
    iautil
    ======
    Internet addresses transforming utilities
"""

from re import findall, match
from typing import Tuple, Union
from socket import gaierror, getaddrinfo, AF_INET, AF_INET6

def resolve_proto(host: str) -> Union[int, None]:
    """
        ### Match host string to one of supported protocol

        * [::1] -> AF_INET6
        * ::1 -> AF_INET6
        * 1.1.1.1 -> AF_INET
        * example.com -> -1
        * hgzx&*:;4zxzd -> ValueError('Failed to match proto for host', host)
    """

    IPv6 = r"^(\[[\d\D]{1,}\])$"
    IP6 = r"^([a-f0-9:]{1,})$"
    IPv4 = r"^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})$"
    TLD = r"^([A-z0-9._-]{1,})$"

    PATTERNS = [IPv6, IPv4, TLD, IP6]

    for pattern in PATTERNS:
        i = match(pattern, host)
        if i:
            if pattern is IPv6:
                return AF_INET6
            
            elif pattern is IP6:
                return AF_INET6

            elif pattern is IPv4:
                return AF_INET

            elif pattern is TLD:
                return -1

    raise ValueError('Failed to match proto for host', host)

def host_parse(host: str) -> Tuple[int, str, int]:
    """
        ### Parse "host:port" into Tuple[proto, host, port]

        * 1.1.1.1:8443 -> (AF_INET, '1.1.1.1', 8443)
        * [::1]:80 -> (AF_INET6, '[::1]', 80)
        * example.com:443 -> (-1, 'example.com', 443)
        * fkjlgh%szc:23 -> ValueError('Failed to parse host string', host)
    """
    
    IPv6_PORT = r"^(\[[\d\D]{1,}\]):([0-9]{1,5})$"
    IPv4_PORT = r"^([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}):([0-9]{1,5})$"
    TLD_PORT = r"^([A-z0-9._-]{1,}):([0-9]{1,5})$"

    PATTERNS = [IPv6_PORT, IPv4_PORT, TLD_PORT]
    for pattern in PATTERNS:
        i = findall(pattern, host)
        if i:
            if pattern is IPv6_PORT:
                proto = AF_INET6
            elif pattern is IPv4_PORT:
                proto = AF_INET
            else:
                proto = -1

            return proto, i[0][0], int(i[0][1])

    raise ValueError('Failed to parse host string', host)

def resolve_host(host: str) -> Tuple[Tuple[int, str]]:
    """
        ### Resolve domain name into Tuple[Tuple[proto, host], ...]

        * localhost -> ((AF_INET, "127.0.0.1"), (AF_INET6, "[::1]"), ...)
        * 127.0.0.1 -> ((AF_INET, "127.0.0.1"), ...)
        * [::1] -> ((AF_INET6, "[::1]]"), ...)
    """

    protocol = resolve_proto(host)

    if protocol == -1:
        try:
            host_addresses = getaddrinfo(host, 7)
        except gaierror:
            raise RuntimeError("Failed to resolve hostname:", host)
        return [(addr[0], addr[4][0]) for addr in host_addresses]
    return [[protocol, host]]
