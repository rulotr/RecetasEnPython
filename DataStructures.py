class Item:
	def __init__(self, name):
		self.name = name
	def __repr__(self):
		return 'Item({!r})'.format(self.name)
		
class User:
	def __init__(self,user_id):
		self.user_id = user_id

	def __repr__(self):
		return 'User({})'.format(self.user_id)