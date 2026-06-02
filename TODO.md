# 你的行动清单(Task Flow)

骨架已搭好。下面是**你现在要亲手做的事**,按顺序勾选。括号是预估耗时。
卡住任何一步就直接告诉我。

---

## 第 1 步 · 装环境(~20 分钟,只做一次)

- [ ] 安装 Quarto:<https://quarto.org/docs/get-started/>(Windows 可用 `winget install Posit.Quarto`)
- [ ] 终端验证:`quarto --version`(能打印版本号即成功)
- [ ] 安装 Python 依赖(代码块需要):`pip install jupyter numpy matplotlib`

## 第 2 步 · 跑起来看一眼(~5 分钟)

- [ ] 在博客文件夹里执行:`quarto preview`
- [ ] 浏览器会自动打开本地站点 —— 确认首页文章列表、谱定理范文里的公式和代码输出都正常显示

## 第 3 步 · 改成你自己的(~30 分钟)

- [ ] `_quarto.yml`:把所有 `Your Name`、`yourusername`、占位 URL 换成真实信息
- [ ] `about.qmd`:写你的简介、研究方向、邮箱(可放一张 `profile.jpg` 到根目录)
- [ ] 决定博客名 + 注册一个空的 GitHub 仓库(域名可选,以后再加)

## 第 4 步 · 上线(~20 分钟,只做一次)

- [ ] 把文件夹初始化为 Git 仓库并推到 GitHub:
      `git init && git add . && git commit -m "init" && git remote add origin <你的仓库地址> && git push -u origin main`
- [ ] 部署:`quarto publish gh-pages`
- [ ] 把生成的网址(`https://你的用户名.github.io/...`)填回 `_quarto.yml` 的 `site-url`,再 push 一次
- [ ] 打开网址确认线上能访问 ✅ 至此博客已正式存在

## 第 5 步 · 发出第一篇(~2–4 个专注时段)

- [ ] 从 `ideas.md` 里挑**一个你不用查资料就能讲清楚**的题目
- [ ] 复制范文起稿:`cp -r posts/spectral-theorem posts/你的slug`
- [ ] 按范文格式写(定理/证明/引用/代码),`draft: true` 期间不会公开
- [ ] 过一遍 `WORKFLOW.md` 里的"质量自查清单"
- [ ] 改成 `draft: false` → `quarto publish gh-pages` → 发布

## 第 6 步 · 形成节奏(持续)

- [ ] 定一个能坚持的频率(建议每 1–2 周一篇)
- [ ] 随手往 `ideas.md` 记选题,永远不从空白页开始
- [ ] (可选)加评论(giscus)和访问统计(Plausible/GoatCounter)

---

### 现在这一刻,只需做一件事:
👉 **第 1 步:装 Quarto。** 装完回来执行 `quarto preview`,其余按顺序推进即可。
