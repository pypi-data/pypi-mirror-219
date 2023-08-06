

import nettoolkit as nt




def get_conditions(jinja_flie):
	"""get all conditional statements from jinja file

	Args:
		jinja_flie (str): jinja template file

	Returns:
		dict: dictionary with list of jinja variables, conditions, and loops.
	"""	
	d = {'conditions':set(), 'loops':set(), 'variables': set() }
	with open(jinja_flie, 'r') as f:
		lns = f.readlines()
	for ln in lns:
		if ln.strip().startswith("{% for "):
			d['loops'].add(ln)
		elif ln.strip().startswith("{% if") or ln.strip().startswith("{% elif"):
			d['conditions'].add(ln)
		elif ln.strip().startswith("{% set "):
			d['variables'].add(ln)
	return d

def get_variables(jinja_flie):
	"""get all jinja variables defined in jinja file

	Args:
		jinja_flie (str): jinja template file

	Returns:
		set: set of jinja variables
	"""	
	conds = set()
	with open(jinja_flie, 'r') as f:
		lns = f.readlines()
	for ln in lns:
		starts, ends = [], []
		for i in range(20):
			if i == 0: s,e = 0,0
			start = nt.STR.find_multi(ln, '{{', start=s, count=None, index=True, beginwith=False)
			end   = nt.STR.find_multi(ln, '}}', start=e, count=None, index=True, beginwith=False)
			if start == -1: break
			starts.append(start)
			ends.append(end)
			s = start+2
			e = end+2

		if starts == []: continue
		for s, e in zip(starts, ends):
			cond = ln[s:e+2]
			conds.add(cond)
	return conds

# # -----------------------------------------------------------------------------------------
