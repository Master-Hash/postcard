# postcard
动态电子名片，使用 FastAPI 框架

## 效果图
<img src="/final.svg" alt="开发环境效果图">

参数：`quote=%E7%94%9F%E6%97%A0%E6%89%80%E6%81%AF%E3%80%82&matrix_quote=(1%200%200%201%20300%20145)&email=A137294381b@163.com&github=Master-Hash&site=https://one.wh0th.ink/&luogu=Master_Hash`

<img src="http://localhost:8000/app?quote=%E7%94%9F%E6%97%A0%E6%89%80%E6%81%AF%E3%80%82&matrix_quote=(1%200%200%201%20300%20145)&email=A137294381b@163.com&github=Master-Hash&site=https://one.wh0th.ink/&luogu=Master_Hash"
    alt="生产环境效果图">

## 请求参数
参见 [docs](https://postcard.wh0th.ink/docs) 和 [redoc](https://postcard.wh0th.ink/redoc)

因为 FastAPI 的锅，Dependency 中不能给参数标文档，~~所以暂时各位只能顾名思义，每个参数试下意思？~~

<dl>
    <dt><code>matrix_{detail,line,contact,quote}</code></dt>
    <dd>线性变换 4 大块的位置。</dd>
    <dd>见 <a href="https://developer.mozilla.org/zh-CN/docs/Web/SVG/Attribute/transform">transform - SVG | MDN</a></dd>
    <dt><code>quote</code>，<code>width</code></dt>
    <dd>一段能表达自己的话。</dd>
    <dd>可自动折行，行宽由 <code>width</code> 指定。</dd>
    <dd>如需手动折行，换行符为 <code>%0A</code></dd>
    <dt><code>lang</code>，<code>tz</code></dt>
    <dd>手动传入语言和时间。</dd>
    <dd>如果不传入，将从 `Accept-Language` 请求头和请求 IP 对应地理位置时区自动计算。</dd>
    <dd>除非 Github（因为会被 camo 预先爬取），推荐自动计算而不是手动传入。</dd>
    <dt><code>light</code>，<code>dark</code></dt>
    <dd>亮色和暗色主题，由 base16 驱动</dd>
    <dt><code>&lt;contact&gt;</code></dt>
    <dd>剩下的全部是可传入的社交属性。</dd>
    <dd>将按传入的先后顺序，从上至下展示。</dd>
    <dd>与 Xecades 的 API 完全相同。</dd>
    <dd>见 <a href="https://api.xecades.xyz/">API | Xecades</a> 图形界面编辑 URL，实时预览</dd>
    <dd><a href="https://github.com/Xecades/API">Github - Xecades/API</a></dd>
</dl>

## 功能
- 本地化 & 时区
- CSS 动画
- 自动生成文档
- 错误链接自动重定向到带有错误提示的图片

## 降级
- 不再支持图片
- 没有特判中文，导致日期格式没有空格
- 图标采用 `<svg>`子元素，导致了 CSS 类冲突

另外，因为 Xecades 认为不合适，我没有加水印。随缘找到这里吧。

## 技术说明
数据库来自 [GeoLite](https://dev.maxmind.com/geoip/geoip2/geolite2/)。

## 致谢
- 前辈 [@hanlin-studio](https://github.com/hanlin-studio) 的[原型](https://github.com/hanlin-studio/IP)
- [P3TERX/GeoLite.mmdb](https://github.com/P3TERX/GeoLite.mmdb)
- [FastGit](https://fastgit.org/)
- [anuraghazra/github-readme-stats](https://github.com/anuraghazra/github-readme-stats)
- [chriskempson/base16](https://github.com/chriskempson/base16) 及配套工具，资源
- [InspectorMustache/base16-builder-python](https://github.com/InspectorMustache/base16-builder-python)
