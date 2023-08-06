# 项目描述

根据 openai 官方接口‘openai’改造的‘openai2’，比官方接口更好用一点。

# 关于作者

作者：lcctoor.com

域名：lcctoor.com

邮箱：lcctoor@outlook.com

[主页](https://lcctoor.github.io/me/) \| [微信](https://lcctoor.github.io/me/author/WeChatQR-max.jpg) \| [Python交流群](https://lcctoor.github.io/me/lccpy/WechatReadersGroupQR-original.jpg) \| [捐赠](https://lcctoor.github.io/me/donation/donationQR-1rmb-max.jpg)

# Bug提交、功能提议

您可以通过 [Github-Issues](https://github.com/lcctoor/lccpy/issues)、[微信](https://lcctoor.github.io/me/author/WeChatQR-max.jpg) 与我联系。

# 安装

```
pip install openai2
```

# 获取api_key

[获取链接1](https://platform.openai.com/account/api-keys)

[获取链接2](https://www.baidu.com/s?wd=%E8%8E%B7%E5%8F%96%20openai%20api_key)

# 教程

#### 导入

```python
from openai2 import Chat
```

#### 创建对话

```python
api_key = 'api_key'  # 更换成自己的api_key

Tony = Chat(api_key=api_key, model="gpt-3.5-turbo")
Lucy = Chat(api_key=api_key, model="gpt-3.5-turbo")  # 每个实例可使用 相同 或者 不同 的api_key
```

#### 对话

```python
Tony.request('自然数50的后面是几?')  # >>> 51
Lucy.request('自然数100的后面是几?')  # >>> 101

Tony.request('再往后是几?')  # >>> 52
Lucy.request('再往后是几?')  # >>> 102

Tony.request('再往后呢?')  # >>> 53
Lucy.request('再往后呢?')  # >>> 103
```

#### 存档

```python
Tony.dump('./talk_record.json')  # 可使用相对路径或绝对路径
```

#### 载入存档

```python
Jenny = Chat(api_key=api_key, model="gpt-3.5-turbo")
Jenny.load('./talk_record.json')

Jenny.request('再往后呢?')  # >>> 54
```

#### 对话回滚

```python
Anna = Chat(api_key=api_key, model="gpt-3.5-turbo")

Anna.request('自然数1的后面是几?')  # >>> 2
Anna.request('再往后是几?')  # >>> 3
Anna.request('再往后呢?')  # >>> 4
Anna.request('再往后呢?')  # >>> 5
Anna.request('再往后呢?')  # >>> 6
Anna.request('再往后呢?')  # >>> 7
Anna.request('再往后呢?')  # >>> 8

# 回滚1轮对话
Anna.rollback()  # >>> [user]:再往后呢? [assistant]:7

# 再回滚3轮对话
Anna.rollback(n=3)  # >>> [user]:再往后呢? [assistant]:4

Anna.request('再往后呢?')  # >>> 5
```

注：

1、执行 `Anna.rollback(n=x)` 可回滚 x 轮对话。

2、`Anna.rollback()` 相当于 `Anna.rollback(n=1)` 。

#### 修改api_key

```python
Anna.api_key = 'new api_key'
```

#### 更多方法

openai2.Chat 底层调用了 [openai.ChatCompletion.create](https://platform.openai.com/docs/api-reference/chat/create?lang=python)，在实例化时，支持 openai.ChatCompletion.create 的所有参数，例如：`Chat(api_key=api_key, model="gpt-3.5-turbo", max_tokens=100)` 。
