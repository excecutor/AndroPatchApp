# Inject code to smali file for method setJavaScriptEnabled(true)
import sys
import re
import subprocess



smalifile = sys.argv[1]
outfile = smalifile + '.patched'
lookup = 'setJavascript'
p = re.compile('^\.method')
regex = re.compile('.*iget-object.*android/webkit/WebView;')

text_array = []



with open(smalifile, 'r' ) as input_data, open(outfile,'w')  as outputfile:

	def varManipulaton( string ):
		static_code_injection_1 ='    invoke-static {'
		static_code_injection_2	='}, Lcom/vasts/JSinject;->setInject(Landroid/webkit/WebView;)V'
		control_webview_value_false=' 0x0\n\n'
                control_webview_value_true =' 0x1\n'

		m = re.search('[a-z][0-9]', string) 
		both_variables = m.group(0)
		Final_inject = static_code_injection_1 + both_variables + static_code_injection_2

                return	Final_inject



	for line in input_data:	
		text_array.append(line)
	idexList = []
	for idx, val in enumerate(text_array):
		if (  regex.match(val)):
			a  = varManipulaton(val)
			print idx, val ,a
			text_array.insert(idx + 1,'\n')
			text_array.insert(idx + 1,a)
			text_array.insert(idx + 1,'\n')



	
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
