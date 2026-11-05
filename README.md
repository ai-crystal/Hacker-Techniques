# 暗门

**黑客技术与安全原理**

作者：Dr. Dezeming

<p>
<a class="download-btn" href="output/dark-gate.pdf">下载 PDF</a>
<a class="download-btn" href="book/chapters/ch01.md">从第一章开始</a>
</p>

---

## 这是一本什么样的书

你在网上冲浪的时候，有没有过一种说不上来的不安。杀毒软件弹出一堆红色警告，你分不清哪条是真的；新闻说某个漏洞影响几亿台设备，你不知道自己是不是其中之一；有人跟你讲"你的密码已经被拖库了"，你不知道该信还是该改。

这种不安大多来自信息不对称。你每天都在用计算机，却不知道它内部在做什么。

这本书想补上这一段。它从晶体管和指令讲起，一路讲到栈溢出、中间人攻击、蠕虫传播和勒索软件。不要求你学过操作系统、编译原理或者密码学，每一章需要的前置知识都会在用到之前讲清楚。

## 目录

### 第一篇　机器的内部

1. [程序是怎样跑起来的](book/chapters/ch01.md)
2. [内存的秩序](book/chapters/ch02.md)
3. [操作系统的门与锁](book/chapters/ch03.md)
4. [网络是怎样连接的](book/chapters/ch04.md)

### 第二篇　漏洞的形状

5. [漏洞是什么](book/chapters/ch05.md)
6. [越界写入](book/chapters/ch06.md)
7. [军备竞赛](book/chapters/ch07.md)
8. [时间的裂缝](book/chapters/ch08.md)
9. [信任的边界](book/chapters/ch09.md)

### 第三篇　网络战场

10. [窃听、冒充与加密](book/chapters/ch10.md)
11. [网页背后的攻防](book/chapters/ch11.md)
12. [密码的数学](book/chapters/ch12.md)

### 第四篇　恶意软件

13. [病毒与蠕虫](book/chapters/ch13.md)
14. [木马、僵尸网络与勒索软件](book/chapters/ch14.md)
15. [杀毒软件为什么像病毒](book/chapters/ch15.md)

### 第五篇　人的因素

16. [骗局的工程学](book/chapters/ch16.md)
17. [四场攻击的解剖](book/chapters/ch17.md)
18. [如何保护自己](book/chapters/ch18.md)

### 附录

- [附录 A　术语表](book/appendix/a1-glossary.md)
- [附录 B　延伸阅读](book/appendix/a2-reading.md)
- [后记](book/front/postscript.md)

## 阅读方式

- 在线阅读：本页就是入口，左侧栏按篇分组，可以直接跳到任意一章。
- 整本下载：[暗门 · PDF](output/dark-gate.pdf)，带书签目录，适合离线或打印。
- 书稿源文件在 `book/chapters/`，插图的绘图代码在 `book/code/`，图片在 `book/images/`。

## 关于内容

书中所有技术内容都停留在原理与防御层面。理解攻击是为了防守，也是为了在别人用术语吓唬你的时候能分辨出他在说什么。任何未经授权对他人系统进行探测、入侵或干扰的行为，在多数国家和地区都属于违法。

书名取自一个古老的比喻。城堡的墙上总有一道门，有人想进去，有人在守。写这本书的目的，是让你知道那道门装在哪里，锁是怎么做的，以及为什么有时候它形同虚设。
