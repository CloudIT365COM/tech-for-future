import time
import concurrent.futures

# 模拟一个耗时的网络 I/O 操作，例如调用外部 API 或下载 S3 文件
def fetch_data(task_id):
    print(f"Task {task_id}: Starting network request...")
    time.sleep(2)  # 模拟网络延迟
    print(f"Task {task_id}: Finished request.")
    return f"Result of {task_id}"

def main():
    task_ids = list(range(1, 6)) # 5 个任务
    start_time = time.time()

    # 最佳实践：使用 ThreadPoolExecutor 处理 I/O 密集型任务
    # 虽然有 GIL，但 time.sleep() (或真实的 socket I/O) 会释放 GIL
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(fetch_data, task_ids))

    print(f"\nAll results: {results}")
    print(f"Total time taken: {time.time() - start_time:.2f} seconds")
    # 如果是串行执行，需要 10 秒。多线程并发只需约 2 秒。

if __name__ == "__main__":
    main()
