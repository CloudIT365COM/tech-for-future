# 01 - Python 并发与 GIL (Global Interpreter Lock)

## 💡 核心概念
*   **GIL 是什么**：CPython 解释器中的一把互斥锁，确保同一时刻只有一个线程在执行 Python 字节码。
*   **为什么重要**：它导致 Python 的多线程无法真正利用多核 CPU 的算力来做数学计算。

## 🚀 场景化选型 (云/数据工程场景)

1.  **I/O 密集型 (I/O-Bound)**
    *   **场景**：批量下载 S3 文件、调用数百个第三方 API、查询外部数据库。
    *   **最佳方案**：`asyncio` 或 `concurrent.futures.ThreadPoolExecutor`（多线程）。
    *   **原因**：线程在等待网络响应时会主动释放 GIL，因此多线程可以极大地提高网络 I/O 效率。
2.  **CPU 密集型 (CPU-Bound)**
    *   **场景**：利用 Pandas 处理千万级行数据、图像格式转换、大矩阵运算。
    *   **最佳方案**：`concurrent.futures.ProcessPoolExecutor`（多进程）。
    *   **原因**：每个进程都有自己独立的 Python 解释器和独立的 GIL，可以直接利用服务器的多核 CPU。

## 🎯 常见面试题对答技巧
**Q: 如果你的 Python 爬虫/数据采集脚本运行得很慢，你会如何优化？**
**A:** 首先区分瓶颈。如果瓶颈在网络请求（I/O 密集），我会使用 `asyncio` 和 `aiohttp`，或者使用多线程池并发请求。如果在数据清洗（CPU 密集），我会考虑用多进程，或者改用底层释放了 GIL 的库（如 NumPy 或 Polars）来进行矢量化计算。
