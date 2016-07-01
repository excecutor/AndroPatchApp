# -*- coding: utf-8 -*-
import argparse
from argparse import RawTextHelpFormatter
import json
import logging
import os
import re
import subprocess
import sys
from time import sleep
from shutil import copyfile
from termcolor import colored


# Initialise the logger:
logger = logging.getLogger("Droid")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()  # console handler for the logger
ch.setLevel(logging.INFO)
ch.setFormatter( logging.Formatter("  >> %(name)s: [%(levelname)s] %(message)s") )  # log message format
logger.addHandler(ch)  # add the handler to the logger

APKTOOL = "../Apktool/apktool"
SIGNLIB = "../lib/signapk.jar"
CAKEY = '../keys/certificate.pem' 
USKEY = '../keys/key.pk8'
SOURCE_PATCH = "../source"
SOURCE_FILE_1 = "JSinject.smali"
SOURCE_FILE_2 = "BuildConfig.smali"
SOURCE_FILE_3 = "JSinject$1.smali"
SOURCE_FILE_4 = 'LocJSinject.smali'
SOURCE_FILE_5 = 'AdJSinject.smali'
SOURCE_FILE_6 = 'htmlReplace.smali'
SOURCE_FILE_7 = 'injectRepRemov.smali'


###MAP 1-1 between VUL_COD & PYTHON Script

#Vulnurable code methods
VUL_CODE_1 = '\'.*iget-object.*android/webkit/WebView;\''
VUL_CODE_2 = '\'.*setAllowFileAccessFromFileURLs*\''
VUL_CODE_3 = '\'.*setAllowUniversalAccessFromFileURLs*\''
VUL_CODE_4 = '\'.*setJavaScriptEnabled*\''
#Script Suppport
PYTHON_SCRIPT_1 ='../libinject.py'
PYTHON_SCRIPT_2 ='../inject_FileAccessURL.py'
PYTHON_SCRIPT_3 ='../inject_setUniversalAccessFromurl.py'
PYTHON_SCRIPT_4 ='../inject_setJVen.py'

ADNETWORK_LIST =" 'com/google/ads' "
adnet1  = " 'com/google/ads' "
adnet2 =  " 'com/ﬂurry'     "
adnet3 =  " 'com/inmobi'     "
adnet4 =  " 'com/tapjoy'     "
adnet5 =  " 'com/mobclix'    "
adnet6 =  " 'com/chartboost' "
adnet7 =  " 'com/adwhirl'    "
adnet8 =  " 'com/mopub'      "
adnet9 =  " 'com/greystripe' " 
adnet10 = " 'com/google/ads|com/greystripe|com/ﬂurry|com/inmobi|com/tapjoy|com/mobclix|com/chartboost|com/adwhirl|com/mopub|com/greystripe|com/google/android/gms' "

def main(argv=None):

	# Retrieve command-line parameters:
	parser = argparse.ArgumentParser(description="Droid description: \n"
						"  >> %(prog)s /path/to/file.apk\n"
						"  >> %(prog)s --no-string-processing /path/to/file.apk\n"
						"  >> %(prog)s /path/to/file.apk --emextract\n"
						"  >> %(prog)s --no-string-processing /path/to/file.apk --extract\n"
						"  >> %(prog)s /path/to/file.apk --extract /dir/where/to/save/APK/info/\n"
						"  >> %(prog)s --help",
				formatter_class=RawTextHelpFormatter)
	parser.add_argument("target", metavar="TARGET_FILE", type=str, help="The targeted APK package to analyse.")
	parser.add_argument("-e", "--extract", type=str, nargs="?", const="./", action="store", dest="extract_to_directory", help="Extract and store all the APK entries as well as it info in a given folder (default: ./APK).")
	parser.add_argument("-m",  "--mode", type=str, nargs="?", const="./", action="store", dest="mode_injection",  help="Choose mode of Injection.'locInject|adInject|adRequest' ")
        parser.add_argument("-n",  "--netad", type=str, nargs="?", const="./", action="store", dest="adnet_injection",  help="Choose Ad Network of Injection.'admob|flurry|inmobi|tapjoy|chartboost|adwhirl|flury|greystripe' ")


	args = parser.parse_args()
	print colored ('Procedure Started.....','green')
        print colored('Filename :' +  args.target,'green')
	# Check mode Injection
	modeInject = args.mode_injection
        modeInject = modeInject.strip(' ')
        adnet = args.adnet_injection
        adnet = adnet.strip(' ')

        if   (adnet == "admob"):
                ADNETWORK_LIST = adnet1
        elif (adnet  == "flurry"):
                ADNETWORK_LIST = adnet2
        elif (adnet == "inmobi"):
                ADNETWORK_LIST = adnet3
        elif (adnet == "tapjoy"):
                ADNETWORK_LIST = adnet4
        elif (adnet == "mobcli"):
                ADNETWORK_LIST = adnet5
        elif (adnet == "chartboost"):
                ADNETWORK_LIST = adnet6
        elif (adnet == "adwhirl"):
                ADNETWORK_LIST = adnet7
        elif (adnet == "mopub"):
                ADNETWORK_LIST = adnet8
        elif (adnet == "greystripe"):
                ADNETWORK_LIST = adnet9
        elif (adnet == "allAdNet"):
                ADNETWORK_LIST = adnet10
        else:
                pass




	if (modeInject == "locInject"):
		print colored('Mode Injection: ' + modeInject,'green')
		SOURCE_INJCT = SOURCE_FILE_4
	elif (modeInject == "adInject"):
		print colored('Mode Injection: ' + modeInject,'green')
		SOURCE_INJCT = SOURCE_FILE_5
        elif (modeInject == "adRequest"):
                print colored('Mode Injection: ' + modeInject,'green')
                SOURCE_INJCT = SOURCE_FILE_6
        elif (modeInject == "adReplRem"):
                print colored('Mode Injection: ' + modeInject,'green')
                SOURCE_INJCT = SOURCE_FILE_7
	else: 	
		print colored ('Wrong mode selection', 'red')
		exit()

	# Extract the APK file name (without extension):
	filename = os.path.basename(args.target)
	if re.search("\.apk", args.target, re.IGNORECASE):
		filename = str(filename[0:-4])

	if args.extract_to_directory is not None:
	# Extract all the APK entries and info to a given directory:
		dir = args.extract_to_directory

		# Check whether no output directory was given (i.e. the default one):
		if args.extract_to_directory == "./":
			dir += filename
		#print dir , args.target, filename, '\n'
	decompileApk(dir, args.target, filename)
	NUM=0
	injection_code0(dir,VUL_CODE_1,PYTHON_SCRIPT_1,ADNETWORK_LIST,NUM,adnet)
        injection_code0(dir,VUL_CODE_2,PYTHON_SCRIPT_2,ADNETWORK_LIST,NUM,adnet)
        injection_code0(dir,VUL_CODE_3,PYTHON_SCRIPT_3,ADNETWORK_LIST,NUM,adnet)
        injection_code0(dir,VUL_CODE_4,PYTHON_SCRIPT_4,ADNETWORK_LIST,NUM,adnet)
        injectLib(dir, SOURCE_PATCH, SOURCE_FILE_1, SOURCE_FILE_2, SOURCE_FILE_3,SOURCE_INJCT)
        patchname = compileApk(dir, args.target, filename)
	signApk   = signapk(patchname, dir, SIGNLIB,CAKEY,USKEY)


def injectLib(output_dir, path, file1, file2, file3,fileInjct):
	command =  output_dir + '/' + 'smali' + '/' + 'com/vasts'
	command1 = output_dir + '/' + 'smali' + '/' + 'com'
	if (os.path.isdir(output_dir + '/' + 'smali' + '/' + 'com')):
		os.makedirs(command)
	else:
		os.makedirs(command1)
		os.makedirs(command)

        src0 = path + '/' + fileInjct
        dst0 = path + '/' + file3
        copyfile(src0, dst0)


	src1 = path + '/' + file1
	dst1 = command + '/' + file1
	copyfile(src1, dst1)

	src2 = path + '/' + file2
        dst2 = command + '/' + file2
        copyfile(src2, dst2)
	
        src3 = path + '/' + file3
        dst3 = command + '/' + file3
        copyfile(src3, dst3)



def injection_code0(output_dir,vul_code,supp_script,ad_list,num,adnet):
	path_file = "/tmp/inject%s.log" % (num)
	open(path_file, 'a').close()
	code = vul_code
	inscript = supp_script


	find_grep = subprocess.Popen('which grep'   , stdout=subprocess.PIPE, stderr=None, shell=True)
	grep, err = find_grep.communicate()
	grep = grep.strip(' \t\n\r')

        find_egrep = subprocess.Popen('which egrep'   , stdout=subprocess.PIPE, stderr=None, shell=True)
        egrep, err = find_egrep.communicate()
        egrep = egrep.strip(' \t\n\r')


        find_python = subprocess.Popen('which python'   , stdout=subprocess.PIPE, stderr=None, shell=True)
        python, err = find_python.communicate()
        python      = python.strip(' \t\n\r')

	def run(cmd, logfile):
		with open(logfile, 'w' ) as fout:
			p = subprocess.Popen(cmd, stdout=fout, stderr=None, shell=True)
			ret_code = p.wait()
			return ret_code

	# define our method
	def replace_all(text, dic):
		for i, j in dic.iteritems():
			text = text.replace(i, j)
		return text

        def replace_grep(adlist,grep,egrep,adnet):
           if ( adnet == "allAdNet"):
                return egrep
           else :
                return grep


	reps = { '$' :'\$'}
	command = grep + ' -ir ' + ' ' + code + ' '+  output_dir + '/' + 'smali' +  ' | ' + replace_grep(ad_list,grep,egrep,adnet) + ' -i ' + ad_list  +   " | awk -F ':' '{print$1}'  | sort -u " 
	print colored('Injection Procedure Started.... ','green')
	print colored("Inject lib %s " %ad_list,'blue')
        print colored('Command: %s ' %command ,'red')
	status = run(command,path_file)


        with open(path_file, 'r+' ) as input_path:

		for path in input_path.readlines():
			path = replace_all(path, reps)
                	p = subprocess.Popen(python  + ' ' + inscript + ' ' + path     , stdout=subprocess.PIPE, stderr=None, shell=True)
                	inf_file, err = p.communicate()
			path = path.strip(' \t\n\r')
	input_path.close()
	print colored ('Injection Successfully  finished', 'green')


def decompileApk(output_dir, filepath, filename ):
	print colored ("Decompile apk ...",'green')
	os.makedirs(output_dir)
	p = subprocess.Popen(APKTOOL + ' ' + 'd '+ '-f '+ '-o '+ output_dir + ' ' + filepath   , stdout=subprocess.PIPE, stderr=None, shell=True)
	out, err = p.communicate()
	print colored(  "APK Successful Decompiled  in directory:  %s "  %(output_dir) , 'red')

def compileApk(output_dir, filepath, filename ):
	print colored ("Recompile apk ...",'green')
	p = subprocess.Popen(APKTOOL + ' ' + 'b '+ '-f '+ '-o '+ 'patched.' + filename + '.apk' + ' ' + output_dir   , stdout=subprocess.PIPE, stderr=None, shell=True)
        out, err = p.communicate()
        patched_name = "patched.%s.apk" %(filename)
        print colored("APK Successful Compiled \n" ,  'green')
	patched_name = patched_name.strip(' \t\n\r')
	return patched_name

def signapk( apkfilename , output_dir, SIGNLIB,CAKEY,USKEY):
	print colored ("Sign Apk", 'green')
        print colored (apkfilename, 'red')

	signapkfilename = "sign.%s" %(apkfilename)
	signapk = "java -jar %s %s %s  %s %s " %(SIGNLIB,CAKEY,USKEY,apkfilename,signapkfilename)
	p = subprocess.Popen( signapk  , stdout=subprocess.PIPE, stderr=None, shell=True)
        out, err = p.communicate()
	
	if os.path.isfile(signapkfilename):
		print colored ("APK Successfully Signed: %s" %(signapkfilename) , 'red')
                p = subprocess.Popen( 'mv ' + signapkfilename + ' ../upload/'  , stdout=subprocess.PIPE, stderr=None, shell=True)
                out, err = p.communicate()
                delete_all(apkfilename, 'decompile')
        	return signapkfilename


def dex2jar (output_dir, filepath):
        os.makedirs(output_dir +  'dx2jrfold' )
        dx2jr_dir = output_dir + 'dx2jrfold'
	filedx2jar = 'class_dx.jar'
	p = subprocess.Popen(DEX2JAR + " -f " + filepath + " -o " + dx2jr_dir + '/'+  filedx2jar, stdout=subprocess.PIPE, stderr=None, shell=True)
	out, err = p.communicate()

	os.makedirs(output_dir +  'jda' )
	p = subprocess.Popen("/bin/bash " + JDSCR + "  " +  dx2jr_dir + "/" + filedx2jar + " " + output_dir + "jda" , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = p.communicate()


def delete_all(del_patch, del_deco ):
 del_all = [ del_patch, del_deco]

 for x in del_all:
     pipe = subprocess.Popen("rm  -rf "  + x , stdout=subprocess.PIPE, stderr=None, shell=True)


if __name__ == "__main__":
	sys.exit(main())
