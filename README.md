# whois_export
This basic script uses the whois command line function to make calls to any supported TLDs

## Dependencies
* `whois` command line application

## Explaination
The script expects at least a domain provided by the `--domain` command, this can be a list separated by spaces.
You also need to provide a list of sections you want to query, this is done through the `--section` parameter, again can be a list (space separated) in the format `field=value` to identify sections you want.
Finally you will need to provide a list of fields you want to list out from those sections, done throught he `--fields` parameter.

## Usage
1. To see a list of fields you can list run a `whois` command
2. Basic example on running the command:

   ```bash
     python3 run.py --domains ed-moore.net eddyswebdesign.com google.com github.com --sections contact=technical contact=administrative --fields name phone address
   ```