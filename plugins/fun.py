import random

from disco.bot import Plugin

class FunPlugin( Plugin ):
	def load( self, ctx ):
		super( FunPlugin, self ).load( ctx )

	
	@Plugin.command( 'coin' )
	def coin( self, event ):
		"""
		Flip a coin
		"""
		event.msg.reply( random.choice( [ 'tails', 'heads' ] ) )

	@Plugin.command( 'roll', '[start:int] [end:int]' )
	def roll( self, event, start = 0, end = 100 ):
		pass