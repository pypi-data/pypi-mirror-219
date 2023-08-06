from rich.console import Console

console = Console(soft_wrap=True, record=True)
errConsole = Console(stderr=True, style="bold red", soft_wrap=True)
print = console.print
log = console.log
status = console.log
