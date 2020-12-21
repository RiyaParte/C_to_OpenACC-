import ast_utilities
from pycparser import parse_file, c_ast, c_parser, c_generator
from pycparser.plyparser import Coord 
from re import sub 

gen = c_generator.CGenerator()
def dependency(file_name): 
	banres,forstmt = test_dependency(file_name)
	#print(banres)
	#print(forstmt)
	read = open(file_name,"r")
	write = open("dependency.txt","w")
	lineno = 0
	forno = 0
	f = 0 
	for i in range(len(banres)):
		for j in range(len(banres[i])):
			if not banres[i][j]:
				write.write("\nDependency exists\n")    
			else:
				write.write("\nNo Dependency exists\n")
			write.write(forstmt[i][j])			
	write.close()

def test_dependency(file_name): 
	comment_pre_processor(file_name)

	ast = parse_file(file_name, use_cpp=True) 
	#print(ast)
	# print(type(ast))
	remove_pre_processor(file_name, file_name) 
	banres = []
	forstmt = []
	# print(ast)
	func_count = 0
	for func in ast.ext:
			func_dict = ast_utilities.to_dict(func)
			#print(func_dict)
			if "body" in func_dict and "block_items" in func_dict["body"] and func_dict["_nodetype"] ==  "FuncDef":
				banres.append([])
				forstmt.append([])
				func_count += 1
				for stmt in func.body.block_items:
					stmt_dict = ast_utilities.to_dict(stmt)
					if stmt_dict["_nodetype"] == "For" or stmt_dict["_nodetype"] == "While" or stmt_dict["_nodetype"] == "DoWhile":
						banres[func_count -1].append(isdependent(stmt) ) 
						forstmt[func_count -1].append(gen.visit(stmt)) 
	return banres,forstmt					

 

def getleftvariable(dic,ast_key,lvar): 
	if dic["_nodetype"] == "ArrayRef":
		# print(dic["subscript"])
		lvar.append([dic["name"]["name"],gen.visit(ast_key.subscript)]) 
	elif dic["_nodetype"] == "ID":
		lvar.append([dic["name"],None]) 
	#print(lvar)
		

def getrightvariable(dic,ast_key,rvar): 
	if dic["_nodetype"] == "BinaryOp":
		getrightvariable(dic["left"],ast_key.left,rvar)
		getrightvariable(dic["right"],ast_key.right,rvar) 
	elif dic["_nodetype"] == "ArrayRef":
		rvar.append([dic["name"]["name"],gen.visit(ast_key.subscript)]) 
	elif dic["_nodetype"] == "ID":
		rvar.append([dic["name"],None]) 	
 	

def isdependent(ast_stmt): 
	# dic = ast_utilities.to_dict(ast_stmt)
	# val = dic['stmt']["block_items"]
	val1 = ast_stmt.stmt.block_items
	lvar,rvar = [],[]
	# print(val1[0].lvalue)
	for ast_key in val1:  
		dic = ast_utilities.to_dict(ast_key)
		if dic["_nodetype"] == "Assignment": 
			getleftvariable(dic["lvalue"],ast_key.lvalue,lvar)
			getrightvariable(dic["rvalue"],ast_key.rvalue,rvar)
		elif dic["_nodetype"] == "FuncCall" and ( dic["name"]["name"] == "printf" or dic["name"]["name"] == "scanf"):
			return False
	#print('lvar')
	#print(lvar)
	#print('rvar')
	#print(rvar)

	for leftitem in lvar:
		for rightitem in rvar:
			if leftitem[0] == rightitem[0] and leftitem[1] != rightitem[1]:
				return False 

	return True			




def comment_pre_processor(file_name):
	f = open(file_name, 'r')
	line_arr = []
	for line in f:
		line_arr.append(line)
	f.close()
	file = open(file_name,'w+')
	for line in line_arr:
		if "#" in line:
			file.write("//" + line)
		else:
			file.write(line)
	file.close()

def remove_pre_processor(file_name, write_file_name):
	f = open(file_name, 'r')
	line_arr = []
	for line in f:
		line_arr.append(line)
	f.close()
	file = open(file_name,'w+')
	for line in line_arr:
		if "#" in line:
			line = sub("//", "", line)
			file.write(line)
		else:
			file.write(line)
	file.close()
	f = open(write_file_name, 'r')
	line_arr = []
	for line in f:
		line_arr.append(line)
	f.close()
	file = open(write_file_name,'w+')
	for line in line_arr:
		if "#" in line:
			line = sub("//", "", line)
			file.write(line)
		else:
			file.write(line)
	file.close()


		
#print(lvar)
#print(rvar)
dependency("test1.c")
