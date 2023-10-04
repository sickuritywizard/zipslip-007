# zipslip-007
Tool to create payloads for exploiting ZipSlip Vulnerability

## Usage
```
options:
  -h, --help               Show this help message and exit
  -i, --input PAYLOADFILE  Payload File that has to be written/overwritten on target server
  -o, --output OUTPUTFILE  Output File Name
  -d, --depth DEPTH.       Depth of the Traversal [Default: 3]
  -t, --type ARCHIVETYPE   File Type - zip,tar,gz,tgz,bz2,jar (Default: tar)
  -p, --path PATH          Path to append to the traversal. Ex: var/www/webroot
  --dir DIR                Adds All files in the provided Directory to the archive
  --os TARGETOS            Target Platform (win|unix) [Default:unix)
  -ex, --example           Show Usage Examples
```

## Example
>  zipslip-007 -i payload.txt -o exploit.tar -d 3 -dir includeFiles/ -p "var/www/webroot/" -t tar

>  zipslip-007 -i payload.txt -o exploit.tar -d 3 -dir includeFiles/ -p "var/www/webroot/" -t bz2
