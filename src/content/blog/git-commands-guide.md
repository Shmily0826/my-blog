---
title: 'Git命令'
description: '记录常用Git命令'
pubDate: 'Mar 27 2026'
heroImage: '../../assets/posts/blog-placeholder-1.jpg'

---

# 常用的git命令

## 🎯 每日必用
### 1.提交
~~~
# 查看状态（使用最频繁）
git status

# 添加文件到暂存区
git add <文件名>          # 添加单个文件
git add .                # 添加所有修改（最常用）

# 提交更改
git commit -m "提交说明"
git commit -am "说明"     # 一次性添加(已跟踪文件)并提交
~~~

### 2.推送和拉取
~~~
# 推送到远程仓库
git push origin main
git push -u origin main  # 首次推送建立跟踪

# 从远程拉取更新
git pull origin main     # 拉取并合并
git fetch origin         # 只下载不合并
~~~

### 3.分支操作
~~~
# 创建并切换分支（高频命令）
git checkout -b feature/new-feature

# 查看分支
git branch              # 本地分支
git branch -a           # 所有分支

# 切换分支
git checkout main
git switch main         # Git 2.23+ 新命令

# 合并分支
git merge feature/new-feature
~~~

## 📁 仓库管理
~~~
# 克隆仓库
git clone <仓库URL>

# 初始化新仓库
git init

# 查看远程仓库
git remote -v
~~~

## 🔍 查看与比较

~~~
# 查看提交历史
git log                 # 详细历史
git log --oneline      # 单行简洁版
git log --graph        # 图形化显示分支

# 比较差异
git diff                # 工作区与暂存区差异
git diff --staged       # 暂存区与上一次提交差异
~~~

## ⏪ 撤销与恢复
~~~
# 撤销工作区修改（危险！）
git checkout -- <文件名>  # 丢弃单个文件修改
git restore <文件名>      # Git 2.23+ 新方式

# 撤销暂存（取消git add）
git restore --staged <文件名>
git reset HEAD <文件名>    # 旧方法

# 撤销提交
git reset --soft HEAD~1  # 撤销提交但保留修改
git reset --mixed HEAD~1 # 撤销提交和暂存
git reset --hard HEAD~1  # 彻底丢弃提交（谨慎！）
~~~

## 📦 实用组合命令
~~~
# 日常开发三连
git add .
git commit -m "更新功能"
git push

# 创建功能分支并推送到远程
git checkout -b feature/xxx
# 开发完成后...
git push -u origin feature/xxx

# 更新代码（先拉后推）
git pull origin main
# 解决冲突后...
git push origin main
~~~

## 🆘 紧急救援
~~~
# 查看所有操作记录
git reflog

# 恢复误删分支
git checkout -b 分支名 commit哈希

# 找回丢失的提交
git fsck --lost-found
~~~

## ⚠️ 危险命令（谨慎使用）
~~~
# 强制推送（覆盖远程历史）
git push -f origin main

# 强制删除未合并分支
git branch -D 分支名

# 彻底清理未跟踪文件
git clean -fd
~~~

## 📋 快速参考表

| 场景               | 命令                                       |
| ------------------ | ------------------------------------------ |
| **开始新功能**     | `git checkout -b feature/xxx`              |
| **保存当前工作**   | `git add . && git commit -m "保存点"`      |
| **同步远程代码**   | `git pull origin main`                     |
| **上传代码**       | `git push origin feature/xxx`              |
| **查看状态**       | `git status`                               |
| **查看历史**       | `git log --oneline -5`（最近5条）          |
| **撤销未提交修改** | `git checkout -- 文件名`                   |
| **创建发布版本**   | `git tag v1.0.0 && git push origin --tags` |

