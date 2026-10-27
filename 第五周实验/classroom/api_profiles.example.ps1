# 复制一个配置块到当前 PowerShell 会话，再运行生成脚本。
# Chat Completions 是一种 HTTP API 请求格式。
# generate_sft_data.py 使用 requests 发送同样格式的 JSON 请求。

# 1. 阿里云百炼（课堂使用：DeepSeek-V4-Flash-0731）
# 控制台：https://bailian.console.aliyun.com/
# 创建 API Key 后，把弹窗中的 WorkspaceId 和完整 Key 填到下方。
$env:COMMERCIAL_API_URL = "https://<WorkspaceId>.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions"
$env:COMMERCIAL_API_KEY = "在此粘贴你自己的百炼通用API Key"
$env:COMMERCIAL_API_MODEL = "deepseek-v4-flash-0731"
# 百炼使用 enable_thinking 开关；high 由生成命令的 --reasoning-effort 指定。
$env:COMMERCIAL_API_EXTRA_JSON = '{"enable_thinking":true}'

# 2. OpenAI 官方
# 控制台：https://platform.openai.com/
# $env:COMMERCIAL_API_URL = "https://api.openai.com/v1/chat/completions"
# $env:COMMERCIAL_API_KEY = "你的OpenAI API Key"
# $env:COMMERCIAL_API_MODEL = "账户模型列表中的实际名称"
# $env:COMMERCIAL_API_EXTRA_JSON = "{}"

# 3. HanheGufei 中转站
# 控制台：https://panel.hanhegufei.online/dashboard
# 登录后依次确认：余额/充值、API Keys、可用模型列表、API文档中的Base URL。
# $env:COMMERCIAL_API_URL = "https://面板文档给出的地址/v1/chat/completions"
# $env:COMMERCIAL_API_KEY = "你的中转站Key"
# $env:COMMERCIAL_API_MODEL = "面板模型列表中的实际名称"
# $env:COMMERCIAL_API_EXTRA_JSON = "{}"
