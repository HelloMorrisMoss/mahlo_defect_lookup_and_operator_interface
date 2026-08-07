import logging
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
    from commonlog.logger_setup import set_up_logger

    # Best Practice: Configure the root logger so all modules benefit from the same setup
    # suppress_prints=True prevents commonlog from redirecting stdout/stderr to devnull
    lg = set_up_logger(
        lg=logging.getLogger(),
        file_log=".\mahlo_dash_app.log",
        suppress_prints=True
    )
    lg.info("Logging initialized on root logger with commonlog.")
except ImportError:
    # Fallback to basicConfig if commonlog is not available
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(".\mahlo_dash_app.log")
        ]
    )
    lg = logging.getLogger()
    lg.debug("Logging initialized on root logger with basicConfig.")
