import os
import logging

from disco.client import Client, ClientConfig
from disco.bot import Bot, BotConfig
from disco.util.token import is_valid_token
from disco.types.message import MessageTable
from disco.util.logging import setup_logging

import argparse

CONFIG_FILE = "config.yaml"

def patch_MessageTable():
	def new_compile_one( self, cols ):
		data = self.sep.lstrip()

		for idx, col in enumerate(cols):
			padding = ' ' * (self.size_index[idx] - len(col))
			data += col + padding + self.sep


	MessageTable.compile_one = new_compile_one



def run_bot( ):
	from gevent import monkey
	monkey.patch_all( )

	#patch_MessageTable()

	parser = argparse.ArgumentParser( )
	parser.add_argument( '--token', help="discord api auth token", default=None )
	parser.add_argument( '--log-level', help='log level', default="INFO" )

	if not os.path.exists( CONFIG_FILE ):
		print( "%s missing, pls fix" % CONFIG_FILE )
		exit( )

	config = ClientConfig.from_file( CONFIG_FILE )

	args = parser.parse_args( )

	if args.log_level:
		setup_logging( level=getattr( logging, args.log_level.upper() ) )

	if args.token is not None:
		config.token = args.token

	if not is_valid_token( config.token ):
		print( "the token '%s' isn't valid" % config.token )
		exit( )

	client = Client( config )
	
	bot_config = BotConfig( config.bot )

	# get plugin files
	# todo: support multilevel nested plugins
	_, _, filenames = next( os.walk( "plugins" ), ( None, None, [ ] ) )
	filenames.remove( "__init__.py" )
	
	# convert plugins from ayylmao.py to plugins.ayylmao
	filenames = [ "plugins.%s" % os.path.splitext( p )[ 0 ] for p in filenames ]

	# remove disabled plugins from plugin array
	filenames = [ p for p in filenames if p not in config.disabled_plugins ]

	bot_config.plugins = filenames

	if len( bot_config.plugins ) > 0:
		print( "discovered plugins:" )

		for p in bot_config.plugins:
			print( " - %s" % p )
	else:
		print( "no plugins found" )

	bot = Bot( client, bot_config )

	bot.run_forever( )

run_bot( )
