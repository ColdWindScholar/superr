#!/bin/bash

banner() {
	echo "$clears"
	echo "------------------------------------------------------------"
	echo "$bo$st                     Bash plugin example                    $normal"
	echo "$it$st                          by SuperR                         $normal"
	echo "------------------------------------------------------------"
	echo ""
}

bd="$1"
ostools="$2"
rd="$3"
plugdir="$4"
plugin="$(basename "$4")"

bo=$(tput bold)
it=$(tput sitm)
st=$(tput smso)
normal=$(tput sgr0)
clears=$(tput clear)

banner
echo "Bash plugin example:"
echo ""
echo "Plugin Name = $plugin"
echo "Base Directory = $bd"
echo "OS Tools Directory = $ostools"
echo "ROM Directory = $rd"
echo "Plugin Directory = $plugdir"
echo ""
echo "*** Add more plugins to /kitchen/tools/plugins ***"
echo ""
echo ""

read -n 1 -p "Would you like to see the contents of your ROM directory?  y/n" reply
if [[ $reply = 'y' ]]; then
	echo ""
	cd "$rd"
	ls -l

	echo ""
	read -p "ENTER to continue"
fi

echo "$clears" # This prevents bad text formatting on the next screen after the plugin exits.
