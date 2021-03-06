#! /bin/sh

STATE_OK=0
STATE_WARNING=1
STATE_CRITICAL=2
STATE_UNKNOWN=3
STATE_DEPENDENT=4

if test -x /usr/bin/printf; then
        ECHO=/usr/bin/printf
else
        ECHO=echo
fi

print_revision() {
        echo "$1 v$2 (nagios-plugins 1.4.16)"
        $ECHO "The nagios plugins come with ABSOLUTELY NO WARRANTY. You may redistribute\ncopies of the plugins under the terms of the GNU General Public License.\nFor more information about these matters, see the file named COPYING.\n" | sed -e 's/\n/ /g'
}

support() {
        $ECHO "Send email to nagios-users@lists.sourceforge.net if you have questions\nregarding use of this software. To submit patches or suggest improvements,\nsend email to nagiosplug-devel@lists.sourceforge.net.\nPlease include version information with all correspondence (when possible,\nuse output from the --version option of the plugin itself).\n" | sed -e 's/\n/ /g'
}

#
# check_range takes a value and a range string, returning successfully if an
# alert should be raised based on the range.
#
check_range() {
        local v range yes no err decimal start end cmp match
        v="$1"
        range="$2"

        # whether to raise an alert or not
        yes=0
        no=1
        err=2

        # regex to match a decimal number
        decimal="-?([0-9]+\.?[0-9]*|[0-9]*\.[0-9]+)"

        # compare numbers (including decimals), returning true/false
        cmp() { awk "BEGIN{ if ($1) exit(0); exit(1)}"; }

        # returns successfully if the string in the first argument matches the
        # regex in the second
        match() { echo "$1" | grep -E -q -- "$2"; }

        # make sure value is valid
        if ! match "$v" "^$decimal$"; then
                echo "${0##*/}: check_range: invalid value" >&2
                unset -f cmp match
                return "$err"
        fi

        # make sure range is valid
        if ! match "$range" "^@?(~|$decimal)(:($decimal)?)?$"; then
                echo "${0##*/}: check_range: invalid range" >&2
                unset -f cmp match
                return "$err"
        fi

        # check for leading @ char, which negates the range
        if match $range '^@'; then
                range=${range#@}
                yes=1
                no=0
        fi
}
