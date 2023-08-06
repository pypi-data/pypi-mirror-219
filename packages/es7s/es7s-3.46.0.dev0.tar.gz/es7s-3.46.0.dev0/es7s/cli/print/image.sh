#!/usr/bin/env bash
# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------
# Changes:
#   - disabled upscaling to the terminal width (downscale is still performed,
#     when neccessary)
#   - added directives for alpha channel removing
#   - made common format default
#   - removed colon/wrong/official format selection options
#   - added "--help" option handling
#   - fixed shellcheck warnings (in addition to disabling 2086)
# ------------------------------------------------------------------------------
# shellcheck disable=SC2086

# ORIGINAL LICENSE
#
# Image viewer for terminals that support true colors.
# Copyright (C) 2014  Egmont Koblinger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

declare -A ARGS
ARGS[w]=120

_usage() {
    local SELF=$(basename "${0%.*}")
    echo "Usage: $SELF [OPTIONS] FILE..."
    echo
    echo 'OPTIONS'
    echo '  -w WIDTH      Set maximum image width, default is 120.'
}

_main() {
    [[ $* =~ --help ]] && _usage && exit 0

    if ! _is_callable convert || ! _is_callable identify ; then
        echo 'ImageMagick is required' >&2
        exit 1
    fi
    # shellcheck disable=SC2214
    while getopts :w:-: OPT; do
        if [ "$OPT" = "-" ]; then
            OPT="${OPTARG%%=*}"
            OPTARG="${OPTARG#$OPT}"
            OPTARG="${OPTARG#=}"
        fi
        case "$OPT" in
            w|width) ARGS[w]=$((OPTARG)) ;;
              ??*|?) echo "Illegal option -${OPTARG:--$OPT}"
                     _usage
                     exit 1 ;;
        esac
    done
    shift $((OPTIND-1))

    # This is so that "upper" is still visible after exiting the while loop.
    shopt -s lastpipe

    local -a upper lower
    upper=()
    lower=()

    _process() {
        local i col

        convert -thumbnail ${outw}x -alpha remove -background \#808080 -define txt:compliance=SVG "$file"[0] txt:- |
            while IFS=',:() ' read -r col row _ red green blue rest; do
                if [ "$col" = "#" ]; then
                    continue
                fi

                if [ $((row % 2)) = 0 ]; then
                    upper[$col]="$red;$green;$blue"
                else
                    lower[$col]="$red;$green;$blue"
                fi

                # After reading every second image row, print them out.
                if [ $((row % 2)) = 1 ] && [ $col = $((outw - 1)) ]; then
                    i=0
                    while [ $i -lt $outw ]; do
                        echo -ne "\\e[38;2;${upper[$i]};48;2;${lower[$i]}m▀"
                        i=$((i + 1))
                    done
                    # \e[K is useful when you resize the terminal while this script is still running.
                    echo -e "\\e[0m\e[K"
                    upper=()
                fi
            done

        # Print the last half line, if required.
        if [ "${upper[0]}" != "" ]; then
            i=0
            while [ $i -lt $outw ]; do
                echo -ne "\\e[38;2;${upper[$i]}m▀"
                i=$((i + 1))
            done
            echo -e "\\e[0m\e[K"
        fi

    }

    for file in "$@" ; do
        _print_filename "$file"
        [[ -d "$file" ]] && _print_failure "Not file" && continue
        [[ ! -f "$file" ]] && _print_failure "Not found" && continue

        local imgsize
        if ! imgsize=$(identify -format "%wx%h\n" "$file"[0] 2>/dev/null) ; then
            _print_failure "Not image" && continue
        fi
        [[ -z "$imgsize" ]] && _print_failure "Not image" && continue

        local firstsize=$(head -1 <<<"$imgsize" | tr -d '\n')
        local firstw=${firstsize%%x*}
        local firsth=${firstsize##*x}
        _print_status "$file" $firstw $firsth && echo

        local imgw=$(cut <<<$firstsize -f1 -dx)
        local outw=$(tput cols)
        [[ $outw -gt $imgw ]] && outw=$imgw
        [[ $outw -gt ${ARGS[w]} ]] && outw=${ARGS[w]}

        if ! _process "$file"[0] ; then
            continue
        fi
    done
}
_print_failure() { printf "%10.10s \n" "$1:" ; }
_print_filename() { _print_status "$1"$'\r' ; }
_print_status() {
    local file="${1:?}" imgw=${2:-} imgh=${3:-}
    local xmk=
    [[ -n $imgw ]] && [[ -n $imgh ]] && xmk=x
    printf "\x1b[K%10s %s" "$imgw$xmk$imgh" "$file" >&2
}
_is_callable() { command -v $1 &>/dev/null ; }

_main "$@"
