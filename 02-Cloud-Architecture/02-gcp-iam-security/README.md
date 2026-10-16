# 02 - 云原生架构：IAM 权限控制 (AWS & GCP)

## 💡 核心概念
*   **IAM (Identity and Access Management)**：决定了“**谁 (Who)**” 可以对“**什么资源 (Which Resource)**” 执行“**什么操作 (What Action)**”。
*   **最小权限原则 (PoLP)**：永远只赋予执行某项任务所需的*最少*权限。不要图省事直接给 `AdministratorAccess` 或 `Owner` 角色。
*   **Role (角色) vs Policy (策略)**：
    *   Policy 是一段 JSON 格式的规则说明（允许或拒绝某些动作）。
    *   Role 是一个可以被“扮演 (Assume)”的身份，你可以把 Policy 绑定给 Role，再把 Role 赋给 Lambda、EC2 或是某个具体的用户。

## 🚀 生产环境的避坑指南 (Best Practices)
1.  **避免硬编码凭证**：绝对不要在 Python 代码里写死 Access Key 和 Secret Key。正确的做法是将 IAM Role 绑定给运行代码的计算资源（如 EC2 或 Lambda），`boto3` 或 Google Cloud SDK 会自动获取临时凭证。
2.  **细粒度控制 (Fine-Grained Access)**：如果 Lambda 只需要读取 S3 的某个特定文件夹，Policy 的 Resource 不能写 `arn:aws:s3:::*`，必须精确到具体的桶和路径，如 `arn:aws:s3:::my-bucket/uploads/*`。
3.  **定期审计**：利用 AWS IAM Access Analyzer 或 GCP Policy Intelligence，定期检查哪些权限已经被赋予但长期未使用。

## 🎯 常见面试题对答技巧
**Q: 如果你需要让一个运行在 EC2 上的 Python 后端应用，能够读取特定 S3 桶里的敏感数据，你会如何设计权限？**
**A:** 
1. 首先，我**绝不会**生成长期的 Access Key 并将其写在配置文件中。
2. 我会编写一个自定义的 IAM Policy，明确只赋予 `s3:GetObject` 权限，并且将 `Resource` 严格限制为那个特定的 S3 ARN (`arn:aws:s3:::sensitive-data-bucket/*`)。
3. 然后，我创建一个 IAM Role 并附加上这个 Policy。
4. 最后，将这个 IAM Role 附加到该 EC2 实例上 (Instance Profile)。EC2 上的 Python 只要初始化原生的 `boto3.client('s3')` 即可透明地获取权限。
