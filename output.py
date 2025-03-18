from rich.console import Console
from rich.panel import Panel
from rich.table import Table

con = Console()  # 实例化Console对象

class Output:
    def __init__(self, translated_text, *alternatives):
        self.text = translated_text
        self.an = alternatives
        asyncio.run(self.main())  # 运行异步方法
    
    async def main(self):
        # 创建并打印面板
        panel = Panel(self.text, title="翻译结果")
        con.print(panel)  # 使用console打印面板
        
        # 创建表格
        antable = Table(title="其他翻译")
        antable.add_column("序号")  # 修正拼写错误 culumn -> column
        antable.add_column("翻译")
        
        # 添加行
        for index, anais in enumerate(self.an):
            antable.add_row(str(index), anais)  # 转换index为字符串
        
        # 打印表格
        con.print(antable)