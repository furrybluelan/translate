from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import sys
import aiofiles
import argparse
import asyncio  # 添加异步事件循环支持

console = Console()

class TranslationOutput:
    """处理翻译结果输出的类"""
    def __init__(self, translated_text, *alternatives):
        self.text = translated_text
        self.alternatives = alternatives
    
    async def show(self):
        """异步显示翻译结果"""
        # 主翻译结果面板
        main_panel = Panel(self.text, title="[bold green]翻译结果[/bold green]")
        console.print(main_panel)
        
        # 备选翻译表格
        if self.alternatives:
            table = Table(title="[bold yellow]备选翻译[/bold yellow]", show_header=True)
            table.add_column("编号", style="cyan", width=6)
            table.add_column("内容", style="magenta")
            
            for idx, alt in enumerate(self.alternatives, 1):
                table.add_row(str(idx), alt)
            
            console.print(table)

class InputHandler:
    """统一输入处理类"""
    def __init__(self, args):
        self.args = args
        self.input_sources = [
            self._from_args,
            self._from_file,
            self._from_stdin,
            self._from_interactive
        ]
    
    async def _from_args(self):
        """从命令行参数获取输入"""
        if getattr(self.args, 'text', None):
            return self.args.text
        return None

    async def _from_file(self):
        """异步读取文件内容"""
        if getattr(self.args, 'file', None):
            try:
                async with aiofiles.open(self.args.file, 'r') as f:
                    return await f.read()
            except Exception as e:
                console.print(f"[red]文件读取错误: {e}[/red]")
        return None

    async def _from_stdin(self):
        """处理管道输入"""
        if not sys.stdin.isatty():
            return sys.stdin.read()
        return None

    async def _from_interactive(self):
        """交互式输入"""
        return console.input("[bold cyan]请输入要翻译的内容: [/]")

    async def get_content(self):
        """按优先级获取输入内容"""
        for source in self.input_sources:
            if content := await source():
                return content.strip()
        return ""

class CommandHandler:
    """命令行处理核心类"""
    def __init__(self):
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """创建参数解析器"""
        parser = argparse.ArgumentParser(
            description="多功能翻译工具",
            add_help=False,
            formatter_class=argparse.RawTextHelpFormatter
        )

        # 通用参数
        parser.add_argument('--debug', action='store_true', help='调试模式')
        parser.add_argument('-h', '--help', action='store_true', help='显示帮助信息')

        # 子命令
        subparsers = parser.add_subparsers(dest='command', title='可用命令')

        # 翻译命令
        trans_parser = subparsers.add_parser(
            'trans', 
            aliases=['t'],
            help='执行翻译操作',
            add_help=False
        )
        trans_parser.add_argument('-f', '--file', help='指定输入文件')
        trans_parser.add_argument('text', nargs='*', help='要翻译的文本')

        # 配置命令
        config_parser = subparsers.add_parser(
            'config',
            aliases=['cfg'],
            help='配置管理',
            add_help=False
        )
        config_parser.add_argument('mainkey',nargs='?',help='配置主键')
        config_parser.add_argument('subkey', nargs='?', help='配置次键')
        config_parser.add_argument('value', nargs='?', help='配置值')

        # 帮助命令
        subparsers.add_parser(
            'help',
            help='显示帮助信息',
            add_help=False
        )

        return parser

    async def handle_config(self, args):
        """处理配置命令"""
        if args.help or not args.key:
            console.print("[bold]配置管理:[/]")
            console.print("  config [subkey] [value] - 设置配置项")
            console.print(" config list - 列出所有配置")
            return
        # 这里添加实际的配置处理逻辑
        console.print(f"[yellow]配置项 {args.mainkey}.{args.subkey} 已设置为 {args.value}[/yellow]")

    async def handle_translation(self, args):
        """处理翻译流程"""
        input_handler = InputHandler(args)
        content = await input_handler.get_content()
        
        if not content:
            console.print("[red]错误: 没有输入内容[/red]")
            return

        # 这里添加实际的翻译逻辑，示例使用伪数据
        translated = "Hello World"
        alternatives
        
        output = TranslationOutput(translated, *alternatives)
        await output.show()

    async def execute(self):
        """执行命令解析"""
        args = self.parser.parse_args()

        if args.help or args.command == 'help':
            self.parser.print_help()
            return

        if args.debug:
            console.print("[yellow]调试模式已启用[/yellow]")

        try:
            if args.command in ('config', 'cfg'):
                await self.handle_config(args)
            elif args.command in ('trans', 't'):
                await self.handle_translation(args)
            else:
                self.parser.print_help()
        except Exception as e:
            console.print(f"[red]错误: {str(e)}[/red]")

def main():
    handler = CommandHandler()
    asyncio.run(handler.execute())

if __name__ == "__main__":
    main()