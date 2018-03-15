from graphviz import Digraph
import string

class treeMaker:

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
		self.dot.render('tree'+str(count)+'.gv', view=True)

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

