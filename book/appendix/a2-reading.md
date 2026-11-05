# 附录 B　延伸阅读

书里的每一章都建立在一些公开的材料上。下面这份清单按主题排列，都是可以直接找到原文的，读完之后对相应章节的理解会扎实很多。

## B.1 原始论文与技术报告

- Aleph One, *Smashing The Stack For Fun And Profit*, Phrack 49, 1996。缓冲区溢出的经典入门文本，讲法比大多数教材直接。
- Eugene Spafford, *The Internet Worm Program: An Analysis*, 1988。Morris 蠕虫的第一份系统分析，也是应急响应的起点。
- Ken Thompson, *Reflections on Trusting Trust*, 1984。八页，讲清楚了"编译器可以被植入后门"这件事为什么无法用读代码来解决。
- Jerome Saltzer, Michael Schroeder, *The Protection of Information in Computer Systems*, 1975。最小权限、完全中介等设计原则的出处，今天读仍然有效。
- Crispin Cowan 等, *StackGuard: Automatic Adaptive Detection and Prevention of Buffer-Overflow Attacks*, USENIX Security 1998。
- Hovav Shacham, *The Geometry of Innocent Flesh on the Bone*, CCS 2007。ROP 的系统化表述。
- Hovav Shacham 等, *On the Effectiveness of Address-Space Randomization*, CCS 2004。用数据说明 32 位系统上的随机化有多容易被暴力破解。
- Paul Kocher 等, *Spectre Attacks: Exploiting Speculative Execution*, IEEE S&P 2019。
- Moritz Lipp 等, *Meltdown: Reading Kernel Memory from User Space*, USENIX Security 2018。
- David Moore 等, *Inside the Slammer Worm*, IEEE Security & Privacy, 2003。蠕虫传播速度的经典测量。
- Stuart Staniford, Vern Paxson, Nicholas Weaver, *How to 0wn the Internet in Your Spare Time*, USENIX Security 2002。
- Niels Provos, David Mazières, *A Future-Adaptable Password Scheme*, USENIX 1999。bcrypt 的原始论文。
- Steven Bellovin, *Security Problems in the TCP/IP Protocol Suite*, 1989。协议设计缺陷的经典梳理。
- Zulfikar Ramzan 等关于钓鱼的实证研究，以及 Rachna Dhamija, J. D. Tygar, Marti Hearst, *Why Phishing Works*, CHI 2006。
- Brett Stone-Gross 等, *Your Botnet is My Botnet*, CCS 2009。Torpig 僵尸网络的接管过程。
- Robin Sommer, Vern Paxson, *Outside the Closed World: On Using Machine Learning for Network Intrusion Detection*, IEEE S&P 2010。基率谬误与检测上限。
- Ralph Langner, *To Kill a Centrifuge*, 2013。Stuxnet 的技术解剖。
- Zakir Durumeric 等, *The Matter of Heartbleed*, IMC 2014。漏洞披露之后世界上到底发生了什么。

## B.2 书

- Ross Anderson, *Security Engineering*。覆盖面最广的一本，第三版可以在作者主页免费读到。
- Jon Erickson, *Hacking: The Art of Exploitation*。从 C 和汇编讲到溢出与利用，配套的虚拟机环境很适合动手。
- Bryant, O'Hallaron, *Computer Systems: A Programmer's Perspective*。第一章到第九章把本书第一篇的内容讲得更深。
- Bruce Schneier, *Secrets and Lies*。谈的是安全的经济学与心理学，不涉及代码。
- Kevin Mitnick, *The Art of Deception*。社会工程的案例集，读起来像故事。

## B.3 可以合法练手的地方

- CTF 赛事与公开题库，比如 picoCTF、OverTheWire。题目环境是专门搭的，打坏了不心疼。
- 各厂商提供的漏洞靶场，例如 OWASP 的 Juice Shop、DVWA，本地起一个容器就能用。
- 各大项目的漏洞赏金计划。这些项目明确授权安全研究者在范围内测试，是最接近真实工作的练习。
- 自己搭虚拟机做实验环境的习惯，比任何教程都重要。快照、回滚、隔离网络，这套流程本身就是安全工程的一部分。
