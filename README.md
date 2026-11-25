# 黑客技术与安全原理

一套讲攻防原理的中文技术书，共三册。每一册都能单独读，合起来是一条从概念到动手的路径。

在线阅读：<https://ai-crystal.github.io/Hacker-Techniques/>　·　仓库：<https://github.com/ai-crystal/Hacker-Techniques>

| 册 | 内容 | 页数 | 阅读 | 下载 |
| --- | --- | --- | --- | --- |
| 入门篇 | 从病毒史到攻防全景 | 199 | [在线阅读](books/beginner/README.md) | <a class="pdf-link" href="output/beginner.pdf" target="_blank" rel="noopener">PDF</a> |
| 理论篇 | 漏洞、内存与协议的深层结构 | 147 | [在线阅读](books/theory/README.md) | <a class="pdf-link" href="output/theory.pdf" target="_blank" rel="noopener">PDF</a> |
| 实战篇 | 从靶场到真实对抗 | 192 | [在线阅读](books/practice/README.md) | <a class="pdf-link" href="output/practice.pdf" target="_blank" rel="noopener">PDF</a> |

## 三册的分工

入门篇讲全貌。从 1971 年第一只会自我复制的程序讲到今天的勒索产业，再把机器、内存、网络、漏洞、恶意软件、人的因素逐层铺开。读完知道这个领域长什么样，遇到新闻能判断危险发生在哪一层。

理论篇讲为什么。指令怎么编码，堆分配器怎么记账，一个越界写怎样变成任意读写，TLS 1.3 的握手为什么这样设计，检测为什么在数学上就有天花板。读完能自己判断一篇漏洞分析写得对不对。

实战篇讲怎么做。在自己的虚拟机里搭靶场，从侦察、验证、利用、提权、横向一路做到样本分析和应急响应。每一步都要求能解释清楚为什么这样做。

## 怎么读

刚入门从第一册读起；已经能写代码、想弄清楚机制的直接读第二册；需要动手的从第三册开始，遇到不懂的概念再回去查。

三册的实验环境、术语与例子保持统一，跨册阅读不需要重新适应。
