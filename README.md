# mydns-toolkit

MyDNS を利用する上で、私が使用しているスクリプトです。本家配布の同機能のスクリプトは PHP で書かれていますが、私は PHP を使ってないので、シェルスクリプトだけで書き直しました。CentOS 7 と Fedora 34以降で使用実績があり、現在も使用中です。利用制限はありませんので、ご自由にお使いください。

## 概要

Let's Encrypt でワイルドカード証明書を取得する処理を自動化するためのスクリプトです。シェルスクリプトだけで書かれているので、特別に必要なものはありません。

## インストール

RPM からインストールする場合は、以下のようにします。Fedora 42 用に見えますが、他のディストリビューションでも大体使えると思います。

```
# sudo dnf install https://github.com/seinolab/mydns-toolkit/releases/download/1.0/mydns-toolkit-1.0-1.fc42.noarch.rpm
```

RPM をソースから作る場合は，以下のようにします。

```
$ sudo dnf install rpm-build
$ curl -sL https://github.com/seinolab/mydns-toolkit/archive/refs/tags/1.0.tar.gz -o mydns-toolkit-1.0.tar.gz
$ rpmbuild -tb --clean mydns-toolkit-1.0.tar.gz
```

ビルドに成功すると `~/rpmbuild/RPMS/noarch/` に出力されるので、そのファイルをインストールします。`fc42` の部分は各自ご使用中のディストリビューションを表す文字列に置き換えて解釈してください。

```
$ ls ~/rpmbuild/RPMS/noarch/
mydns-toolkit-1.0-1.fc42.noarch.rpm
$ sudo dnf install ~/rpmbuild/RPMS/noarch/mydns-toolkit-1.0-1.fc42.noarch.rpm
```

このパッケージでインストールされるのは、以下のファイルです。

```
$ rpm -ql mydns-toolkit
/usr/lib/systemd/system/mydns-notify-ip.service
/usr/lib/systemd/system/mydns-notify-ip.timer
/usr/libexec/mydns-toolkit/delete.sh
/usr/libexec/mydns-toolkit/notify.sh
/usr/libexec/mydns-toolkit/regist.sh
```

## 準備

MyDNS の ID とパスワードを設定します。セキュリティを考えて、一般ユーザから読み書きできない `/root/.mydns` に配置します。以下のように `:` でつなげて ID とパスワードを書きます。パーミッションは `600` または `400` にしましょう。

```
mydns999999:password
```

## 証明書の取得

通常通り、certbot を実行します（実際に動かすときは `--dry-run` を外してください）。

```
$ sudo certbot certonly --dry-run --manual --preferred-challenges dns \
		--manual-auth-hook　'/usr/libexec/mydns-toolkit/regist.sh' \
		--manual-cleanup-hook '/usr/libexec/mydns-toolkit/delete.sh' \
		--domain example.com --domain '*.example.com' \
		--server https://acme-v02.api.letsencrypt.org/directory
```

動作確認のために、`regist.sh` と `delete.sh` は以下のようなログを出力します。

```
Jul 14 18:50:24 hostname MyDNS[12066]: REGIST example.com - HTTP/2 200
Jul 14 18:50:29 hostname MyDNS[12079]: REGIST example.com - HTTP/2 200
Jul 14 18:50:35 hostname MyDNS[12092]: DELETE example.com - HTTP/2 200
Jul 14 18:50:39 hostname MyDNS[12105]: DELETE example.com - HTTP/2 200
```

## IP アドレスの通知

MyDNS の利用を継続するために、IP アドレスを通知する必要があります。`cron` か `systemd` で定期的に動かします。

配布しているパッケージでは、`systemd` によって毎日 6:00 〜 7:00 くらいに実行する設定になっています。起動時刻をカスタマイズする場合は、以下のように入力して設定を変更します。

```
$ sudo systemctl edit mydns-notify-ip.timer
```

エディタが起動するので、`### Anything between here ...` から `### Lines below ...` の間に、以下のように上書きしたい設定を記述します。

```
### Anything between here and the comment below will become the new contents of the file

[Timer]
OnCalendar=
OnCalendar=*-*-* 12:00

### Lines below this comment will be discarded
```

定期実行を有効にします。

```
$ sudo systemctl start mydns-notify-ip.timer
$ sudo systemctl enable mydns-notify-ip.timer
```

動作確認のために、`notify.sh` は以下のようなログを出力します。

```
Jul 14 06:12:34 hostname MyDNS[999]: https://ipv4.mydns.jp/login.html - HTTP/1.1 200 OK
```

エラーになった場合は、以下のようなログを出力します。

```
Jul 14 06:12:34 hostname MyDNS[999]: https://ipv4.mydns.jp/login.html - curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to ipv4.mydns.jp:443
```

## 今後の課題

割と自分用に公開している感じなので、ドキュメントが適当ですみません。小さくシンプルなスクリプトですので、コードを読んだ方が早いかもです。

- [ ] マルチドメインに対応する。これをやりたいなら Python あたりで書き直した方が良さそうです。
