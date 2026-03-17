# Untracked Config

This folder contains configuration files that are not tracked by version control because they contain
environment-specific settings (e.g., local hostnames, server addresses).

## How to use

1. Copy the template files to create the corresponding `.py` files:
    * Copy `development_node.py.template` to `development_node.py`
    * Copy `server_address.py.template` to `server_address.py`
    * Copy `no_proxy_ips.py.template` to `no_proxy_ips.py`
   * Copy `laminator_popup_links.py.template` to `laminator_popup_links.py`
2. Edit the new `.py` files with your local or environment-specific values.

## Files

### `development_node.py`

Used to determine if the application is running on a development system. You can add your local hostname to the
`__dev_node_names` list in this file.

### `server_address.py`

Contains the base URLs for various services used by the application, such as the defects list and operator data
services.

### `no_proxy_ips.py`

Contains a list of IP addresses that should bypass the corporate proxy. This is particularly important for the
`requests` library on Windows, which doesn't support wildcards in `NO_PROXY`.

### `laminator_popup_links.py`

Contains a dictionary of labels and URLs for the dropdown menu on the navigation bar. These links are dynamically
added to the navbar.
