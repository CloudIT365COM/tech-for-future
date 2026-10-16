import sys
import time

def process_data_with_list(num_items):
    """传统做法：使用列表，一次性将所有数据载入内存"""
    print(f"Creating list of {num_items} items...")
    # 列表推导式
    data_list = [x ** 2 for x in range(num_items)]
    print(f"Memory size of List: {sys.getsizeof(data_list) / (1024*1024):.2f} MB")
    return data_list

def process_data_with_generator(num_items):
    """高级做法：使用生成器，按需计算"""
    print(f"Creating generator for {num_items} items...")
    # 生成器表达式 (注意用的是圆括号)
    data_gen = (x ** 2 for x in range(num_items))
    print(f"Memory size of Generator: {sys.getsizeof(data_gen)} Bytes")
    return data_gen

def main():
    # 模拟处理一千万条数据
    NUM_RECORDS = 10_000_000 
    
    print("--- Testing List Approach ---")
    start = time.time()
    my_list = process_data_with_list(NUM_RECORDS)
    # 模拟处理第一条数据
    print(f"First item processed: {my_list[0]}")
    
    print("\n--- Testing Generator Approach ---")
    my_gen = process_data_with_generator(NUM_RECORDS)
    # 模拟处理第一条数据，使用 next() 按需获取
    print(f"First item processed: {next(my_gen)}")

if __name__ == "__main__":
    main()
