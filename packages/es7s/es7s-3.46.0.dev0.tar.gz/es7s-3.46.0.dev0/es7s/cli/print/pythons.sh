#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------
# shellcheck disable=SC2119,SC2016
# shellcheck source=../../data/es7s-shell-commons.sh
__E7SL() { local c="$(realpath "$(dirname "$(readlink -f "$0")")")" ; local l=\
"es7s-shell-commons.sh" ; local p=( "$ES7S_SHELL_COMMONS" "$HOME/.es7s/data/$l"
"$c/../$l" ); while [[ ! $(type -t __es7s_com) =~ ^fu ]];do [[ -f "${p[0]}" ]]\
&& source "${p[0]}"; p=("${p[@]:1}"); [[ "${#p[@]}" -gt 0 ]] && continue; echo\
'ERROR: es7s/commons is missing (ES7S_SHELL_COMMONS)'; exit 57; done } ; __E7SL
# ------------------------------------------------------------- loader v.3B ---

_main() {
    declare paths=${PATH//:/ }
    local whichp=$(which python)
    local whichp3=$(which python3)
    local _r=$(_cs 39) _f=$(_cs) venv=$(_cs8 183)

    { for p in $(find $paths -maxdepth 1 -regex '.+/python[0-9.]*' -print | sort -V); do
          local cmd="$(basename $p)"
          local cmd_sorter="${cmd/python}"
          local cmd_prefix="  "
          local cmd_fmt=$'\x1b[32m'

          local lpath=$(which "$p") ppath=$(realpath "$p")
          [[ "$lpath" == "$ppath" ]] && lpath= || ppath="-> $ppath"
          local p_fmt=$(_cs 37)

          local v="$($p -VV 2>&1 | tr -d '\n')"
          local vtrim="$(sed <<<$v -Ee "s/[^0-9.]+([0-9.]+)(\.[0-9]+).*/\1\x1b[37m\2/")"
          local v_fmt=$'\x1b[33m'

          local apath="${lpath:-$ppath}"
          if [[ -n "$apath" ]] && [[ "$apath" == "$whichp" || "$apath" == "$whichp3" ]] ; then
              cmd_prefix=$'\x1b[92m> '
              v_fmt=$'\x1b[93m'
              p_fmt="$(_cs 97)"
          fi

          local path=$(printf "%s\t%s" "$lpath" "$ppath" | sed -Ee "s/\/?(venv|hatch)\/?/${venv}&${_r}${p_fmt}/g")

          printf "%s $cmd_fmt%s$_f%s$_r\t$v_fmt%8s$_f$p_fmt\t%s\t%s$_f\n" \
                 "${cmd_sorter:-0}$cmd" "$cmd_prefix$cmd" "$venv" "$vtrim" "$path"

    done } | sort -Vk1,1 | cut -f2- -d' ' | column -ts$'\t'
}

_main "$@"
