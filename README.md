# Lambda code for EC2 Dynamic DNS to Route53

## Description
EC2 の起動/削除時にタグ情報に従い Route53 へのレコード登録/削除を実施する Pythonスクリプトを lambda に登録し、CloudWatchEvent で実行するサンプル

## Test Sample
テストといっても、実際に環境に対して実行されてしまうので注意
```
# cd source/
# pip install python-lambda-local
# pip install -r requirements.txt -t lib
# python-lambda-local --function lambda_handler --library lib --timeout 30 main.py event.json
```
```
# cat event.json
{
  "detail": {
    "instance-id": "i-abcd1111",
    "state": "running"
  }
}
```

## EC2 Tags
|key  |value  |
|---|---|
|PublicDNS  |ドメイン名  |
|PublicHost  |ホスト名  |
|PrivateDNS  |プライベートドメイン名  |
|PrivateHost  |プライベートホスト名  |

## Event
CloudWatchイベント側で EC2 の StateChange にて running/terminated を指定

## Remark
* PublicIP が変わっても固定の FQDN で常にアクセスできるようにしておきたいときに利用