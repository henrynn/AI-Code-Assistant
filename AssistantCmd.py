import os
import argparse
import openai
from dotenv import load_dotenv


# 设置 OpenAI API 密钥
load_dotenv('.env')
openai.api_type = "azure"
openai.api_base = "https://<YOUR_RESROUCE>.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

review_prompt = "You are an code reviewer that help developer find program languange potential issue, such as memory leak, empty pointer,unclosed resources, infinite loop etc.\n Unclosed resources: When working with input/output streams, it's important to ensure that any resources that are opened (such as InputStream or OutputStream objects) are closed when they are no longer needed. Failure to close these resources can lead to resource leaks and other issues. \n Reading larg input streams: When reading from input streams, it's important to be aware of the size of the stream. If the stream is very large, it may not be possible to read the entire stream into memory at once without causing an OutOfMemoryError. In these cases, it's best to read the stream in smaller chunks using a buffer. Provide output for the issue only related current input using chinese. If there is no mentioned issue found, don't provide any output. Expected output:Provide explanation about the issue. Provide solution for the issue. Provide the modified code that fix the issue. for example: 问题：xxx  解决方案：xxxx 修改后的代码：xxxx"

"""
You are an code reviewer that help developer find program languange potential issue, such as memory leak, empty pointer,unclosed resources, infinite loop etc.
Unclosed resources: When working with input/output streams, it's important to ensure that any resources that are opened (such as InputStream or OutputStream objects) 
are closed when they are no longer needed. Failure to close these resources can lead to resource leaks and other issues. 
Reading larg input streams: When reading from input streams, it's important to be aware of the size of the stream. If the stream is very large, 
it may not be possible to read the entire stream into memory at once without causing an OutOfMemoryError. 
In these cases, it's best to read the stream in smaller chunks using a buffer. 
Provide output for the issue only related current input using chinese. If there is no mentioned issue found, don't provide any output. 
Expected output:Provide explanation about the issue. Provide solution for the issue. Provide the modified code that fix the issue. 

for example: 
    问题：xxx  
    解决方案：xxxx 
    修改后的代码：xxxx"

"""
# 定义 OpenAI API 请求
def check_code(code):
    model_engine = "<YOUR_RESROUCE>"
    prompt = f"{review_prompt}:\n{code}\n\n"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )
    return response.choices[0].text.strip()

# 遍历指定文件夹中的所有 Java 文件
def check_folder(folder_path):
    # 设置输出文件路径
    output_file = os.path.join(folder_path, "scan_result.txt")

    with open(output_file, "w",encoding='utf-8',errors='replace') as output:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith(".java"):
                    file_path = os.path.join(root, file)
                    # 判断文件大小是否大于 8KB
                    if os.path.getsize(file_path) > 7 * 1024:
                        print(f"File {file_path} is too large, skipping...")
                        continue

                    with open(file_path, encoding='utf-8') as f:
                        print(file_path)
                        try:
                            code = f.read()
                            result = check_code(code)
                            result = result.replace("<|im_end|>", "")
                            result = result.replace("<|im_sep|>", "")
                            
                        except Exception as e:
                            print(e)
                        output.write(f"代码文件: {file_path}\n")
                        output.write(f"{result}\n")
                        output.write("=" * 90 + "\n")

# 解析命令行参数
#parser = argparse.ArgumentParser(description="Check Java code using OpenAI API")
#parser.add_argument("folder_path", type=str, help="Path to the folder containing Java files")
#args = parser.parse_args()

# 获取用户输入的文件夹路径
folder_path = input("请提供需要扫描的Java项目代码目录: ")

# 检查指定文件夹中的所有 Java 文件
check_folder(folder_path)

print(f"检测结果输出到： {folder_path}/scan_result.txt")
