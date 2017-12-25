"""
	action.py
	Basic script driven action
"""



class Action(object):
	def ___init__(self, obj_name, action_name, start_frame=0):
		self._name = obj_name
		self._action_name = action_name
		self._start_frame = start_frame

