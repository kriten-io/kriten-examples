resource "aws_instance" "example" {
  ami           = "ami-0666c668000b91fcb" # Replace with a valid AMI for your region
  instance_type = "t2.micro"

  tags = {
    Name = "ExampleInstance"
  }
}
