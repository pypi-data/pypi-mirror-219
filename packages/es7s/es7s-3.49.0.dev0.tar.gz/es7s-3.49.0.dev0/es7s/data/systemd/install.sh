#!/bin/bash

__=$'\e[%sm' _f=$'\e[0m'

__main() {
    local srcpath="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
    local SERVICES=$(echo $srcpath/*.service | sort)
    printf "Found $__%s$_f service(s)\n" "1" "$( wc -w <<<"$SERVICES" )"
    for svcpath in ${SERVICES[*]} ; do
        local svcfile="$(basename "$svcpath")"
        local svcname="${svcfile#*.}"
        local msg="$(printf "Install $__%s$_f?" "32;1" "$svcname")"
        __prompt "$msg" || continue
        __install_service "$svcname" "$svcpath"
    done
    echo
}

__prompt() {
    local msg=$'\n'"${1:-} (y/n): "
    while true ; do
        read -n1 -r -p "$msg" yn
        case $yn in
            [Yy]*) return 0 ;;
            [Nn]*) return 1 ;;
            [Qq]*) echo && exit 1 ;;
                *) continue ;;
        esac
    done
}

__install_service() {
    local svcname="${1:?Required}" svcpath="${2:?Required}"
    echo
    printf "Installing $__%s$_f\n" "1" "$svcname"

    set -e
    __call sudo cp "$svcpath" "/etc/systemd/system/$svcname"
    __call sudo sed "/etc/systemd/system/$svcname" -i -Ee "s/%UID/$(id -u)/g; s/%USER/$(id -un)/g"
    __call sudo systemctl enable "$svcname"
    __call sudo systemctl daemon-reload
    __call sudo systemctl restart "$svcname"
    __call sudo systemctl status "$svcname" --lines 5 --no-pager --quiet
    set +e
}

__call() {
    printf "$__>$_f $__%s$_f\n" "34;1" "34;2" "$*"
    "$@"
}

__main "$@"
