import sys
import asyncio
import aiofile
import fileinput
from rich.console import Console


console = Console()

class GetInput():
  def __init__(self):
    self.main()
  async def _stdin():
    return fileinput.input()
  async def _input():
    return console.input("[cyan]请输入翻译内容：[/cyan]")
  async def _file():
    args.file
