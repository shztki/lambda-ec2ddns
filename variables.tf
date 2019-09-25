variable "label" {
  type = "map"

  default = {
    namespace = "myself"
    stage     = "dev"
    name      = "ec2ddns"
  }
}
