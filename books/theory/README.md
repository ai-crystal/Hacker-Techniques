# 理论篇　漏洞、内存与协议的深层结构

共 147 页，PDF 4.9 MB。

为什么栈溢出能改写控制流，为什么堆上的一个字节能变成任意写，为什么加了地址随机化攻击者还能算准地址，为什么 TLS 的握手设计得这么绕。这一册不回避细节，把体系结构、可执行文件、分配器、密码学、协议和程序分析逐层拆开。

它不教你点哪个按钮。它解释那些按钮背后成立与不成立的条件，以及在什么情况下这些条件会失效。读完能自己判断一篇漏洞分析写得对不对。

[下载本册 PDF](output/theory.pdf)

## 目录


### 第一篇　机器与内存

- [第一章　指令与微架构：一条指令走了多远](books/theory/chapters/ch01.md)
- [第二章　可执行文件与加载器](books/theory/chapters/ch02.md)
- [第三章　调用约定与栈的物理结构](books/theory/chapters/ch03.md)
- [第四章　堆与分配器：malloc 的账本](books/theory/chapters/ch04.md)

### 第二篇　攻防的机制

- [第五章　利用原语：从越界到任意读写](books/theory/chapters/ch05.md)
- [第六章　缓解机制的数学](books/theory/chapters/ch06.md)
- [第七章　内核攻击面](books/theory/chapters/ch07.md)
- [第八章　浏览器与 JIT](books/theory/chapters/ch08.md)

### 第三篇　协议与密码

- [第九章　密码学的构造](books/theory/chapters/ch09.md)
- [第十章　协议安全：TLS 1.3 与 QUIC](books/theory/chapters/ch10.md)
- [第十一章　身份与授权](books/theory/chapters/ch11.md)
- [第十二章　Web 平台的安全模型](books/theory/chapters/ch12.md)

### 第四篇　分析与检测

- [第十三章　程序分析：符号执行与抽象解释](books/theory/chapters/ch13.md)
- [第十四章　模糊测试：覆盖率与变异](books/theory/chapters/ch14.md)
- [第十五章　侧信道与微架构](books/theory/chapters/ch15.md)
- [第十六章　检测的极限](books/theory/chapters/ch16.md)

- [后记](books/theory/front/postscript.md)
- [附录 A　符号与术语](books/theory/appendix/a1-notation.md)
- [附录 B　延伸阅读](books/theory/appendix/a2-reading.md)
