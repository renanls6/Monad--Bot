import os
import sys
import importlib
import inquirer
import asyncio
import time
from colorama import init, Fore, Style
from scripts.apriori import get_quote

init(autoreset=True)

BORDER_WIDTH = 80

def print_border(text: str, color=Fore.CYAN, width=BORDER_WIDTH):
    text = text.strip()
    if len(text) > width - 4:
        text = text[:width - 7] + "..."
    padded_text = f" {text} ".center(width - 2)
    print(f"{color}╭{'─' * (width - 2)}╮{Style.RESET_ALL}")
    print(f"{color}│{padded_text}│{Style.RESET_ALL}")
    print(f"{color}╰{'─' * (width - 2)}╯{Style.RESET_ALL}")

def print_section(title, icon="⚙️", color=Fore.YELLOW):
    print(f"\n{color}{'─'*BORDER_WIDTH}")
    print_border(f"{icon} {title}", color)
    print(f"{color}{'─'*BORDER_WIDTH}{Style.RESET_ALL}")

def _banner():
    print(f"\n{Fore.GREEN}{'═' * BORDER_WIDTH}")
    print_border("🚀 MONAD TESTNET AUTOMATION", Fore.GREEN)
    print(f"{'═' * BORDER_WIDTH}{Style.RESET_ALL}\n")

def get_available_scripts():
    return [
        {"name": "1. Rubic Swap", "value": "rubic"},
        {"name": "2. Magma Staking", "value": "magma"},
        {"name": "3. Izumi Swap", "value": "izumi"},
        {"name": "4. aPriori Staking", "value": "apriori"},
        {"name": "5. Kintsu Staking", "value": "kintsu"},
        {"name": "6. Bean Swap", "value": "bean"},
        {"name": "7. Monorail Swap", "value": "mono"},
        {"name": "8. Bebop Swap", "value": "bebop"},
        {"name": "9. Ambient Finance Swap", "value": "ambient"},
        {"name": "10. Uniswap Swap", "value": "uniswap"},
        {"name": "11. Deploy Contract", "value": "deploy"},
        {"name": "12. Send TX (random/file)", "value": "sendtx"},
        {"name": "13. Bima Deposit bmBTC", "value": "bima"},
        {"name": "14. Mint NFT Lil Chogstars", "value": "lilchogstars"},
        {"name": "17. ❌ Exit", "value": "exit"}
    ]

def run_script(script_module):
    run_func = script_module.run
    if asyncio.iscoroutinefunction(run_func):
        asyncio.run(run_func())
    else:
        run_func()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    _banner()

    while True:
        print_section("Main Menu", icon="📋")
        get_quote()

        available_scripts = get_available_scripts()
        questions = [
            inquirer.List(
                'script',
                message=f"{Fore.CYAN}Select a script to run:{Style.RESET_ALL}",
                choices=[script["name"] for script in available_scripts],
                carousel=True
            )
        ]
        answers = inquirer.prompt(questions)
        if not answers:
            continue

        selected_script_name = answers['script']
        selected_script_value = next(script["value"] for script in available_scripts if script["name"] == selected_script_name)

        if selected_script_value == "exit":
            print_section("EXITING", icon="👋", color=Fore.RED)
            print(f"{Fore.YELLOW}{'Goodbye! See you soon!':^80}")
            print(f"{Fore.GREEN}{'═' * BORDER_WIDTH}{Style.RESET_ALL}\n")
            sys.exit(0)

        try:
            print_section(f"Running: {selected_script_name}", icon="🚧", color=Fore.CYAN)
            start_time = time.time()
            script_module = importlib.import_module(f"scripts.{selected_script_value}")
            run_script(script_module)
            duration = time.time() - start_time

            print_section("✅ Completed", icon="✅", color=Fore.GREEN)
            print(f"{Fore.GREEN}⏱ Duration: {duration:.2f} seconds")
            input(f"\n{Fore.YELLOW}⏎ Press Enter to return to menu...")

        except ImportError:
            print_section("❌ Script not found", icon="🛑", color=Fore.RED)
            print(f"{Fore.RED}Script '{selected_script_value}' not found in /scripts/")
            input(f"\n{Fore.YELLOW}⏎ Press Enter to continue...")

        except Exception as e:
            print_section("❌ Error during execution", icon="🔥", color=Fore.RED)
            print(f"{Fore.RED}Error: {str(e)}")
            input(f"\n{Fore.YELLOW}⏎ Press Enter to continue...")

if __name__ == "__main__":
    main()
