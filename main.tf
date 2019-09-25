terraform {
  required_version = "~> 0.12"
}

module "label" {
  source      = "git::https://github.com/cloudposse/terraform-null-label.git?ref=master"
  namespace   = "${lookup(var.label, "namespace")}"
  stage       = "${lookup(var.label, "stage")}"
  name        = "${lookup(var.label, "name")}"
  attributes  = ["${lookup(var.label, "namespace")}", "${lookup(var.label, "stage")}", "${lookup(var.label, "name")}"]
  delimiter   = "-"
  label_order = ["namespace", "stage", "name"]
}

## EC2/EBS label tags sample
#module "label_ec2" {
#  source      = "git::https://github.com/cloudposse/terraform-null-label.git?ref=master"
#  namespace   = "${lookup(var.label, "namespace")}"
#  stage       = "${lookup(var.label, "stage")}"
#  name        = "${lookup(var.label, "name")}"
#  attributes  = ["${lookup(var.label, "namespace")}", "${lookup(var.label, "stage")}", "${lookup(var.label, "name")}"]
#  delimiter   = "-"
#  label_order = ["namespace", "stage", "name"]
#  tags = {
#    "Ec2StartStop" = "Auto"
#    "PublicDNS"    = "example.com"
#    "PublicHost"   = "dev"
#    "PrivateDNS"   = "example.local"
#    "PrivateHost"  = "dev"
#  }
#}
#module "label_ebs" {
#  source      = "git::https://github.com/cloudposse/terraform-null-label.git?ref=master"
#  namespace   = "${lookup(var.label, "namespace")}"
#  stage       = "${lookup(var.label, "stage")}"
#  name        = "${lookup(var.label, "name")}"
#  attributes  = ["${lookup(var.label, "namespace")}", "${lookup(var.label, "stage")}", "${lookup(var.label, "name")}"]
#  delimiter   = "-"
#  label_order = ["namespace", "stage", "name"]
#  tags = {
#    "DlmSnapshot"  = "daily-0300-14"
#  }
#}
