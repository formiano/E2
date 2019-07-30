from enigma import eActionMap

from Tools.KeyBindings import queryKeyBinding


class ActionMap:
	def __init__(self, contexts=[], actions={}, prio=0):
		self.contexts = contexts
		self.actions = actions
		self.prio = prio
		self.p = eActionMap.getInstance()
		self.bound = False
		self.exec_active = False
		self.enabled = True

	def setEnabled(self, enabled):
		self.enabled = enabled
		self.checkBind()

	def doBind(self):
		if not self.bound:
			for ctx in self.contexts:
				self.p.bindAction(ctx, self.prio, self.action)
			self.bound = True

	def doUnbind(self):
		if self.bound:
			for ctx in self.contexts:
				self.p.unbindAction(ctx, self.action)
			self.bound = False

	def checkBind(self):
		if self.exec_active and self.enabled:
			self.doBind()
		else:
			self.doUnbind()

	def execBegin(self):
		self.exec_active = True
		self.checkBind()

	def execEnd(self):
		self.exec_active = False
		self.checkBind()

	def action(self, context, action):
		if action in self.actions:
			print "[ActionMap] Keymap '%s' -> Action = '%s'" % (context, action)
			res = self.actions[action]()
			if res is not None:
				return res
			return 1
		else:
			print "[ActionMap] Keymap '%s' -> Unknown action '%s'! (Typo in keymap?)" % (context, action)
			return 0

	def destroy(self):
		pass

class NumberActionMap(ActionMap):
	def action(self, contexts, action):
		if action in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9") and action in self.actions:
			res = self.actions[action](int(action))
			if res is not None:
				return res
			return 1
		else:
			return ActionMap.action(self, contexts, action)

class HelpableActionMap(ActionMap):
	def __init__(self, parent, contexts, actions={}, prio=0, description=None):
		if not hasattr(contexts, '__iter__'):
			contexts = [contexts]
		self.description = description
		adict = {}
		for context in contexts:
			alist = []
			for (action, funchelp) in actions.iteritems():
				if isinstance(funchelp, tuple):
					if queryKeyBinding(context, action):
						alist.append((action, funchelp[1]))
					adict[action] = funchelp[0]
				else:
					if queryKeyBinding(context, action):
						alist.append((action, None))
					adict[action] = funchelp
			parent.helpList.append((self, context, alist))
		ActionMap.__init__(self, contexts, adict, prio)


class HelpableNumberActionMap(NumberActionMap, HelpableActionMap):
	def __init__(self, parent, contexts, actions=None, prio=0, description=None):
		NumberActionMap.__init__(self, [], {})
		HelpableActionMap.__init__(self, parent, contexts, actions, prio, description)
