# 附录 A　命令与工具速查

只列实战里反复用到的，参数以常见版本为准。装在 Kali 或自己配的 Ubuntu 上都可用。

## A.1 网络与侦察

```bash
ip a                       # 本机地址与网卡
ip route                   # 路由与默认网关
ss -lntup                  # 监听端口与对应进程
nmap -sn 10.10.10.0/24     # 主机发现
nmap -sT -p- --min-rate 2000 10.10.10.5   # 全端口 TCP 连接扫描
nmap -sV -sC -p 22,80,445 10.10.10.5      # 版本与默认脚本
dig +short example.lab     # 解析结果
dig axfr @10.10.10.5 example.lab          # 尝试区域传送
curl -I http://10.10.10.5  # 只看响应头
curl -s -o /dev/null -w '%{http_code} %{size_download}\n' http://10.10.10.5/a
```

## A.2 抓包与代理

```bash
tcpdump -i eth0 -nn port 80 -w cap.pcap
tcpdump -r cap.pcap -A -nn 'tcp port 80'
tshark -r cap.pcap -Y 'http.request' -T fields -e http.host -e http.request.uri
ssh -D 1080 -N user@10.10.10.5            # 动态转发（socks5）
ssh -L 8080:127.0.0.1:80 user@10.10.10.5  # 本地端口转发
```

## A.3 Web

```bash
ffuf -u http://10.10.10.5/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,301,302
ffuf -u http://10.10.10.5 -H 'Host: FUZZ.example.lab' -w subs.txt -fs 4242
sqlmap -u 'http://10.10.10.5/item?id=1' --batch --level 3 --risk 2
nikto -h http://10.10.10.5
whatweb -a 3 http://10.10.10.5
```

## A.4 二进制

```bash
checksec --file=./vuln            # 保护项一览（pwntools 也有 checksec）
file ./vuln && readelf -hW ./vuln
objdump -d -M intel ./vuln | less
gdb -q ./vuln -ex 'set disassembly-flavor intel' -ex 'b main' -ex run
python3 -c "from pwn import *; print(cyclic(200))"   # 生成模式串
python3 -c "from pwn import *; print(cyclic_find(0x6161616c))"
ROPgadget --binary ./vuln --only 'pop|ret'
one_gadget /lib/x86_64-linux-gnu/libc.so.6
```

## A.5 Windows 与域

```powershell
whoami /all                       # 用户、组、特权
net user /domain                  # 域用户
net group "Domain Admins" /domain
Get-ADUser -Filter * -Properties ServicePrincipalName | ? ServicePrincipalName
Get-ADComputer -Filter * | select Name,OperatingSystem
nltest /dclist:lab.local
klist                             # 当前票据
```

```bash
impacket-GetUserSPNs lab.local/user:pass -dc-ip 10.10.10.10 -request
impacket-GetNPUsers lab.local/ -usersfile users.txt -dc-ip 10.10.10.10
impacket-secretsdump lab.local/administrator:pass@10.10.10.11
crackmapexec smb 10.10.10.0/24 -u user -p pass --shares
```

## A.6 主机枚举

```bash
id && sudo -l                     # 身份与可用的 sudo 规则
find / -perm -4000 -type f 2>/dev/null      # SUID
getcap -r / 2>/dev/null                     # capabilities
cat /etc/crontab; ls -l /etc/cron.*         # 定时任务
systemctl list-units --type=service --state=running
uname -a; cat /etc/os-release               # 内核与发行版
```

## A.7 样本与日志

```bash
file sample.bin && sha256sum sample.bin
strings -n 6 -a sample.bin | less
objdump -x sample.bin | head -60            # 节表与导入（PE 用 objdump 亦可）
yara -r rules.yar samples/                  # 批量匹配
```

```bash
# Sigma 规则转成具体后端查询
sigma convert -t splunk rules/proc_creation.yml
```

## A.8 常用路径

| 用途 | 路径 |
| --- | --- |
| Linux 口令与组 | `/etc/passwd`、`/etc/shadow`、`/etc/group` |
| SSH 配置与密钥 | `/etc/ssh/sshd_config`、`~/.ssh/` |
| 定时任务 | `/etc/crontab`、`/etc/cron.d/`、`/var/spool/cron/` |
| Web 根目录 | `/var/www/html`、`/srv/http` |
| 日志 | `/var/log/auth.log`、`/var/log/syslog`、`/var/log/nginx/` |
| Windows 事件 | `C:\Windows\System32\winevt\Logs\` |
| 域数据库 | `C:\Windows\NTDS\ntds.dit` |
