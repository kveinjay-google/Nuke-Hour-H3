# Nuke Hour H3

基于 [VCMI](https://github.com/vcmi/vcmi) 的实验性 iOS 简体中文社区版。面向触摸屏重新设计启动器，并使用独立生成的奇幻美术素材。

[English](README.md) · [iOS 构建说明](docs/community/BUILD_IOS.md) · [验收状态](docs/community/STATUS.md) · [素材与许可](docs/community/ARTWORK.md)

![iPad 启动器](docs/community/screenshots/launcher-ipad.png)

包含游戏、模组、设置、帮助与导入界面的改版，大尺寸触摸控件、立体按钮四种状态、狮鹫应用图标，以及可选的 Noto 简体中文字体回退模组。上游固定为 `290525c5518e6fba43143d374d5262acb5c0f5ec`，保留引擎源码、作者署名和原有许可证。社区改动与原创素材使用了 AI 辅助。

## 自备游戏数据

运行必须拥有合法的 **Heroes III Complete 或 Shadow of Death** 数据。本仓库不提供商业游戏安装资源、音乐、地图、HD Edition PAK 文件或用户存档。

官方 **HD Edition** 只能作为可选高清资源增强，不能替代基础游戏。本项目保留上游原生 HD 导入机制，HD 真机实测仍待完成。

## 获取与构建

```sh
git clone --recurse-submodules https://github.com/kveinjay-google/Nuke-Hour-H3.git
cd Nuke-Hour-H3
python3 tools/check_community_package.py
```

iOS 构建需要 macOS、Xcode、CMake、Conan，并使用你自己的签名团队与应用标识，详见[构建说明](docs/community/BUILD_IOS.md)。

此次公开的是源码，不是 IPA 或 App Store 上架版本。设备与模拟器构建、签名安装及启动器检查已通过；中文游戏内容、地图、战斗、存档读写、HD 真机 A/B 与性能验收仍未完成，详见[验收状态](docs/community/STATUS.md)。

## 许可证

VCMI 与社区改动遵循 [GPL-2.0-or-later](license.txt)，各第三方组件保留自身许可证。Noto 中文字体为 [OFL-1.1](Mods/vcmi-zh-cn-fonts/LICENSE.OFL.txt)，其[版权说明](Mods/vcmi-zh-cn-fonts/NOTICE.md)随字体保留。原创美术素材的来源与文件哈希见[素材说明](docs/community/ARTWORK.md)。

这是独立社区分支，不代表 VCMI、Ubisoft 或 Apple 官方项目。贡献前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 `AGENTS.md`，理解并验证提交内容，保留上游署名，不要提交商业资源或个人签名、测试资料。
