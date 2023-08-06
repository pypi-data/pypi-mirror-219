#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2120

_log() {
    logger -p local7."${1:-debug}" -t "es7s/shocks[$$]"
}

_shocks.usage(){
    cat <<-EOF
	⚡ es7s/shocks
	  s[sh] s[ocks] proxy tunnel

	USAGE:
	  shocks PORT [USERNAME@]HOSTNAME [ARGS...]

	ARGUMENTS:
	  PORT        Local port binding for SOCKS proxy, e.g. "1080"
	  USERNAME    Remote server login
	  HOSTNAME    Remote server hostname/IP that will be used as a relay
	  ARGS        Extra arguments for (auto)ssh, e.g. "-i <PATH_TO_SSH_KEY>"

	ENVIRONMENT:
	  ES7S_SHOCKS_MONITOR
	              Non-empty string enables real-time monitoring of the connection
	              between local SOCKS proxy and the relay. The value should be
	              a name or a name mask of relay network interface the monitor
	              should connect to, e.g. "vpn0" or "eth*".

	DEPENDENCIES:
	  Requires installed 'ssh' and 'autossh' utilities.

	EXAMPLES:
	  shocks 1080 coolvps.com
	              Creates a port forwarding from localhost:1080 to the remote
	              host which tunnels the traffic through.

EOF
}

_shocks.main() {
    local PORT=${1:?Port required}
    local DEST=${2:?Destination required}

    local MODE_ARGS=(-N)  # no remote commands, background mode
    [[ -n $ES7S_SHOCKS_MONITOR ]] && \
        MODE_ARGS=(-t "/usr/bin/env ES7S_NO_AUTOSTART=true \$SHELL -c 'bmon -p $ES7S_SHOCKS_MONITOR --use-si'")

    autossh "$DEST" -v -D "$PORT" "${MODE_ARGS[@]}" "${@:3}" 2> >(_log)
}

[[ $* =~ (--)?help ]] && _shocks.usage && exit
_shocks.main "$@"
