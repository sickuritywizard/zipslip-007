# zipslip-007
Tool to create payloads for exploiting ZipSlip Vulnerability

## Usage
```
options:
  -h, --help               Show this help message and exit
  -i, --input PAYLOADFILE  Payload File that has to be written/overwritten on target server
  -o, --output OUTPUTFILE  Output File Name
  -d, --depth DEPTH.       Depth of the Traversal [Default: 3]
  -p, --path PATH          Path to append to the traversal. Ex: var/www/webroot
  -c, --completeDir DIR    Adds All files in the provided Directory to the archive
  --os TARGETOS            Target Platform (win|unix) [Default:unix)
```

## Example
>  zipslip-007 -i payload.txt -o Exploit.tar -d 3 -c includeFiles/ -p "var/www/webroot/"

## Note
> This is similar to evilarc with few new features
