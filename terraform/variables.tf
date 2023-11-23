variable "aws_access_key" {
  default = file("/etc/secret/aws_access_key_id")
}

variable "aws_secret_key" {
  default = file("/etc/secret/aws_secret_access_key")
}

