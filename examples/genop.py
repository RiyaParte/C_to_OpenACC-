func_for_loop_line_number_arr=[11,16,16,20,20,24]
func_for_loop_line_number_arr=func_for_loop_line_number_arr[:-1]
func_for_loop_line_number_arr = set(func_for_loop_line_number_arr)  
func_for_loop_line_number_arr = list(func_for_loop_line_number_arr)

print(func_for_loop_line_number_arr)
stmt = "#pragma acc parallel loop"

f = open("C:/Users/parte/Desktop/temp/examples/test.c",'r')
f1 = open("C:/Users/parte/Desktop/temp/examples/result.c","a")
x=0
lines = f.readlines()
print(lines)
print(x)


for i in range(len(lines)):
    if i+1 in func_for_loop_line_number_arr:
        f1.write(stmt+'\n')
        f1.write(lines[i])
        #print(lines[i])
    else:
        f1.write(lines[i])