resource "aws_vpc" "mlops_vpc" {
  cidr_block           = "10.123.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "dev"
  }
}

resource "aws_subnet" "mlops_public_subnet" {
  cidr_block              = "10.123.1.0/24"
  vpc_id                  = aws_vpc.mlops_vpc.id
  map_public_ip_on_launch = true
  availability_zone       = "eu-central-1a"

  tags = {
    Name = "dev-public"
  }
}

resource "aws_internet_gateway" "mlops_internet_gateway" {
  vpc_id = aws_vpc.mlops_vpc.id

  tags = {
    Name = "dev-igw"
  }
}

resource "aws_route_table" "mlops_public_rt" {
  vpc_id = aws_vpc.mlops_vpc.id

  tags = {
    Name = "dev-public-rt"
  }
}

resource "aws_route" "default_route" {
  route_table_id         = aws_route_table.mlops_public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.mlops_internet_gateway.id
}

resource "aws_route_table_association" "mlops_public_assoc" {
  route_table_id = aws_route_table.mlops_public_rt.id
  subnet_id      = aws_subnet.mlops_public_subnet.id
}

resource "aws_security_group" "mlops_sg" {
  name = "dev-sg"
  description = "Dev security group"
  vpc_id = aws_vpc.mlops_vpc.id

  ingress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    protocol  = "-1"
    to_port   = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_key_pair" "mlops_auth" {
  public_key = file("~/.ssh/mlops-aws.pub")
  key_name = "mlops-aws-key"
}

resource "aws_instance" "mlops_dev_node" {
  instance_type = "t2.micro"
  ami = data.aws_ami.server_ami.id
  key_name = aws_key_pair.mlops_auth.id
  vpc_security_group_ids = [aws_security_group.mlops_sg.id]
  subnet_id = aws_subnet.mlops_public_subnet.id
  user_data = file("userdata.tpl")

  tags = {
    Name = "mlops-dev-node"
  }

  root_block_device {
    volume_size = 8
  }

}