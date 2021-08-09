# mydns-toolkit

MyDNS を利用する上で、私が使用しているスクリプトです。CentOS 7 と Fedora 34 で使用しています。利用制限はありませんので、ご自由にお使いください。

## 概要

### regist.sh, delete.sh

Let's Encrypt でワイルドカード証明書を取得する処理を自動化するためのスクリプトです。シェルスクリプトだけで書かれているので、特別に必要なものはありません。

/usr/local/sbin あたりに設置します。

```
MYDNS_TOOLKIT_URL=https://raw.githubusercontent.com/seinolab/mydns-toolkit/main
PREFIX=/usr/local
mkdir -p ${PREFIX}/sbin
curl -sSL "${MYDNS_TOOLKIT_URL}/{delete,notify,regist}.sh" -o ${PREFIX}/sbin
chmod 700 ${PREFIX}/sbin/{delete,notify,regist}.sh
```

MyDNS の ID とパスワードを設定します。/root/.mydns に以下のように `:` でつなげて ID とパスワードを書きます。パーミッションは 600 にしましょう。

```
mydns999999:password
```

あとは、通常通り、certbot を実行します（実際に動かすときは `--dry-run` を外してください）。

```
# certbot certonly --dry-run --manual --preferred-challenges dns \
    --manual-auth-hook "/usr/local/sbin/regist.sh" \
    --manual-cleanup-hook "/usr/local/sbin/delete.sh" \
    --domain example.com --domain *.example.com \
    --server https://acme-v02.api.letsencrypt.org/directory \
    --agree-tos -m user@example.com
```

動作確認のために、これらのスクリプトは以下のようなログを出力します。

```
Jul 14 18:50:24 hostname MyDNS[12066]: REGIST example.com - HTTP/2 200
Jul 14 18:50:29 hostname MyDNS[12079]: REGIST example.com - HTTP/2 200
Jul 14 18:50:35 hostname MyDNS[12092]: DELETE example.com - HTTP/2 200
Jul 14 18:50:39 hostname MyDNS[12105]: DELETE example.com - HTTP/2 200
```

### notify.sh

MyDNS の利用を継続するために、IP アドレスを通知するスクリプトです。cron か systemd で定期的に動かします。

MyDNS の ID とパスワードを設定します。/root/.mydns に以下のように `:` でつなげて ID とパスワードを書きます。パーミッションは 600 にしましょう。

```
mydns999999:password
```

あとは、cron か systemd で各自必要な間隔で動かしてください。

systemd で起動する場合は、以下の設定をインストールします。

```
mkdir -p ${PREFIX}/systemd/system
curl -sSL "${MYDNS_TOOLKIT_URL}/mydns-notify-ip.{timer,service}" -o ${PREFIX}/systemd/system
```

起動時刻を変更する場合は、以下のように入力して設定を変更します。

```
systemctl edit mydns-notify-ip.timer
```

設定が変更できたら、タイマーを有効にします。

```
systemctl start mydns-notify-ip.timer
systemctl enable mydns-notify-ip.timer
```

動作確認のために、/etc/mydns/notify.sh は以下のようなログを出力します。

```
Jul 14 20:00:00 hostname MyDNS[999]: https://ipv4.mydns.jp/login.html - HTTP/1.1 200 OK
```

エラーになった場合は、以下のようなログを出力します。

```
Jul 20 20:00:00 hostname MyDNS[999]: https://ipv4.mydns.jp/login.html - curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to ipv4.mydns.jp:443
```

## 今後の課題

割と自分用に公開している感じなので、ドキュメントが適当ですみません。小さくシンプルなスクリプトですので、コードを読んだ方が早いかもです。

- [ ] マルチドメインに対応する。
- [ ] urlencode をサボっているので真面目にやる。
