# 项目描述

一套符合直觉的索引和切片语法。

|                                        | **Python**                                                           | **rstyleslice**                                                      |
| -------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **索引**                         | 从 0 开始（0 表示第 1 个元素）<br /><br />-1 表示倒数第 1 个元素（相同点） | 从 1 开始（1 表示第 1 个元素）<br /><br />-1 表示倒数第 1 个元素（相同点） |
| **切片**                         | 左闭右开区间，例如：<br />[3: 5] 表示提取第 4、5 这 2 个元素               | 双闭区间，例如：<br />[3: 5] 表示提取第 3、4、5 这 3 个元素                |
| **从右往**<br />**左切片** | step（步长）为负值，例如：<br />[9: 1: -1] 表示提取第 9~3 这 7 个元素      | step（步长）始终为正值，例如：<br />[9: 1: 1] 表示提取第 9~1 这 9 个元素   |

切片格式为  [start: stop: step]  ，start 表示从哪条开始，stop 表示到哪条停止，step 表示步长。当  step>=2  时表示间隔式切片。

# 关于作者

作者：lcctoor.com

域名：lcctoor.com

邮箱：lcctoor@outlook.com

[主页](https://lcctoor.github.io/me/) \| [微信](https://lcctoor.github.io/me/author/WeChatQR-max.jpg) \| [Python交流群](https://lcctoor.github.io/me/lccpy/WechatReadersGroupQR-original.jpg) \| [捐赠](https://lcctoor.github.io/me/donation/donationQR-1rmb-max.jpg)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/lccpy/issues)、[微信](https://lcctoor.github.io/me/author/WeChatQR-max.jpg) 与我联系。

# 安装

```
pip install rstyleslice
```

# [教程](https://lcctoor.github.io/lccpy/?doc=rstyleslice)

# 教程预览

#### 导入

```python
from rstyleslice import rslice
```

#### 创建R风格容器

```python
obj = rslice([1,2,3,4,5,6,7,8,9])

# Python中任何可以索引和切片的对象（如list、str、tuple）都可以转化成R风格容器。
```

#### 索引取值

```python
obj[1]
# >>> 1
```

#### 索引赋值

```python
obj[1] = 111
obj[:]
# >>> [111, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### 切片取值

```python
obj[3:7]  # >>> [3, 4, 5, 6, 7]
obj[7:3]  # >>> [7, 6, 5, 4, 3]
obj[3:7:2]  # >>> [3, 5, 7]
obj[8:2:3]  # >>> [8, 5, 2]
```

#### 切片赋值

```python
obj[4:6] = [44, 55]
obj[:]
# >>> [111, 2, 3, 44, 55, 7, 8, 9]

obj[4:6] = []
obj[:]
# >>> [111, 2, 3, 8, 9]

obj[4:] = [1, 2, 3, 4, 5]
obj[:]
# >>> [111, 2, 3, 1, 2, 3, 4, 5]

obj[4:100] = ['1', 2, 3, 4, 5]
obj[:]
# >>> [111, 2, 3, '1', 2, 3, 4, 5]
```
