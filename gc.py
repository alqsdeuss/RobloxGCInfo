# imports
import requests
import time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
# console
console = Console()
# load gr
def gtgrp(id):
    url = f"https://groups.roblox.com/v1/groups/{id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# load roles
def gtroles(id):
    url = f"https://groups.roblox.com/v1/groups/{id}/roles"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
# loading spinner
def loading(msg="loading..."):
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as p:
        task = p.add_task(msg, total=None)
        time.sleep(2)
        p.stop()
# main fn
def main():
    console.print("[bold green]roblox group info[/bold green]")
    while True:
        gid = console.input("\n[bold green]enter roblox group id: [/bold green]").lower()
        with console.status("[bold green]loading...[/bold green]", spinner="dots"):
            grp = gtgrp(gid)
            time.sleep(1.5)

        if not grp or "errors" in grp:
            console.print("[bold red]invalid group[/bold red]")
        else:
            console.print("[bold green]group found[/bold green]")
# show ginfo
            loading("fetching details...")
            name = grp.get("name", "n/a")
            desc = grp.get("description", "no description")
            mems = grp.get("memberCount", 0)
            owner = grp.get("owner", {}).get("username", "unknown")
            rolesdata = gtroles(gid)
            roles = rolesdata.get("roles", []) if rolesdata else []
            ranks = ", ".join(r.get("name", "unknown") for r in roles) if roles else "none"
            tbl = Table(title=f"group info: [bold cyan]{name}[/bold cyan]", style="bright_blue")
            tbl.add_column("field", style="magenta", no_wrap=True)
            tbl.add_column("value", style="green")
            tbl.add_row("group id", str(gid))
            tbl.add_row("name", name)
            tbl.add_row("description", desc)
            tbl.add_row("owner", owner)
            tbl.add_row("members", str(mems))
            tbl.add_row("ranks", ranks)
            console.print(tbl)
# repeat
        ans = console.input("\n[bold green]check another group: 1 = yes or 2 = no: [/bold green]").strip()
        while ans not in ("1", "2"):
            ans = console.input("[bold red]enter 1 or 2: [/bold red]").strip()
        if ans == "2":
            console.print("[bold green]bye![/bold green]")
            break
# end
if __name__ == "__main__":
    main()
