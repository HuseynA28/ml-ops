# Deploy FastAPI ML Prediction API on AWS via Terraform
- Terraform will provision an EC2 instance
- The application code will be cloned from GitHub: https://github.com/erkansirin78/fastapi-advertising-prediction.git
- 

## 1. AWS web console
- Create an user
  - Name  example: ` ahmet-admin `
  - Select `Access key - Programmatic access `
  - Attach policy: `AdministratorAccess` permission user

## 2. Configure aws cli on VM
```commandline
(base) [train@localhost ~]$ cat ~/.aws/credentials
[default]
aws_access_key_id = trainkey
aws_secret_access_key = trainsecret

[aws]
aws_access_key_id = <your key will be here>
aws_secret_access_key = <your secret will be here>
```
## 3. Test aws cli
```commandline
(base) [train@localhost ~]$ aws s3 ls --profile aws

2022-03-06 20:50:07 mlops-on-aws
2022-03-12 09:08:21 vbo-mlflow-bucket
2022-02-22 09:44:38 vbo-mlops-bootcamp
```

## 4. Create terraform folder
- providers.tf
```commandline
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
  shared_credentials_files = ["~/.aws/credentials"]
  profile = "aws"
}
```

## 5. Copy/push project to VM

## 6. Terraform init
```commandline
(base) [train@localhost ~]$ mv 13_deploy_fastapi_on_aws_ec2 13
(base) [train@localhost ~]$ cd 13/terraform/
(base) [train@localhost terraform]$ terraform init

Initializing the backend...

Initializing provider plugins...
- Finding latest version of hashicorp/aws...
- Installing hashicorp/aws v4.14.0...
- Installed hashicorp/aws v4.14.0 (signed by HashiCorp)

Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.

```

## 7. In terraform folder 
- main.tf
 ```commandline
resource "aws_vpc" "mlops_vpc" {
  cidr_block = "10.123.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support = true

  tags = {
    Name = "dev"
  }
}
```

- Plan
```commandline
terraform plan

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
  + create

Terraform will perform the following actions:

  # aws_vpc.mlops_vpc will be created
  + resource "aws_vpc" "mlops_vpc" {
      + arn                                  = (known after apply)
      + cidr_block                           = "10.123.0.0/16"
      + default_network_acl_id               = (known after apply)
      + default_route_table_id               = (known after apply)
      + default_security_group_id            = (known after apply)
      + dhcp_options_id                      = (known after apply)
      + enable_classiclink                   = (known after apply)
      + enable_classiclink_dns_support       = (known after apply)
      + enable_dns_hostnames                 = true
      + enable_dns_support                   = true
      + id                                   = (known after apply)
      + instance_tenancy                     = "default"
      + ipv6_association_id                  = (known after apply)
      + ipv6_cidr_block                      = (known after apply)
      + ipv6_cidr_block_network_border_group = (known after apply)
      + main_route_table_id                  = (known after apply)
      + owner_id                             = (known after apply)
      + tags                                 = {
          + "Name" = "dev"
        }
      + tags_all                             = {
          + "Name" = "dev"
        }
    }

```

- Terraform apply
```commandline
terraform apply --auto-approve


...
...
Plan: 1 to add, 0 to change, 0 to destroy.
aws_vpc.mlops_vpc: Creating...
aws_vpc.mlops_vpc: Still creating... [10s elapsed]
aws_vpc.mlops_vpc: Creation complete after 12s [id=vpc-0b95775269a5c752b]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```
- State list
```commandline
terraform state list
aws_vpc.mlops_vpc
```

- Destroy 
` terraform destroy --auto-approve `

## 8. Subnet
- main.tf

## 9. Internet gateway

## 10. Route table

## 11. Route table association

## 12. Security Groups

## 13. The AMI Datasource
- Add datasources.tf
- Learn ami id from web console
- owner: AMIs -> Public images -> filter ami id -> Get Owner id 

## 14. Key Pair
```commandline
 ssh-keygen
```

- Enter file path /home/train/.ssh/mlops-aws
- Check keys
```commandline
(base) [train@localhost terraform]$ ls -al  /home/train/.ssh/
total 16
drwx------.  2 train train   63 May 20 12:21 .
drwx------. 34 train train 4096 May 19 19:37 ..
-rw-r--r--.  1 train train  376 May  1 16:52 known_hosts
-rw-------.  1 train train 1679 May 20 12:21 mlops-aws
-rw-r--r--.  1 train train  409 May 20 12:21 mlops-aws.pub
```
 
- main.tf 
```commandline
resource "aws_key_pair" "mlops_auth" {
  public_key = file("~/.ssh/mlops-aws.pub")
  key_name = "mlops-aws-key"
}
```

- AWS web console check EC2 Key Pairs

## 15. EC2 Instances

- Apply
- terraform state
- Learn public ip and connect ec2 instance
```commandline
(base) [train@localhost terraform]$ ssh -i ~/.ssh/mlops-aws ec2-user@3.122.194.80
```

## 16. User data
- Create userdata.tpl
- tpl stands for template
```commandline
sudo yum -y update
sudo yum -y install git
python3 -m pip install virtualenv
python3 -m virtualenv fastapi
source fastapi/bin/activate
git clone https://github.com/erkansirin78/fastapi-advertising-prediction.git
cd fastapi-advertising-prediction/fastapi_advertising_prediction/
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload

```

- In main.tf ec2 add user data 
user_data = file("userdata.tpl")

## 17. SSH Config scripts

## 18. Provisioners
