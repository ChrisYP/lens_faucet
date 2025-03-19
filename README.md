# 项目说明文档

## 项目概述
~~由于领水需要google账户登录，我也懒得维护了，所以代码已过期。~~

这是一个基于Python的多线程任务处理系统，能够高效地领取`Lens`的`$Grass`测试币。该系统利用线程池并发执行任务，并提供实时的进度跟踪和日志记录功能。


## 使用方法

0. 安装依赖：`pip install -r requirements.txt`
1. 准备数据文件：在`data/data.txt`中每行放置一个任务项
2. 配置环境变量：创建`.env`文件并设置相关参数（如`WORKERS`）
3. 运行主程序：执行`python main.py`
4. 可以重复运行，并且会跳过已经执行过的任务。请放心大胆的暂停、终止、重启程序。
5. 成功领取`$Grass`测试币后，会保存在`data/success.txt`，但是注意这只是`字面意义上的成功领取`，网站是返回领取成功的，但如果他没有发给你测试币，我也是没办法的。同理，即使不在`success.txt`中，也不代表没有领取成功。所以后续还是需要自己去写个查询查看是否领取成功。

## 配置说明

- `WORKERS`：指定线程池大小，不设置则默认为CPU核心数的2倍
- 日志配置：日志文件保存在`logs`目录，按日期命名，保留3天

## 代码示例

```python
# 主函数调用示例
if __name__ == '__main__':
    # 每3秒重新加载环境变量
    timer = abu.SetInterval(lambda: load_dotenv(override=True), 3)
    # 从文件加载任务数据
    with open("data/data.txt", "r") as f:
        data = f.read().strip().split("\n")
    # 执行主处理函数
    main(data, os.getenv("WORKERS"))
    # 取消定时器
    timer.cancel()
```

## 项目结构

```
├── main.py          # 主程序入口
├── src/
│   └── task.py      # 任务处理模块
├── data/
│   └── data.txt     # 任务数据文件
├── logs/            # 日志文件目录
└── .env             # 环境变量配置文件
```

## 注意事项

- 确保`data`目录下有正确格式的`data.txt`文件
- 程序会自动创建`logs`目录用于存放日志文件
- 可以通过修改`.env`文件动态调整程序配置，无需重启程序

## 依赖库

- loguru：高级日志管理
- python-dotenv：环境变量管理
- abu：提供定时器功能
- concurrent.futures：提供线程池支持
