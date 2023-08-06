#!/bin/bash
#-------------------------------------------------------------------------------
# es7s/core
# (c) 2023 A. Shavykin <0.delameter@gmail.com>
#-------------------------------------------------------------------------------

main() {
    nohup google-chrome --disable-web-security --user-data-dir=/tmp/chrome_dev_test > /tmp/nohup.$(date +%s).out
}

[[ $# -lt 1 ]] || [[ $* =~ (--)?help ]] && exit
(main &)
--help
