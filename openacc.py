import ast_utilities
from pycparser import parse_file, c_ast, c_parser, c_generator
from pycparser.plyparser import Coord 
from re import sub
import dependency_test
gen = c_generator.CGenerator()

def convert(file_name):
	
	banres,forstmt = dependency_test.test_dependency(file_name) 
	dependency_test.comment_pre_processor(file_name)
	##print(banres)
	##print(forstmt)
	ast = parse_file(file_name, use_cpp=True)
	##print(ast)
	dependency_test.remove_pre_processor(file_name,file_name)

	func_count = 0
	all_for_list=[]
	all_while_list=[]

	for func in ast.ext:
		func_dict = ast_utilities.to_dict(func)
		##print(func_dict)
		if "body" in func_dict and "block_items" in func_dict["body"] and func_dict["_nodetype"] ==  "FuncDef":
			func_count += 1
			func_for_loop_var_list, func_while_loop_var_list, func_for_loop_line_number_arr, func_while_loop_line_number_arr  = convert_function_handler(func, func_dict,func_count,banres,file_name)
			all_for_list.append(func_for_loop_var_list)
			#print(all_for_list)
			all_while_list.append(func_while_loop_var_list)
	#data 
	data_directive('mid.c',all_for_list,all_while_list)

	return 0		
	


def convert_function_handler(func, func_dict,func_count,banres,file_name):
	func_for_loop_var_list = find_all_for_variable_list(func, func_dict)
	func_while_loop_var_list = find_all_while_variable_list(func, func_dict)

	#print(func_for_loop_var_list)
	#print(func_while_loop_var_list)
	
	func_for_loop_line_number_arr = find_func_for_loop_line_number_arr(func)
	func_while_loop_line_number_arr = find_func_while_loop_line_number_arr(func)

	##print(func_for_loop_line_number_arr)
	func_for_loop_line_number_arr = func_for_loop_line_number_arr[:-1]
	func_for_loop_line_number_arr = set(func_for_loop_line_number_arr)  
	func_for_loop_line_number_arr = list(func_for_loop_line_number_arr)

	current_for_loop_number = 0
	current_while_loop_number = 0
	loop_count = 0

	for stmt in func.body.block_items:
		stmt_dict = ast_utilities.to_dict(stmt)
		
		if stmt_dict["_nodetype"] == "For":
			loop_count += 1
			for_loop_handle(file_name,banres, func_for_loop_line_number_arr,func_count)
			


		if stmt_dict["_nodetype"] == "While" or stmt_dict["_nodetype"] == "DoWhile" :
			loop_count += 1
			while_loop_handle(file_name,banres, func_while_loop_line_number_arr,func_count)
			



	return func_for_loop_var_list, func_while_loop_var_list, func_for_loop_line_number_arr, func_while_loop_line_number_arr



def for_loop_handle(file_name,banres, func_for_loop_line_number_arr,func_count):
	#print(func_for_loop_line_number_arr)
	#print(banres)

	func_for_loop_line_number_arr.sort()
	d={}

	for i in range(len(func_for_loop_line_number_arr)):
		d[func_for_loop_line_number_arr[i]]= banres[func_count-1][i]

	#print(d)

	f=open(file_name,'r')
	stmt = "#pragma acc parallel loop"
	lines = f.readlines()
	f2=open('mid.c','w+')
	
	for i in range(len(lines)):
		if ((i+1 in func_for_loop_line_number_arr) and d[i+1]==True):
			##print(i+1)
			##print(d[i+1])
			f2.write(stmt+'\n')
			f2.write(lines[i])
			
		else:
			f2.write(lines[i])

	return 0



def while_loop_handle(file_name,banres, func_while_loop_line_number_arr,func_count):
	#print(func_while_loop_line_number_arr)
	#print(banres)

	f=open(file_name,'r')
	stmt = "#pragma acc parallel loop"
	lines = f.readlines()
	f2=open('mid.c','w+')

	##print(lines)
	while_line_no=[]
	
	for i in range(len(lines)):
		if (i+1) in func_while_loop_line_number_arr  and lines[i].startswith("while"):
			while_line_no.append(i+1)

	d={}

	for i in range(len(while_line_no)):
		d[while_line_no[i]]= banres[func_count-1][i]

	for i in range(len(lines)):
		if ((i+1 in while_line_no) and d[i+1]==True):
			f2.write(stmt+'\n')
			f2.write(lines[i])
			
		else:
			f2.write(lines[i])
	return 0


def data_directive(file_name,all_for_list,all_while_list):
	for_arr=[]
	while_arr=[]
	for i in range (len(all_for_list)):
		for_arr.append(all_for_list[i][2])

	#print(for_arr)
	print(all_while_list)
	while_arr=[]
	for i in range (len(all_while_list)):
		while_arr.append(all_while_list[i][2])

	print(while_arr)


	banres,forstmt = dependency_test.test_dependency(file_name)
	#print(banres)
	#print(forstmt)


	f=open(file_name,'r')
	stmt = "#pragma acc data"
	lines = f.readlines()
	f2=open('final.c','w+')

	dependency_test.comment_pre_processor(file_name)
	ast = parse_file(file_name, use_cpp=True)
	dependency_test.remove_pre_processor(file_name,file_name)

	func_line_number_arr = find_func_line_number_arr(ast)

	final_list=[]
	for func in ast.ext:
		list1=[]
		func_dict = ast_utilities.to_dict(func)
		if "body" in func_dict and "block_items" in func_dict["body"] and func_dict["_nodetype"] ==  "FuncDef":
			for stmt_line in func.body.block_items:
				stmt_dict = ast_utilities.to_dict(stmt_line)
				#print(stmt_dict)
				if stmt_dict["_nodetype"] == "For" or stmt_dict["_nodetype"] == "While" or stmt_dict["_nodetype"] == "DoWhile":
					#print(len(stmt_dict['stmt']['block_items']))
					
					for i in range(len(stmt_dict['stmt']['block_items'])):
						#print(stmt_dict['stmt']['block_items'][0])
						d=stmt_dict['stmt']['block_items'][0]

						if 'rvalue' in d.keys() :
							d1=d['rvalue']
							#print(d1)
							if d1['_nodetype'] == 'BinaryOp':
								if d1['right']['_nodetype']=='ArrayRef':
									#print(stmt_line)
									list1.append('True')
									var1 = stmt_line
									
									#print(var1)
								else:
									list1.append('False')
									break
							elif d1['_nodetype'] == 'ArrayRef':
								#print(stmt_line)
								list1.append('True')
								var1 = stmt_line
								

								#print(var1)
							else:
								list1.append('False')
								break
						else:
							continue


		final_list.append(list1)

	print(final_list)




	
	if len(func_line_number_arr)>1:


		for j in range (len(final_list)) :

			if len(final_list[j])!=0 and ('True') in final_list[j]: 
				#print(len(final_list[j]))
				pragma_no=0
				for i in range(len(final_list[j])):
					if final_list[j][i]=='True':
						pragma_no=i
					else:
						continue

				"""
				#print(pragma_no)
				k=0
				t=0
				for i in range(len(lines)):
					#print(k)
					if lines[i].startswith('#pragma') and k==pragma_no:
						t=1
						f2.write(stmt+'\n')
						f2.write('{'+'\n')
						f2.write(lines[i])
						continue
					elif lines[i].startswith('#pragma') and k != pragma_no:		
						k+=1
					f2.write(lines[i])

				if t==1:
					f2.write('}'+'\n')

				"""
		n_list=[]
		#print(func_line_number_arr)
		

		for i in range(len(func_line_number_arr)-1):
			n_list.append([int(func_line_number_arr[i]),int(func_line_number_arr[i+1])])

		#print(n_list)
		flag =0
		#print(n_list[len(n_list)-1][1]-2)
		for i in range(len(lines)):
			if i < (n_list[0][0]-1):
				f2.write(lines[i])

			elif i> (n_list[len(n_list)-1][1]-2):
				
				f2.write(lines[i])

			elif i>(n_list[0][0]-1) and i<(n_list[len(n_list)-1][1]-2) and flag==0:
				flag=1
				for ele in n_list:
					t,k=0,0
					flag=1
					for i in range (ele[0]-1, ele[1]-1):
						if lines[i].startswith("#pragma") and t==0 and k==pragma_no :
							t=1
							f2.write(stmt+'\n')
							f2.write('{'+'\n')
							f2.write(lines[i])
							continue
						elif lines[i].startswith('#pragma') and k != pragma_no:		
							k+=1
						
						f2.write(lines[i])
					if t==1:
						f2.write('}'+'\n')





		
		"""
		n_list=[]
		#print(func_line_number_arr)
		

		for i in range(len(func_line_number_arr)-1):
			n_list.append([int(func_line_number_arr[i]),int(func_line_number_arr[i+1])])

		#print(n_list)
		flag =0
		#print(n_list[len(n_list)-1][1]-2)
		for i in range(len(lines)):
			if i < (n_list[0][0]-1):
				f2.write(lines[i])

			elif i> (n_list[len(n_list)-1][1]-2):
				
				f2.write(lines[i])

			elif i>(n_list[0][0]-1) and i<(n_list[len(n_list)-1][1]-2) and flag==0:
				flag=1
				for ele in n_list:
					t=0
					flag=1
					for i in range (ele[0]-1, ele[1]-1):
						if lines[i].startswith("#pragma") and t==0:
							t=1
							f2.write(stmt+'\n')
							f2.write('{'+'\n')
							f2.write(lines[i])
							continue
						
						f2.write(lines[i])
					if t==1:
						f2.write('}'+'\n')"""

	else :
		pragma_no=0
		for i in range(len(final_list[0])):
			if final_list[0][i]=='True':
				pragma_no=i
				break
			else:
				continue
		#print(pragma_no)
		k=0
		t=0
		for i in range(len(lines)):
			#print(k)
			if lines[i].startswith('#pragma') and k==pragma_no:
				t=1
				f2.write(stmt+'\n')
				f2.write('{'+'\n')
				f2.write(lines[i])
				continue
			elif lines[i].startswith('#pragma') and k != pragma_no:		
				k+=1
			f2.write(lines[i])

		if t==1:
			f2.write('}'+'\n')
			






	return 0





def find_all_for_variable_list(func, func_dict):
	# all_for_variable_arr_list Structure:- List of array in for variable in given function
	# [{"variable_name": "a", type: "int"}]	 
	argument_variable,argument_array_variable = find_function_args_variable_type(func, func_dict) 
	all_function_variable,all_function_array_variable = {},{}
	# find_function_all_variable_type(func_dict,all_function_variable,all_function_array_variable,all_array_dim)
	# all_function_variable = {**argument_variable, **function_variable}
	all_for_variable = set()
	for_variable_array = {}
	for_variable = {} 
	all_array_dim = {}
	for blocks in func_dict["body"]["block_items"]: 
		find_function_all_variable_type(func_dict,all_function_variable,all_function_array_variable,all_array_dim)
		if blocks["_nodetype"] == "For":
			if "stmt" in blocks and "block_items" in blocks["stmt"]:
				all_for_variable = find_function_for_variable(blocks["stmt"]["block_items"],all_for_variable)
	all_function_variable = {**argument_variable, **all_function_variable}	
	all_function_array_variable = {**argument_array_variable, **all_function_array_variable}	
	for i in all_for_variable:
		if i in all_function_array_variable:
			for_variable_array[i] = all_function_array_variable[i] 
		elif i in all_function_variable:
			for_variable[i] = all_function_variable[i]  
	return for_variable,for_variable_array,all_array_dim	

def find_all_while_variable_list(func, func_dict):
	# all_for_variable_arr_list Structure:- List of array in for variable in given function
	# [{"variable_name": "a", type: "int"}]	 
	argument_variable,argument_array_variable = find_function_args_variable_type(func, func_dict) 
	all_function_variable,all_function_array_variable = {},{}
	# find_function_all_variable_type(func_dict,all_function_variable,all_function_array_variable,all_array_dim)
	# all_function_variable = {**argument_variable, **function_variable}
	all_for_variable = set()
	for_variable_array = {}
	for_variable = {} 
	all_array_dim = {}
	for blocks in func_dict["body"]["block_items"]: 
		find_function_all_variable_type(func_dict,all_function_variable,all_function_array_variable,all_array_dim)
		if blocks["_nodetype"] == "While" or blocks["_nodetype"] == "DoWhile":
			if "stmt" in blocks and "block_items" in blocks["stmt"]:
				all_for_variable = find_function_for_variable(blocks["stmt"]["block_items"],all_for_variable)
	all_function_variable = {**argument_variable, **all_function_variable}	
	all_function_array_variable = {**argument_array_variable, **all_function_array_variable}	
	for i in all_for_variable:
		if i in all_function_array_variable:
			for_variable_array[i] = all_function_array_variable[i] 
		elif i in all_function_variable:
			for_variable[i] = all_function_variable[i]  
	return for_variable,for_variable_array,all_array_dim


def find_func_for_loop_line_number_arr(func):
	func_for_loop_line_number_arr = []
	flag = 0
	for stmt in func.body.block_items:
		stmt_dict = ast_utilities.to_dict(stmt)
		if flag == 1:
			func_for_loop_line_number_arr.append(int(str(stmt.coord).split(":")[1]))
			flag = 0
		if stmt_dict["_nodetype"] == "For":
			func_for_loop_line_number_arr.append(int(str(stmt.coord).split(":")[1]))
			flag = 1
	return func_for_loop_line_number_arr

def find_func_while_loop_line_number_arr(func):
	func_while_loop_line_number_arr = []
	flag = 0
	for stmt in func.body.block_items:
		stmt_dict = ast_utilities.to_dict(stmt)
		if flag == 1:
			func_while_loop_line_number_arr.append(int(str(stmt.coord).split(":")[1]))
			flag = 0
		if stmt_dict["_nodetype"] == "While" or stmt_dict["_nodetype"] == "DoWhile":
			func_while_loop_line_number_arr.append(int(str(stmt.coord).split(":")[1]))
			flag = 1
	return func_while_loop_line_number_arr

def find_function_args_variable_type(func, func_dict):
	var,array_var = {} ,{}
	if func_dict["decl"]["type"]["args"] : 
		for arg in func_dict["decl"]["type"]["args"]["params"]:
			if arg["type"]["_nodetype"] == "ArrayDecl":  
				curr =  arg["type"]
				while curr["_nodetype"] != "IdentifierType":
					curr = curr["type"] 
				array_var[arg["name"]] = curr["names"][0] 
			elif arg["type"]["_nodetype"] == "Decl" :  
				var[arg["name"]] = arg["type"]["type"]["names"][0] 
			 	
	return var,array_var

def find_function_all_variable_type(func_dict,all_variable,all_array,all_array_dim):
	# check if element is list
	if isinstance(func_dict,list):
		# iterate every element and recall function
		for i in func_dict: 
			find_function_all_variable_type(i,all_variable,all_array,all_array_dim) 
	# check if element is dictionary
	if isinstance(func_dict,dict):		
		for key in func_dict :  
			# check if dictionary is present in value
			if isinstance(func_dict[key], list):
				find_function_all_variable_type(func_dict[key],all_variable,all_array,all_array_dim)
			if isinstance(func_dict[key],dict): 
				find_function_all_variable_type(func_dict[key],all_variable,all_array,all_array_dim) # Recall fucntion and value i.e dictionary
			if key == "_nodetype" and func_dict[key] == "Decl": 
				if func_dict["type"]["_nodetype"]=="ArrayDecl":
					curr = func_dict["type"] 
					while "type" in curr: 
						curr = curr["type"]
					all_array[func_dict["name"]] = curr["names"][0] 

					curr = func_dict["type"]
					subscripts = []
					if curr["dim"]:
						while "dim" in curr:
							if "name" in curr["dim"]:
								subscripts.append(curr["dim"]["name"])
								curr = curr["type"]
							elif "type" in curr["dim"]:
								subscripts.append(curr["dim"]["value"])
								curr = curr["type"]
						all_array_dim[func_dict["name"]] = subscripts 


				curr = func_dict
				while "names" not in curr: #loop till type is over
					curr = curr["type"] 
				all_variable[func_dict["name"]] = curr["names"][0] 

def find_function_for_variable(func_dict,var ):
	# check if element is list 
	if isinstance(func_dict,list):
		# iterate every element and recall function
		for i in func_dict: 
			find_function_for_variable(i,var ) 
	# check if element is dictionary		
	if isinstance(func_dict,dict):		
		for key in func_dict : 

			# check if dictionary is present in value
			if isinstance(func_dict[key], list):
				find_function_for_variable(func_dict[key], var )

			if isinstance(func_dict[key],dict): 
				find_function_for_variable(func_dict[key],var ) # Recall fucntion and value i.e dictionary

			if key == "name" and not isinstance(func_dict[key],dict) and not isinstance(func_dict,list):
				var.add(func_dict[key])
	return var

#file_name = open("C:/Users/parte/Desktop/temp/examples/test.c",'r')
#f1 = open("C:/Users/parte/Desktop/temp/examples/result.c","a")



def find_func_line_number_arr(ast):
	func_line_number_arr = []
	for func in ast.ext:
		func_dict = ast_utilities.to_dict(func)
		if "body" in func_dict and "block_items" in func_dict["body"] and func_dict["_nodetype"] ==  "FuncDef":
			func_line_number_arr.append(int(str(func.coord).split(":")[1]))
	return func_line_number_arr

convert('test1.c')  