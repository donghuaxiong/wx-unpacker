# wx-unpacker-skill

一个用于微信小程序和微信小游戏包处理的 Codex Skill。

它只负责一件事：根据目标 AppID 找到已获授权的 `wxapkg`，完成必要的解密、解包、主包/分包重建和入口修复，使结果能够导入微信开发者工具并启动。

```text
目标 AppID
→ 定位并复制缓存包
→ 校验原包
→ 必要时解密 V1MMWX
→ 解包主包和分包
→ 重建目录与启动入口
→ 导入微信开发者工具验证启动
```

本 Skill 不负责解包后的业务功能修改。详细工作规范见 [SKILL.md](SKILL.md)。

## 如何查看 AppID

AppID 通常以 `wx` 开头。优先使用下面几种方式确认，不要只根据包目录名猜测。

### 方法一：微信公众平台

如果你是该小程序或小游戏的管理员，登录[微信公众平台](https://mp.weixin.qq.com/)，在开发设置或开发者 ID 页面查看 AppID。后台菜单名称可能随平台版本调整。

### 方法二：已有开发者工具工程

打开工程根目录的 `project.config.json`，查找：

```json
{
  "appid": "wx1234567890abcdef"
}
```

也可以在微信开发者工具的项目详情或基本信息中查看当前项目 AppID。

### 方法三：微信客户端

打开目标小程序或小游戏，点击右上角菜单，进入“关于”或“更多资料”页面。部分微信版本会显示或允许复制 AppID；如果没有显示，请使用公众平台或开发者工具确认。

拿到 AppID 后，建议同时记录目标名称、类型以及你拥有的授权范围，避免处理错误的缓存包。

## 一句话让 AI 解包

安装本 Skill 后，把下面的 AppID 替换为目标值，直接对支持本地文件操作的 Codex 说：

```text
使用 $wx-unpacker-skill，根据 AppID wx1234567890abcdef 在这台电脑上定位我有权处理的微信小程序或小游戏缓存包；先复制原包并记录 SHA-256，不要修改微信缓存中的原文件；然后识别是否为 V1MMWX、完成解密，解出主包和所有相关分包，重建为可导入微信开发者工具并能启动的工程；最后告诉我原包、解包目录、工程目录和验证结果。
```

如果已经有 `.wxapkg` 文件，可以说：

```text
使用 $wx-unpacker-skill，解包这个我有权处理的 wxapkg；保留原文件，自动判断是否需要 V1MMWX 解密，重建主包和分包，并验证结果能否导入微信开发者工具启动。
```

## 一句话安装

对支持 GitHub 和本地文件操作的 Codex 说：

```text
请从 https://github.com/donghuaxiong/wx-unpacker.git 安装 Codex Skill wx-unpacker-skill 到当前用户的默认 skills 目录；不要覆盖已有同名目录；安装后验证 SKILL.md、scripts 和 references 是否完整，并告诉我如何调用。
```

默认安装位置通常是：

```text
${CODEX_HOME}/skills/wx-unpacker-skill
```

未设置 `CODEX_HOME` 时通常为：

```text
~/.codex/skills/wx-unpacker-skill
```

## 手动安装

直接克隆：

```bash
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"
mkdir -p "$CODEX_SKILLS_DIR"
git clone https://github.com/donghuaxiong/wx-unpacker.git \
  "$CODEX_SKILLS_DIR/wx-unpacker-skill"
```

如果你正在本地开发这个 Skill，可以使用软连接。把示例源路径替换为当前电脑的真实绝对路径：

```bash
SKILL_SOURCE="/absolute/path/to/wx-unpacker-skill"
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$CODEX_SKILLS_DIR"
test -f "$SKILL_SOURCE/SKILL.md"
test ! -e "$CODEX_SKILLS_DIR/wx-unpacker-skill"
ln -s "$SKILL_SOURCE" "$CODEX_SKILLS_DIR/wx-unpacker-skill"
```

软连接只能指向当前电脑真实存在的路径，不能照搬其他人的 `/Users/用户名/...` 路径。

安装或更新后，重新启动 Codex 或刷新 Skill 列表，然后使用：

```text
$wx-unpacker-skill
```

## 环境要求

- Node.js
- Python 3.9+
- 微信开发者工具
- 一个与目标包兼容的 wxapkg 解包器
- `rg`，推荐但不是硬依赖

本 Skill 可以调用外部 `qwerty472123/wxappUnpacker`，但不包含其源码。该外部工具使用 GPL-3.0-or-later，仍受其自身许可证约束。

## 自带脚本

```text
scripts/decrypt_wxapkg.js   解密 V1MMWX 包
scripts/inspect_project.py  识别包类型和工程结构
scripts/validate_project.py 检查 JSON、JS、入口和预览目录
```

解密示例：

```bash
node scripts/decrypt_wxapkg.js \
  --appid wx1234567890abcdef \
  --input /path/to/input.wxapkg \
  --output /path/to/output.wxapkg
```

检查重建工程：

```bash
python3 scripts/inspect_project.py /path/to/project --strict
python3 scripts/validate_project.py /path/to/project
```

## 合格输出

一次完整处理至少应给出：

- 目标 AppID
- 原包复制位置和 SHA-256
- 是否进行了 V1MMWX 解密
- 使用的解包器及版本
- 主包和分包关系
- 解包原始目录
- 可导入微信开发者工具的工程目录
- 是否通过静态检查和基础启动验证
- 尚未解决的导入、模块或资源错误

## 常见问题

### AppID 错误或解密失败

重新确认 AppID，不要用当前调试项目的 AppID 代替原包 AppID。确认文件完整，并检查它是否真的是 `V1MMWX` 包。

### 分包提示需要主包目录

先解主包，再把主包的原始解包目录作为上下文处理分包。不要把多个包按同名文件直接覆盖合并。

### `module ... is not defined`

从报错调用方计算模块 ID，检查物理文件和虚拟模块注册名。不要全局替换 `__plugin__` 字符串。

### 真机预览提示非法目录

检查是否存在以双下划线开头和结尾的实体目录。虚拟模块 ID 与实体目录不是同一概念。

## 项目结构

```text
wx-unpacker-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
├── scripts/
└── references/
```

## 使用边界与免责声明

仅处理你拥有或已经得到明确授权的小程序、小游戏和软件包。不得使用本项目绕过支付、授权、账号权限、访问控制或其他安全措施，也不得获取、修改或传播他人的凭证、数据及受保护内容。

使用者应自行确认授权范围，并自行承担违法、违规、侵权或超出授权使用所造成的后果。本项目按“现状”提供；在适用法律允许的最大范围内，作者和版权持有人不对因本项目或其使用产生的索赔、损害或其他责任负责。

## License

[MIT License](LICENSE) © 2026 Jason。允许使用、复制、修改、分发和商业使用，但必须保留 MIT 许可证要求的版权及许可声明。第三方工具继续适用各自许可证。
