# 理论篇

> 漏洞、内存与协议的深层结构

为什么栈溢出能改写控制流，为什么堆上的一个字节能变成任意写，为什么加了地址随机化攻击者还能算准地址，为什么 TLS 的握手设计得这么绕。这一册不回避细节，把体系结构、可执行文件、分配器、密码学、协议和程序分析逐层拆开。

它不教你点哪个按钮。它解释那些按钮背后成立与不成立的条件，以及在什么情况下这些条件会失效。读完能自己判断一篇漏洞分析写得对不对。

共 16 章 · 147 页

[从第 1 章开始](chapters/ch01.md)　·　<a href="../../output/v2-theory.pdf" target="_blank" rel="noopener" data-router-ignore>下载本册 PDF</a>

## 目录

- [前言](front/preface.md)
- [第 1 章　指令与微架构：一条指令走了多远](chapters/ch01.md)
- [第 2 章　可执行文件与加载器](chapters/ch02.md)
- [第 3 章　调用约定与栈的物理结构](chapters/ch03.md)
- [第 4 章　堆与分配器：malloc 的账本](chapters/ch04.md)
- [第 5 章　利用原语：从越界到任意读写](chapters/ch05.md)
- [第 6 章　缓解机制的数学](chapters/ch06.md)
- [第 7 章　内核攻击面](chapters/ch07.md)
- [第 8 章　浏览器与 JIT](chapters/ch08.md)
- [第 9 章　密码学的构造](chapters/ch09.md)
- [第 10 章　协议安全：TLS 1.3 与 QUIC](chapters/ch10.md)
- [第 11 章　身份与授权](chapters/ch11.md)
- [第 12 章　Web 平台的安全模型](chapters/ch12.md)
- [第 13 章　程序分析：符号执行与抽象解释](chapters/ch13.md)
- [第 14 章　模糊测试：覆盖率与变异](chapters/ch14.md)
- [第 15 章　侧信道与微架构](chapters/ch15.md)
- [第 16 章　检测的极限](chapters/ch16.md)

### 附录

- [附录 A　符号与术语](appendix/a1-notation.md)
- [附录 B　延伸阅读](appendix/a2-reading.md)

---

[返回系列首页](../../README.md)
