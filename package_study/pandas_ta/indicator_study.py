import io
import re
import contextlib
from inspect import isroutine, getmodule

def capture_help(obj):
    """
    捕获对象的帮助文档并清理格式控制字符
    
    参数:
        obj: 要获取帮助的Python对象(函数/类/模块等)
        
    返回:
        str: 清理后的纯文本帮助文档
    """
    # 创建内存缓冲区
    buffer = io.StringIO()
    
    # 重定向标准输出并执行help()
    with contextlib.redirect_stdout(buffer):
        help(obj)
    
    # 获取原始帮助文本
    raw_text = buffer.getvalue()
    
    # 清理退格控制字符（用于终端粗体显示）
    cleaned_text = re.sub(r'.\x08', '', raw_text)
    
    return cleaned_text


# 示例用法
if __name__ == "__main__":
    import pandas_ta as ta
    bbands_code = capture_help(ta.momentum.macd)
    print(bbands_code)
    