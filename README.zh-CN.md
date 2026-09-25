# Hawkstore Publishing

简体中文 · [English](README.md)

这是 Hawkstore 生态面向作者的打包和校验工具仓库。本仓库不会包含拥有整个 Registry 权限的凭据，也不会允许桌面客户端直接推送默认分支。

## 插件包结构

```text
MyMod-1.2.0/
  manifest.json
  README.md
  CHANGELOG.md
  icon.png
  BepInEx/
    plugins/
      MyMod/
        MyMod.dll
        assets/
```

最低要求是 `manifest.json`、`README.md`，以及 `BepInEx/plugins` 下至少一个 DLL。

## 创建插件包

```bash
python tools/package_mod.py path/to/MyMod-1.2.0 --out artifacts
```

命令会进行基础规范校验、创建可复现 ZIP，并在旁边生成 SHA-256 文件。

## 计划中的在线发布流程

1. 作者通过 Steam OpenID 登录；服务端从已签名回调中取得 SteamID64，不信任手工填写的身份字段。
2. 作者连接最小权限 GitHub App，并在 Hawkstore 中上传 ZIP。
3. 服务端检查压缩包、manifest、DLL 元数据、包所有权、依赖和恶意软件扫描结果。
4. 服务端创建投稿分支和 Registry Pull Request。
5. GitHub Actions 重复执行确定性校验。
6. 新作者第一次发布需要人工审核。
7. 合并后创建不可变的 Release 资源并更新 Registry 索引。

作者提交时必须使用 `steamVerification.status: pending`。只有发布服务在确认 OpenID 身份与 `author.steamId` 一致后，才能将其提升为 `verified`。不得要求作者输入 Personal Access Token，也不得把 PAT 内置在客户端中。
