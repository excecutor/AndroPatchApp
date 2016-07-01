# Inject code to smali file for method setJavaScriptEnabled(true)
import sys
import re
import subprocess



smalifile = sys.argv[1]
outfile = smalifile + '.patched'
p = re.compile('^\.method')
regex = re.compile('.*setJavaScriptEnabled*')

text_array = []



with open(smalifile, 'r' ) as input_data, open(outfile,'w')  as outputfile:

	def varManipulaton( string ):
		static_code_injection ='    const/4 '
		control_webview_value_false=' 0x0\n\n'
                control_webview_value_true =' 0x1\n'



                m = re.search('{.*[0-9]}', string)
                both_variables = m.group(0)
                a , b = both_variables.split(',')
                variable1 = re.search('[a-w][0-9]',a)   #Contrunction of string 
                variable2 = re.search('[a-w][0-9]',b)
                final_string_injection_false = static_code_injection + variable2.group(0) + ',' + control_webview_value_false
                final_string_injection_true = static_code_injection + variable2.group(0) + ',' + control_webview_value_true
                return        final_string_injection_false



	# Skips text before the beginning of the interesting block:
	for line in input_data:	
		text_array.append(line)
	
        idexList = []
        for idx, val in enumerate(text_array):
                if (  regex.match(val)):
                        a  = varManipulaton(val)
                        print idx, val ,a
                        idexList.append(int(idx))
        for num in idexList:
                        text_array.insert(num -1,a)
                        print "lalakis %s" ,num

	for item in text_array:
		outputfile.write(item)
	print 'File  successfully created!!!'

# define our method
def replace_all(text, dic):
        for i, j in dic.iteritems():
                text = text.replace(i, j)
                return text




print 'Smalif file : ' ,smalifile
print 'OutFile : ' , outfile

reps = { '$' :'\$'}
new_outfile = outfile
new_outfile = replace_all(new_outfile, reps)
new_smalifile = smalifile
new_smalifile = replace_all(new_smalifile, reps)

print 'New Smalif file : ' ,new_smalifile
print 'NEW OutFile : ' , new_outfile

p = subprocess.Popen('mv ' + new_outfile + ' ' + new_smalifile  , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
out, err = p.communicate()
