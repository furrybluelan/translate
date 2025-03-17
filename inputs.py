import sys
import aiofiles  # 注意这里是aiofiles而不是aiofile
import fileinput
from rich.console import Console


console = Console()

class GetInput:
    def __init__(self, args):
        self.args = args  # 保存args参数
        
    async def _stdin(self):
        # fileinput不支持异步，所以这里返回一个字符串
        return ''.join(fileinput.input())
    
    async def _input(self):
        # console.input也不是异步的，但为了保持接口一致
        return console.input("[cyan]请输入翻译内容：[/cyan]")
    
    async def _file(self):
        if hasattr(self.args, 'file') and self.args.file:
            try:
                async with aiofiles.open(self.args.file, mode='r') as f:
                    return await f.read()
            except Exception as e:
                console.print(f"[red]读取文件出错: {e}[/red]")
        return None
    
    async def _con(self):
        if hasattr(self.args, 'input') and self.args.input:
            return self.args.input
        return None
    
    async def main(self):
        # 按优先级尝试不同的输入方式
        methods = [
            self._con(),      # 首先尝试命令行参数
            self._file(),     # 然后尝试文件
            self._input(),    # 接着尝试交互式输入
            self._stdin()     # 最后尝试标准输入
        ]
        
        for method in methods:
            try:
                result = await method
                if result is not None and result != "":
                    return result
            except Exception as e:
                console.print(f"[yellow]输入方法失败: {e}[/yellow]")
                continue
        
        console.print("[red]没有有效的输入[/red]")
        sys.exit(1)
