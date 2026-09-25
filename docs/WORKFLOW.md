# Publishing workflow / 发布工作流

## English

The first public version uses pull requests as the audit trail. Upload through the desktop app is intentionally postponed until a GitHub App and server-side validation worker exist. The future worker will have only Contents and Pull Requests permissions required for its repository scope.

Published versions are immutable: changing a binary requires a new semantic version. Package ownership is stored as GitHub login names in the registry manifest and checked before updates are accepted.

## 简体中文

第一版使用 Pull Request 作为审核记录。在 GitHub App 和服务端校验 Worker 完成之前，桌面端不会开放直接上传。未来 Worker 仅申请目标仓库所需的 Contents 和 Pull Requests 权限。

已发布版本不可修改；更改二进制文件必须发布新的语义化版本。包所有权以 GitHub 登录名保存在 Registry manifest 中，接受更新前必须核对所有权。
