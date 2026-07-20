# wx-unpacker-skill

面向授权场景的微信小程序与微信小游戏逆向、工程重建和本地调试技能包。

它解决的不是单纯“把 wxapkg 解压出来”，而是完整处理：

```text
定位缓存包
→ 保留与校验原包
→ V1MMWX 解密
→ wxapkg 解包
→ 主包/分包/插件重建
→ 普通小程序或小游戏分类
→ 启动链与模块路径修复
→ 微信开发者工具运行验证
→ 真机预览检查
```

## 使用边界

仅用于你拥有或明确获准检查、修改的软件，例如：

- 自有小程序/小游戏的源码丢失恢复
- 获得客户授权的兼容性排查
- 内部安全研究与离线调试
- 已下线服务的本地演示恢复
- 广告、登录、后端依赖的授权本地替换

不要用于绕过支付、账号权限、访问控制、授权机制，或获取其他用户的凭证、存档和受保护数据。

## 许可、使用限制与免责声明

本项目采用 [MIT License](LICENSE) 发布。你可以在遵守 MIT License、适用法律、平台规则、目标软件许可协议及第三方权利的前提下使用、复制、修改、分发和商业使用本项目。使用者只能分析自己拥有的软件，或已经取得权利人明确授权的软件。

严禁将本项目用于任何违反法律法规、平台规则、软件许可协议或第三方合法权益的活动，包括但不限于：

- 未经授权获取、解包、修改、复制或传播他人的小程序、小游戏及其资源
- 绕过支付、账号权限、访问控制、授权验证、反作弊或其他安全措施
- 获取、篡改或传播他人的账号、凭证、个人信息、存档及受保护数据
- 制作、运营、销售或传播侵权版本、破解版本、作弊工具或其他非法衍生物

下载、安装、复制、修改、运行或传播本项目，即表示使用者已经理解并同意：

1. 使用者应自行确认其行为已经获得充分授权，并自行承担因使用本项目产生的全部风险和责任。
2. 因使用者违法、违规、侵权、违反平台规则或超出授权范围使用本项目而引起的投诉、封号、数据损失、设备损坏、经济损失、行政责任、民事责任或刑事责任，均由使用者自行承担。
3. 作者及贡献者不参与、不鼓励也不支持任何未经授权或违法用途；对于使用者的具体使用方式及其直接或间接后果，作者及贡献者不承担责任，但适用法律另有强制性规定的除外。
4. 本项目按“现状”提供，不对完整性、准确性、可用性、适销性、特定用途适用性、持续维护或不侵害第三方权利作出任何明示或默示保证。
5. 本项目引用或调用的第三方工具、代码和资料仍分别受其原有许可证及使用条款约束；本免责声明不会替代或改变第三方许可证。

如果你不能确认目标软件的权属、授权范围或当地法律是否允许相关行为，请不要使用本项目，并应先咨询具备资质的法律专业人士。

MIT License 中的免责声明是本项目授权条款的一部分：本项目按“现状”提供，在适用法律允许的最大范围内，作者或版权持有人不对因本项目或其使用产生的索赔、损害或其他责任负责。README 中的中文说明用于帮助理解；如与 `LICENSE` 正文存在差异，以 `LICENSE` 为准。

## 与 wxappUnpacker 的关系

本 skill 不等于 wxappUnpacker，也不把 wxappUnpacker 源码打包进来。

- `wxappUnpacker`：负责从明文 wxapkg 提取和尝试还原文件。
- `decrypt_wxapkg.js`：负责本 skill 内的 `V1MMWX` 解密。
- `wx-unpacker-skill`：负责选择工具、重建工程、修复运行时、替换服务契约并完成验证闭环。

因此：

```text
wxappUnpacker = 解包工具
wx-unpacker-skill = 完整逆向与恢复方法
```

## 目录结构

```text
wx-unpacker-skill/
├── SKILL.md
├── README.md
├── LICENSE
├── agents/
│   └── openai.yaml
├── scripts/
│   ├── decrypt_wxapkg.js
│   ├── inspect_project.py
│   └── validate_project.py
└── references/
    ├── unpacking.md
    ├── mini-program.md
    ├── mini-game.md
    ├── cocos.md
    ├── service-boundaries.md
    ├── verification.md
    └── troubleshooting.md
```

## 环境要求

基础工具：

- macOS、Linux 或 Windows
- Node.js，建议保留一个与所选解包器兼容的版本
- Python 3.9+
- 微信开发者工具
- `rg`（ripgrep），推荐但不是脚本硬依赖
- 一个兼容目标包的 wxapkg 解包器

当前已验证过的外部解包器类型：

- `qwerty472123/wxappUnpacker`
- 其 `package.json` 名称为 `wxapp-unpacker`
- 许可证为 GPL-3.0-or-later，因此本 skill 不复制其源码

老版本 wxappUnpacker 依赖较旧的 `vm2`、`cheerio` 等库。不要随意升级依赖后就认为输出仍等价，建议记录：

- Git commit
- `package-lock.json`
- Node.js 版本
- 实际执行命令

## 安装为 Codex Skill

### 安装前提

Skill 目录必须完整包含：

```text
wx-unpacker-skill/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
└── references/
```

Codex 默认从以下目录发现个人 skills：

```text
${CODEX_HOME}/skills/
```

如果没有设置 `CODEX_HOME`，通常使用：

```text
~/.codex/skills/
```

安装完成后的目标结构必须是：

```text
<Codex skills 目录>/wx-unpacker-skill/SKILL.md
```

不能多嵌套一层，例如下面这种结构通常无法正确发现：

```text
<Codex skills 目录>/wx-unpacker-skill/wx-unpacker-skill/SKILL.md
```

### 用一句话让 AI 安装（推荐）

要让其他电脑上的用户通过一句话安装，必须先把这个 skill 发布到用户或 AI 可以访问的位置，例如：

- GitHub、GitLab、Gitee 等 Git 仓库
- 用户可访问的私有仓库
- 对话中上传的 ZIP 压缩包
- 本机已经存在的完整 skill 目录

当前电脑上的绝对路径不能被其他电脑直接访问。公开分发前，应把本目录作为仓库根目录发布，并取得真实仓库 URL。

用户只需要把下面的 `<SKILL_REPOSITORY_URL>` 换成真实地址，然后对支持本地文件操作的 AI 说一句：

```text
请从 <SKILL_REPOSITORY_URL> 安装 Codex skill `wx-unpacker-skill` 到当前用户的默认 Codex skills 目录；安装前检查仓库根目录存在 SKILL.md，不要覆盖已有同名目录，安装后验证 YAML frontmatter、scripts 和 references 完整，并告诉我是否需要重启以及如何用 `$wx-unpacker-skill` 调用。
```

例如仓库发布后，可以写成：

```text
请从 https://github.com/example/wx-unpacker-skill 安装 Codex skill `wx-unpacker-skill`，验证成功后告诉我怎么调用。
```

如果用户直接上传了 ZIP，可以说：

```text
请把我上传的 wx-unpacker-skill 压缩包安全解压到当前用户的默认 Codex skills 目录，确保 SKILL.md 位于 wx-unpacker-skill 根目录，验证结构后告诉我如何调用；如果已经存在同名 skill，请先停止并询问我，不要覆盖。
```

如果仓库是私有的，AI 必须已经具备该仓库的合法访问权限。不要把访问令牌直接写进聊天、URL、README 或安装命令。

### 从 Git 仓库手动安装

以下示例假定 Git 仓库根目录就是本 skill 根目录。先设置实际仓库地址：

```bash
SKILL_REPOSITORY_URL="https://github.com/example/wx-unpacker-skill.git"
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$CODEX_SKILLS_DIR"
git clone "$SKILL_REPOSITORY_URL" "$CODEX_SKILLS_DIR/wx-unpacker-skill"
```

如果目标目录已经存在，不要直接覆盖。先检查它是旧版本、软连接还是用户自己的修改。

安装后验证：

```bash
test -f "$CODEX_SKILLS_DIR/wx-unpacker-skill/SKILL.md"
test -d "$CODEX_SKILLS_DIR/wx-unpacker-skill/scripts"
test -d "$CODEX_SKILLS_DIR/wx-unpacker-skill/references"
```

### 本地开发目录使用软连接

如果 skill 已经存在于当前电脑的某个开发目录，推荐创建软连接。这样修改开发目录后，Codex 使用的也是最新内容。

下面是通用示例；请把 `/absolute/path/to/wx-unpacker-skill` 替换为当前电脑上的真实绝对路径：

```bash
SKILL_SOURCE="/absolute/path/to/wx-unpacker-skill"
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$CODEX_SKILLS_DIR"
ln -s "$SKILL_SOURCE" "$CODEX_SKILLS_DIR/wx-unpacker-skill"
```

创建前建议检查：

```bash
test -f "$SKILL_SOURCE/SKILL.md"
test ! -e "$CODEX_SKILLS_DIR/wx-unpacker-skill"
```

检查软连接是否正确：

```bash
ls -ld "$CODEX_SKILLS_DIR/wx-unpacker-skill"
test -f "$CODEX_SKILLS_DIR/wx-unpacker-skill/SKILL.md"
```

注意：软连接只能指向当前电脑真实存在的目录。把某台电脑的 `/Users/某个用户名/...` 路径复制给其他用户通常无效。

### 复制安装

如果不希望使用软连接，可以复制整个目录：

```bash
SKILL_SOURCE="/absolute/path/to/wx-unpacker-skill"
CODEX_SKILLS_DIR="${CODEX_HOME:-$HOME/.codex}/skills"

mkdir -p "$CODEX_SKILLS_DIR"
cp -R "$SKILL_SOURCE" "$CODEX_SKILLS_DIR/wx-unpacker-skill"
```

复制安装不会自动同步后续更新。升级时应先比较本地修改，不要直接删除或覆盖未知内容。

### Windows PowerShell 示例

复制安装：

```powershell
$SkillSource = "C:\absolute\path\to\wx-unpacker-skill"
$CodexRoot = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$SkillsDir = Join-Path $CodexRoot "skills"
$Target = Join-Path $SkillsDir "wx-unpacker-skill"

New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null
Copy-Item -Recurse -Path $SkillSource -Destination $Target
Test-Path (Join-Path $Target "SKILL.md")
```

Windows 创建符号链接可能需要开发者模式或管理员权限。如果不确定，优先使用复制安装。

### 安装完成后的验证

确认以下文件都能访问：

```text
wx-unpacker-skill/SKILL.md
wx-unpacker-skill/agents/openai.yaml
wx-unpacker-skill/scripts/decrypt_wxapkg.js
wx-unpacker-skill/scripts/inspect_project.py
wx-unpacker-skill/scripts/validate_project.py
```

如果当前 Codex 安装中带有 skill 校验器，可以运行：

```bash
python3 <skill-creator目录>/scripts/quick_validate.py \
  "${CODEX_HOME:-$HOME/.codex}/skills/wx-unpacker-skill"
```

没有校验器时，至少确认：

- `SKILL.md` 顶部 YAML 包含 `name` 和 `description`
- `name` 为 `wx-unpacker-skill`
- `agents/openai.yaml` 中的默认提示引用 `$wx-unpacker-skill`
- 三个脚本通过 Python/Node 语法检查
- `references/` 文件完整

安装或更新 skill 后，重新启动 Codex 或刷新技能列表。然后可直接使用：

```text
$wx-unpacker-skill
```

如果 Codex 没有自动触发，可以在请求中明确写出 skill 名称。

### 调用示例

示例请求：

```text
使用 $wx-unpacker-skill，根据 AppID 定位我有权限调试的小程序包，解包并恢复成可导入微信开发者工具的工程。
```

```text
使用 $wx-unpacker-skill，检查这个 Cocos 微信小游戏为什么导入后提示 module __plugin__ is not defined。
```

```text
使用 $wx-unpacker-skill，把这个已获授权的小程序登录和接口替换成本地 mock，并验证页面跳转和刷新保存。
```

## 推荐案例目录

每个目标建立独立案例目录：

```text
cases/<appid>/<timestamp>/
├── original/
├── decrypted/
├── raw/
├── project/
├── hashes.sha256
└── NOTES.md
```

含义：

- `original/`：从微信缓存复制出的原始加密包，只读保存。
- `decrypted/`：解密后的 wxapkg。
- `raw/`：解包器的原始输出，不直接修改。
- `project/`：导入微信开发者工具的工作工程。
- `hashes.sha256`：源包 SHA-256。
- `NOTES.md`：AppID、工具版本、主包/分包关系、修改和验证记录。

## 快速开始

以下命令使用 `SKILL_DIR` 表示本 skill 在当前电脑上的实际目录。先根据自己的安装位置设置：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/wx-unpacker-skill"
test -f "$SKILL_DIR/SKILL.md"
```

如果使用的是尚未安装的本地开发副本，则把 `SKILL_DIR` 改成该副本的绝对路径。

### 1. 保存原包并计算哈希

```bash
mkdir -p cases/wx123/2026-01-01/original
cp /path/from/wechat/cache/*.wxapkg cases/wx123/2026-01-01/original/
cd cases/wx123/2026-01-01
shasum -a 256 original/*.wxapkg > hashes.sha256
```

不要直接对微信缓存文件进行修改。

### 2. 检查包头

```bash
xxd -l 32 original/package.wxapkg
```

常见情况：

- 开头为 `V1MMWX`：需要先解密。
- 第 0 字节为 `BE`，第 13 字节为 `ED`：通常已经是明文 wxapkg。

### 3. 解密 V1MMWX

```bash
node "$SKILL_DIR/scripts/decrypt_wxapkg.js" \
  --appid wx1234567890abcdef \
  --input original/package.wxapkg \
  --output decrypted/package.wxapkg
```

脚本特性：

- 要求明确提供 AppID、输入和输出路径
- 禁止输入输出使用同一文件
- 默认禁止覆盖已有输出
- 解密后校验 wxapkg 魔数
- AppID 错误时返回非零退出码

如果明确需要替换输出：

```bash
node scripts/decrypt_wxapkg.js \
  --appid wx1234567890abcdef \
  --input original/package.wxapkg \
  --output decrypted/package.wxapkg \
  --force
```

### 4. 使用 wxappUnpacker 解包

以下命令在外部 `wxappUnpacker` 目录中执行：

```bash
npm install
node wuWxapkg.js -d /absolute/path/decrypted/main.wxapkg
```

如果自动转换失败，保留原始提取结果：

```bash
node wuWxapkg.js -o /absolute/path/decrypted/main.wxapkg
```

分包通常需要主包上下文：

```bash
node wuWxapkg.js \
  -s=/absolute/path/raw/main \
  /absolute/path/decrypted/subpackage.wxapkg
```

先解主包，再解分包。不要把多个包按同名文件直接覆盖合并。

### 5. 检查重建工程

```bash
python3 "$SKILL_DIR/scripts/inspect_project.py" \
  /absolute/path/project
```

JSON 输出：

```bash
python3 scripts/inspect_project.py /absolute/path/project --json
```

严格模式发现错误时返回非零：

```bash
python3 scripts/inspect_project.py /absolute/path/project --strict
```

检查内容包括：

- 普通小程序/小游戏分类
- AppID、入口和 manifest
- 页面数、分包和插件声明
- Cocos/Laya/Egret 特征
- 缺失的分包根目录
- 入口文件中缺失的相对 `require()`
- 重复分包嵌套
- 真机预览禁止的 `__...__` 实体目录

### 6. 上传前静态验证

```bash
python3 "$SKILL_DIR/scripts/validate_project.py" \
  /absolute/path/project
```

默认检查：

- 所有 JSON 是否可解析
- JavaScript 是否通过 `node --check`
- 是否存在入口和 manifest
- 是否存在微信预览保留目录
- 是否缺少 `project.config.json`

特别大的生成文件默认允许到 16 MB。可以调整：

```bash
python3 scripts/validate_project.py /path/project --max-js-mb 32
```

只检查 JSON、结构和目录：

```bash
python3 scripts/validate_project.py /path/project --skip-js
```

## 普通微信小程序流程

普通小程序优先检查：

```text
app.json
app.js
app.wxss
pages/
components/
workers/
miniprogram_npm/
```

每个页面重点确认：

```text
页面路由
页面 JS
页面 JSON
WXML
WXSS
usingComponents
```

如果原项目由 uni-app、Taro、WePY 等框架构建，解包结果通常是微信编译后的运行代码，不代表能恢复成原始 Vue、React 或 TypeScript 工程。优先目标应是恢复可运行的小程序工程。

普通小程序常见线上边界：

- 登录和 session 交换
- HTTP 请求
- 云开发
- 上传下载
- 地图、位置、蓝牙、相机
- 订阅消息
- 支付
- 广告与统计

云函数和数据库通常不在客户端包中，需要根据已授权的接口契约建立本地 mock。

## 微信小游戏流程

小游戏优先检查：

```text
game.js
game.json
主包与独立分包
游戏引擎
资源 Bundle
插件缓存
本地存档
开放数据域
```

小游戏“能显示首页”不等于恢复完成。至少还要测试：

- 点击和触摸
- 人物移动或拖动
- 场景切换
- 一次战斗或核心操作
- 一次奖励流程
- 保存与重载

统计 SDK 或插件方法缺失也可能中断触摸事件，因此不要看到“人物不能移动”就直接修改移动算法。

## Cocos 小游戏注意事项

Cocos 常见启动链：

```text
game.js
→ adapter/bootstrap
→ Cocos 引擎或插件 bundle
→ ccRequire
→ settings
→ main
→ window.boot()
```

最容易混淆的是两类 `__plugin__`：

- JavaScript 里的 `__plugin__/appid/module.js` 可能是虚拟模块 ID，不能随意删除。
- 文件系统中的 `__plugin__` 目录可能被真机预览判定为保留目录，必须迁移。

迁移包装文件后，`require()` 的相对基准也会改变，必须重新计算最终模块 ID。

## 本地模式设计

所有替换集中在一个开关下：

```js
GameGlobal.__LOCAL_MOCK_GAME__ = true;
// 或
globalThis.__LOCAL_MOCK_APP__ = true;
```

建议用一个独立启动文件承载：

- 登录替身
- 请求替身
- 广告替身
- 统计 SDK 替身
- 插件替身
- 存储补丁

替身需要保持完整接口契约：

- 同步返回还是 Promise
- 回调触发顺序
- `onX/offX`
- `show/load/destroy`
- 嵌套字段
- `getData()` 等包装方法

不要用一个 `{code: 0}` 处理所有服务。

## 无广告模式

需要分别处理：

- 激励视频
- 插屏
- Banner
- 自定义广告
- 格子广告
- 其他 `create*Ad` API
- 广告关闭后的线上奖励校验

如果用户明确要求“去广告但点击直接领奖励”，激励广告的关闭回调应模拟完整观看：

```js
{ isEnded: true }
```

如果只是普通离线模式、没有授权直接发放奖励，则不能默认模拟奖励成功。

## 存档和数值修改

优先修改权威存档边界，而不是 UI 标签：

```text
getStorageSync
setStorageSync
getStorage
setStorage
cc.sys.localStorage
游戏自己的 SaveManager
```

使用游戏真实字段和物品 ID，并同时处理读取和保存，否则消费或重载后会恢复原值。

## 微信开发者工具验证清单

静态脚本通过后，在开发者工具中验证：

1. 导入根目录正确。
2. 调试 AppID 已记录。
3. 编译无致命错误。
4. 第一页面或第一场景显示。
5. 所需分包与资源加载。
6. 至少一次真实点击、输入、拖动或移动。
7. 所有被替换的服务流程执行一次。
8. 等待延迟回调，确认没有定时器异常。
9. 重新加载并检查存档。
10. 生成新的预览包。
11. 真机执行目标流程。

不要通过过滤控制台异常来制造“零错误”。已知无害警告应记录，不应隐藏。

## 常见问题

### `module __plugin__ is not defined`

检查调用模块的 ID、相对解析基准和插件 bundle 的 `define()` 注册名。不要全局替换字符串。

### `cc is not defined`

先修 Cocos 引擎和适配器加载顺序，不要创建假的 `cc` 对象。

### `getData is not a function`

本地响应缺少业务包装层，按调用者要求补齐对象结构。

### 首页能打开，但点击或移动失效

检查触摸/点击事件中的第一个异常。统计上报、教程接口、插件方法都可能在真正操作逻辑之前抛错。

### 开发者工具运行正常，真机预览提示非法目录

运行 `validate_project.py`，重点检查以双下划线开头和结尾的实体目录。虚拟模块字符串不等于实体目录。

### 手机仍运行旧代码

清理适当的编译缓存，重新编译并生成新的二维码。不要继续扫描旧预览二维码。

## 完成标准

不能以“解包成功”作为完成标准。一个合格交付至少应说明：

- 原包和 SHA-256 在哪里
- 使用了哪个解包器及版本
- 导入微信开发者工具的准确目录
- 普通小程序还是小游戏
- 引擎及版本
- 主包、分包和插件关系
- 本地模式开关位置
- 修改过哪些文件
- 验证了哪些真实交互
- 哪些线上能力仍不可用
- 是否完成真机预览验证

详细的 Agent 工作规范位于 [SKILL.md](SKILL.md)，专项资料位于 [references/](references/)。
