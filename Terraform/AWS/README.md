## Example of modular AWS hcl files to provision instances

* Modules for EC2 and RDS
* Environment for dev (wich can be replicated and adapted for prod)

## Usage

```bash
terraform -chdir=environments/dev init
terraform -chdir=environments/dev plan
terraform -chdir=environments/dev apply
``` 

