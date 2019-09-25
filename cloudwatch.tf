resource "aws_cloudwatch_event_rule" "this" {
  name        = "${module.label.id}"
  description = "${module.label.id}"

  event_pattern = <<PATTERN
{
  "source": [
    "aws.ec2"
  ],
  "detail-type": [
    "EC2 Instance State-change Notification"
  ],
  "detail": {
    "state": [
      "running",
      "terminated"
    ]
  }
}
PATTERN
}

resource "aws_cloudwatch_event_target" "this" {
  rule = "${aws_cloudwatch_event_rule.this.name}"
  arn  = "${aws_lambda_function.this.arn}"
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/lambda/${aws_lambda_function.this.function_name}"
  retention_in_days = 30
}
