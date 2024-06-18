#!/usr/bin/env python3

# Constant variables. DO NOT EDIT unless you know what you are doing
import os, sys

def main(j, plugin):
	plugdir = os.path.join(j.tools, 'plugins', plugin)
	color = j.color
# END Constant variables

# START Script here
	def banner():
		j.clears()
		print()
		print('-'.center(j.tsize, '-'))
		print(j.intro1 + "Plugin for SuperR's Kitchen".center(j.tsize) + color['n'])
		print(j.intro2 + 'by SuperR'.center(j.tsize) + color['n'])
		print('-'.center(j.tsize, '-'))
		print()

	banner()
	j.kprint('Python plugin example:\n')
	j.kprint('Plugin Name = ' + plugin, 'g')
	j.kprint('Base Directory = ' + j.bd, 'g')
	j.kprint('OS Tools Directory = ' + j.tools, 'g')
	j.kprint('ROM Directory = ' + j.rd, 'g')
	j.kprint('Plugin Directory = ' + plugdir + '\n', 'g')
	j.kprint('***' + j.lang['plug_example_text'] + '/kitchen/tools/plugins ***\n\n', 'b')

	print('Would you like to see the contents of your ROM directory?  y/n')

	if j.getChar() == 'y':
		with j.cd(j.rd):
			j.kprint('\n'.join(j.findf('*')) + '\n', 'y')

		input(j.lang['enter_continue'])

	return
