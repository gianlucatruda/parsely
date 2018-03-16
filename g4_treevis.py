from graphviz import Digraph
import string

'''
This class is used to produce syntax trees.
'''
class syntaxTreeMaker:

	# class instantiation variables
	def __init__(self):
		self.edge_list = []
		self.dot = Digraph(comment="")
		# list of uppercase alphabet so nodes generator can use preferred naming
		self.alpha = []
		for s in string.ascii_uppercase:
			self.alpha.append(s)

	# tree generator using graphyviz library
	def generate(self, orig_tup, count):
		self.dot = Digraph(comment=str(orig_tup))
		self.treefy(orig_tup)
		self.dot.edges(self.edge_list)
		self.dot.format = "png"
		self.dot.render('syntax_tree'+str(count)+'.gv', view=True)

	# Funky recursive tree generating function
	def treefy(self, tup):
		p = tup[0]
		n_p = self.alpha.pop()
		lc = tup[1]
		rc = tup[2]
		self.dot.node(n_p, str(p))
		if type(lc) == tuple:
			call_tup = self.treefy(lc)
			lcn = call_tup[0]
			n_lcn = call_tup[1]
			self.dot.node(n_lcn,str(lcn))
			self.edge_list.append(n_p+n_lcn)
		else:
			n_lc = self.alpha.pop()
			self.dot.node(n_lc,str(lc))
			self.edge_list.append(n_p+n_lc)
		if type(rc) == tuple:
			call_tup = self.treefy(rc)
			rcn = call_tup[0]
			n_rcn = call_tup[1]
			self.dot.node(n_rcn,str(rcn))
			self.edge_list.append(n_p+n_rcn)
		else:
			n_rc = self.alpha.pop()
			self.dot.node(n_rc,str(rc))
			self.edge_list.append(n_p+n_rc)

		return (p, n_p)

'''
This class is used to produce parse trees.
'''
class parseTreeMaker:

	# class instantiation variables
	def __init__(self):
		self.edge_list = []
		self.dot = Digraph(comment="")
		# list of uppercase alphabet so nodes generator can use preferred naming
		self.alpha = []
		for s in string.ascii_uppercase:
			self.alpha.append(s)

	# tree generator using graphyviz library
	def generate(self, orig_tup, count):
		self.dot = Digraph(comment=str(orig_tup))
		self.treefy(orig_tup)
		self.dot.edges(self.edge_list)
		self.dot.format = "png"
		self.dot.render('parse_tree_'+str(count)+'.gv', view=True)

	# Funky recursive tree generating function
	def treefy(self, tup):
		p = str(tup)
		n_p = self.alpha.pop()
		op = tup[0]
		parse_type = 'factor'
		if op == 'times' or op == 'divide':
			parse_type = 'term'
		elif op == 'plus' or op == 'minus':
			parse_type = 'expression'
		n_op = self.alpha.pop()
		lc = tup[1]
		rc = tup[2]
		self.dot.node(n_p, parse_type)
		# Left child
		if type(lc) == tuple:
			call_tup = self.treefy(lc)
			lcn = call_tup[0]
			n_lcn = call_tup[1]
			self.dot.node(n_lcn,str(lcn))
			self.edge_list.append(n_p+n_lcn)
		else:
			n_lc = self.alpha.pop()
			n_lc_t = self.alpha.pop()
			self.dot.node(n_lc,"factor")
			self.dot.node(n_lc_t,str(lc))
			self.edge_list.append(n_p+n_lc)
			self.edge_list.append(n_lc+n_lc_t)
		# Central operation
		self.dot.node(n_op, str(op))
		self.edge_list.append(n_p+n_op)
		# Right child
		if type(rc) == tuple:
			call_tup = self.treefy(rc)
			rcn = call_tup[0]
			n_rcn = call_tup[1]
			self.dot.node(n_rcn,str(rcn))
			self.edge_list.append(n_p+n_rcn)
		else:
			n_rc = self.alpha.pop()
			n_rc_t = self.alpha.pop()
			self.dot.node(n_rc,"factor")
			self.dot.node(n_rc_t,str(rc))
			self.edge_list.append(n_p+n_rc)
			self.edge_list.append(n_rc+n_rc_t)
		return (parse_type, n_p)

