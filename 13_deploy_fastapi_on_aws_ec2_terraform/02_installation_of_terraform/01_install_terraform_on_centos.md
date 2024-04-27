## 1. Install terraform on VM
```commandline
# Install yum-utils
sudo yum install -y yum-utils

# Add hashicorp repo
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo

# Install terraform
sudo yum -y install terraform

# Check version
terraform --version
```

