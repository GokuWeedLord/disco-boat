from disco.bot import Plugin, CommandLevels
from flask import request

class HttpPlugin( Plugin ):
	def load( self, ctx ):
		super( HttpPlugin, self ).load( ctx )

	@Plugin.route('/test')
	def test( self ):
		if request.values.get('t'):
			return request.values['t']

		return 'reeeeee'