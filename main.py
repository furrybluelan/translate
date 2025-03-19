from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import sys
import aiofiles  # 用于异步文件操作

console = Console()  # 实例化Console对象

class Output:
    def __init__(self, translated_text, *alternatives):
        self.text = translated_text
        self.an = alternatives
    
    async def main(self):
        # 创建并打印面板
        panel = Panel(self.text, title="翻译结果")
        console.print(panel)  # 使用console打印面板
        
        # 创建表格
        antable = Table(title="其他翻译")
        antable.add_column("序号")  # 修正拼写错误 culumn -> column
        antable.add_column("翻译")
        
        # 添加行
        for index, anais in enumerate(self.an):
            antable.add_row(str(index), anais)  # 转换index为字符串
        
        # 打印表格
        console.print(antable)


class GetInput:
    """
    处理多种输入方式的类，按照优先级获取输入内容
    支持：命令行参数、文件输入、标准输入(包括管道)、交互式输入
    """
    def __init__(self, args):
        self.args = args  # 保存命令行参数
        
    async def _stdin(self):
        """
        从标准输入(stdin)读取内容，支持管道输入
        例如: echo "hello" | python script.py
        """
        # 检查是否有管道输入
        if not sys.stdin.isatty():  # 如果stdin不是终端，说明是管道输入
            return sys.stdin.read()  # 直接读取stdin
        return None  # 没有管道输入则返回None
    
    async def _input(self):
        """
        交互式获取用户输入，使用rich库美化提示
        当其他输入方式都不可用时使用
        """
        # console.input不是异步的，但为了保持接口一致，使用async定义
        return console.input("[cyan]请输入翻译内容：[/cyan]")
    
    async def _file(self):
        """
        从指定文件异步读取内容
        如果文件不存在或读取出错，返回None
        """
        if hasattr(self.args, 'file') and self.args.file:
            try:
                async with aiofiles.open(self.args.file, mode='r') as f:
                    return await f.read()
            except Exception as e:
                console.print(f"[red]读取文件出错: {e}[/red]")
        return None
    
    async def _con(self):
        """
        从命令行参数中获取直接提供的输入内容
        例如: python script.py --input "hello world"
        """
        if hasattr(self.args, 'input') and self.args.input:
            return self.args.input
        return None
    
    async def main(self):
        """
        主方法：按优先级尝试不同的输入方式
        优先级：命令行参数 > 文件输入 > 标准输入(管道) > 交互式输入
        """
        # 按优先级尝试不同的输入方式
        methods = [self._con, self._file, self._stdin, self._input]
        
        for method in methods:
            result = await method()
            if result is not None:
                return result
        
        # 如果所有方法都失败，返回空字符串
        return ""