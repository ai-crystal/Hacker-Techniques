# -*- coding: utf-8 -*-
"""临时自检脚本（不属于产出，用完即删）。"""
import re
import sys

BAN_START = ["首先", "其次", "再次", "最后", "另外", "总之", "综上所述", "值得注意的是",
             "值得一提的是", "需要指出的是", "不难发现", "我们可以看到", "让我们",
             "众所周知", "然而", "因此"]
BAN_PHRASE = ["本章将", "本节将", "接下来我们", "下面让我们", "总而言之", "小结一下",
              "极其重要", "至关重要", "意义重大", "不可忽视", "令人震惊",
              "你可能会问", "答案是", "在……的今天", "随着"]

for path in sys.argv[1:]:
    t = open(path, encoding="utf-8").read()
    body = re.sub(r"<figcaption>.*?</figcaption>", "", t, flags=re.S)
    han = len(re.findall(r"[\u4e00-\u9fff]", t))
    print(f"\n=== {path}  汉字 {han}")
    print("二级标题:", re.findall(r"^## .*$", t, flags=re.M))
    print("全角冒号", body.count("："), "| 破折号", body.count("——"))
    print("图注:", re.findall(r"图 \d+-\d+", t))
    for w in BAN_START:
        for m in re.finditer("^" + w, body, flags=re.M):
            print("  段首禁用:", w, body[m.start():m.start() + 12].replace("\n", " "))
    for w in BAN_PHRASE:
        if w in body:
            n = body.count(w)
            print("  禁用短语:", w, n)
    for i, line in enumerate(body.splitlines(), 1):
        if len(line) > 0 and re.match(r"^[^|#<>`\s]", line) and "：" in line and line.count("：") > 2:
            print("  行内冒号过多 第%d行" % i)
