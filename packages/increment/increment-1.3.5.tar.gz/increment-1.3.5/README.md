# 项目描述

分布式主键生成器，支持多机器|多进程|多线程并发生成。

# 关于作者

作者：lcctoor.com

域名：lcctoor.com

邮箱：lcctoor@outlook.com

[主页](https://lcctoor.github.io/me/) \| [微信](https://lcctoor.github.io/me/author/WeChatQR-max.jpg) \| [Python交流群](https://lcctoor.github.io/me/lccpy/WechatReadersGroupQR-original.jpg) \| [捐赠](https://lcctoor.github.io/me/donation/donationQR-1rmb-max.jpg)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/lccpy/issues)、[微信](https://lcctoor.github.io/me/author/WeChatQR-max.jpg) 与我联系。

# 安装

```
pip install increment
```

# 教程

#### 导入

```python
from increment import incrementer
```

#### 创建生成器

```python
inc = incrementer()
```

#### 使用创建生成器时的时间

```python
inc.pk1()
# >>> 'lg85x42f_gsdo_258_1'

inc.pk1()
# >>> 'lg85x42f_gsdo_258_2'

# 'lg85x42f'是创建生成器时的时间
```

#### 使用当前时间

```python
inc.pk2()
# >>> 'lg8657cj_gsdo_258_3'

# 'lg8657cj'是当前时间
```

#### 只返回自增主键

```python
inc.pk3()
# >>> '4'

inc.pk3()
# >>> '5'
```
