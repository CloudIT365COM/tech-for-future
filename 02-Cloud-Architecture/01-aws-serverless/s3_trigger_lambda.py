import urllib.parse
import boto3
import logging

# 配置日志，Lambda 会自动将这些日志推送到 AWS CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 最佳实践：在 handler 外部初始化客户端
# 这样在 Lambda 环境被复用（Warm Start）时，无需重新建立连接
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    AWS Lambda 的标准入口函数。
    当 S3 配置了事件触发器后，上传文件会自动将事件信息传入 event 参数。
    """
    # 1. 从事件(Event)中提取 Bucket 名字和文件的 Key
    # 注意：使用 unquote_plus 防止文件名中带有空格或特殊字符被 URL 编码
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    try:
        logger.info(f"Started processing file: {key} from bucket: {bucket}")
        
        # 2. 获取对象流 (非常重要：不要用 download_file 直接存盘)
        response = s3_client.get_object(Bucket=bucket, Key=key)
        
        # 3. 结合“生成器”思想，迭代读取 StreamingBody
        # 这样 Lambda 哪怕只有 128MB 内存，也能处理 GB 级别的大文件
        line_count = 0
        for line in response['Body'].iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                # TODO: 在这里添加数据清洗、格式转换或写入数据库的业务逻辑
                line_count += 1
        
        logger.info(f"Successfully processed {line_count} lines.")
        return {
            'statusCode': 200,
            'body': f'Success: Processed {line_count} lines from {key}'
        }
        
    except Exception as e:
        logger.error(f"Error getting object {key} from bucket {bucket}. Error: {str(e)}")
        # 在生产环境中，这里应该抛出异常以便触发死信队列 (DLQ) 或重试机制
        raise e
