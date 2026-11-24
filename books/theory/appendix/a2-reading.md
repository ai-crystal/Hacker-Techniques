# 附录 B　延伸阅读

下列材料的共同点是可获取、可核对，且比二手转述更可靠。读的时候留意它们的实验条件。

## B.1 内存与利用

- Aleph One, *Smashing The Stack For Fun And Profit*, Phrack 49, 1996。
- Crispin Cowan 等, *StackGuard: Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks*, USENIX Security 1998。
- Hovav Shacham, *The Geometry of Innocent Flesh on the Bone: Return-into-libc without Function Calls*, CCS 2007。
- Hovav Shacham 等, *On the Effectiveness of Address-Space Randomization*, CCS 2004。
- Laszlo Szekeres 等, *SoK: Eternal War in Memory*, IEEE S&P 2013。把内存错误的攻防史梳理成一条线。
- glibc 的 `malloc.c` 源码与 `malloc` 手册页。关于 chunk 与 bins 的权威描述只有源码。

## B.2 内核与虚拟化

- Linux 内核文档中的 `Documentation/admin-guide/security-bugs.rst` 与 `Documentation/security/` 目录。
- Jann Horn 关于内核提权与 Spectre 变体的公开分析（Project Zero 博客）。
- Windows 内部结构可参考 *Windows Internals*（Russinovich 等），对象管理器与令牌章节尤其相关。

## B.3 密码学与协议

- Dan Boneh, Victor Shoup, *A Graduate Course in Applied Cryptography*，作者主页可免费下载。
- RFC 8446（TLS 1.3）、RFC 9000（QUIC）、RFC 6749（OAuth 2.0）、RFC 7519（JWT）。
- Nadhem AlFardan, Kenneth Paterson, *Lucky Thirteen: Breaking the TLS and DTLS Record Protocols*, IEEE S&P 2013。
- Zakir Durumeric 等, *The Matter of Heartbleed*, IMC 2014。

## B.4 程序分析与检测

- Cristian Cadar, Koushik Sen, *Symbolic Execution for Software Testing: Three Decades Later*, CACM 2013。
- Patrice Godefroid 等, *SAGE: Whitebox Fuzzing for Security Testing*, 2012。
- Michał Zalewski, *American Fuzzy Lop* 的技术说明（afl-fuzz 的 README 与相关博客）。
- Robin Sommer, Vern Paxson, *Outside the Closed World: On Using Machine Learning for Network Intrusion Detection*, IEEE S&P 2010。
- MITRE ATT&CK 的官方文档，注意区分“技术”与“战术”的层级。

## B.5 侧信道与微架构

- Paul Kocher 等, *Spectre Attacks: Exploiting Speculative Execution*, IEEE S&P 2019。
- Moritz Lipp 等, *Meltdown: Reading Kernel Memory from User Space*, USENIX Security 2018。
- Yuval Yarom, Katrina Falkner, *FLUSH+RELOAD: A High Resolution, Low Noise, L3 Cache Side-Channel Attack*, USENIX Security 2014。
