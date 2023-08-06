#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------

_main() {
    local key="$1"
    [[ $key == ESC ]] && key=$'\x1b'
    printf %s "$key" | xsel --clipboard
    xdotool sleep 0.1 key --clearmodifiers ctrl+v
}

[[ $# -lt 1 ]] || [[ $* =~ (--)?help ]] && exit
_main "$@"
