import os

from untracked_config.no_proxy_ips import no_proxy_ip_addresses

# Ensure internal LAN addresses bypass the corporate proxy
# requests library on Windows does not support asterisk wildcards in NO_PROXY (e.g., 10.*) use CIDR 10.0.0.0/8 notation
# explicit IP addresses must be used
no_proxy = os.environ.get('NO_PROXY', '')
no_proxy_list = [ip.strip() for ip in no_proxy.split(',') if ip.strip()]
for ip in no_proxy_ip_addresses:
    if ip not in no_proxy_list:
        no_proxy_list.append(ip)
os.environ['NO_PROXY'] = ','.join(no_proxy_list)

try:
    import commonlog

    lg = commonlog.single_logger()
except ImportError:
    import logging

    lg = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG)
