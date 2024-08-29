# An AI chat bot

This is basic terminal chat bot. Uses Gemini API. Get an API and set

    export GEMINI_API_KEY=my-super-secret-key 

Install

    pip install .

Start a chat

    ask

Or pass in a file to work on

    ask file.txt

Or ask a question to work on

    ask what time is love

Hit return to ask the default question, e.g. proof read or answer the question.
Or elaborate and ask more.

## Example

Start off a chat on a given theme and then quick fire requests

```sh
❯ ask show me terraform for the following
```

(-_-) s3

```terraform
resource "aws_s3_bucket" "example" {
  bucket = "my-bucket-name"

  acl = "private"

  tags = {
    Name = "My bucket"
  }
}
```

(-_-) vpc

```terraform
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"

  enable_dns_hostnames = true
  enable_dns_support = true
}

resource "aws_subnet" "public" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = true
}
```

(-_-) rds

```terraform
resource "aws_db_instance" "default" {
  allocated_storage = 10
  engine             = "mysql"
  engine_version     = "5.7.28"
  instance_class     = "db.t2.micro"
  name               = "mydb"
  username           = "admin"
  password           = "password"
  db_subnet_group_name = "default"
}

resource "aws_db_subnet_group" "default" {
  name       = "default"
  subnet_ids = [aws_subnet.public.id]
}
```
