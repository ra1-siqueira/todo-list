# Biblioteca padrao
import os
import sys
import readline

# Modulos do projeto
from terminal_ui import (
    clear_console,
    hide_cursor,
    wait_key,
    visible,
    centered,
    color_text,
    GREY,
    YELLOW,
    GREEN,
    RESET
)
from task_manager import TaskManager

def show_tasks(manager: TaskManager) -> None:
    clear_console()
    print()
    print()
    print()
    print(centered('TO DO:\n'))
    
    tasks = manager.get_tasks()
    if not tasks:
        return
    aux = max(len(t.name) for t in tasks) + 9
    for t in tasks:
        done      = 'ok'  if t.is_done   else '  '
        color     = GREY  if t.is_done   else ''
        show_pin  = '📌 ' if t.is_pinned else '   '
        show_dly  = '🗓️'  if t.is_daily  else ' '
        task_name = t.name 
        task_name = f'{task_name} '
        missing   = max(aux - len(task_name), 0)
        
        if t.is_done:
            task_name = color_text(task_name, GREY)
        dashes = color_text('-' * missing, GREY)
        
        display_line = (
            f'{show_dly}'
            f'{show_pin}'
            f'{task_name}'
            f'{dashes}'
            f'{color}[{done}]{RESET}'
            '  '
        )
        print(centered(display_line))

def display(manager: TaskManager) -> None:
    show_tasks(manager)
    print()
    print(centered(
        f'{GREY}Digite {YELLOW}info{RESET}{GREY} '
        f'para ver a lista de comandos.{RESET}'
    ))

def show_info(manager: TaskManager) -> None:
    clear_console()
    info = manager.get_info()
    formtd_info = info.format(YELLOW=YELLOW, RESET=RESET)
    print(formtd_info)
    print(
        f'\n  {GREY}Pressione {YELLOW}ENTER{RESET} '
        f'{GREY}para voltar...{RESET}'
    )
    wait_key()
    
def resolve_unknown(text: str) -> None:
    print(f"Erro: Comando '{text}' não existe.")
    hide_cursor(2)
 
def menu(option: list[str], manager: TaskManager) -> None:
    if len(option) > 1:
        task_name = option[1].upper()
    match option:
        case ['add', *_]:
            manager.create(task_name)
        case ['done', *_]:
            manager.toggle_done(task_name)
            manager.order_by_done()
            manager.order_by_pin('')
        case ['pin', *_] | ['unpin', *_]:
            manager.toggle_pin(task_name, option[0])
            manager.order_by_pin(task_name)
        case ['dly', *_]:
            manager.toggle_daily(task_name)
        case ['rm', *_]:
            manager.delete(task_name)
        case ['f-rm', *_]:
            manager.force_delete(task_name)
        case ['cl']:
            manager.delete_all()
        case ['f-cl']:
            manager.force_delete_all()
        case ['umrkall']:
            manager.mark_all_as_pending()
        case ['clhist']:
            manager.clear_history()
        case ['info']:
            show_info(manager)
        case ['rfsh']:
            return
        case ['ex']:
            clear_console()
            sys.exit()
        case _:
            resolve_unknown(option[0])

def main() -> None:
    clear_console()
    manager = TaskManager() 
    manager.load_history()
    while True:
        manager.update_daily_tasks()
        display(manager)
        user_input = input(
            f'\n\n{GREY}┌────({GREEN}user@todolist'
            f'{RESET}{GREY})\n└─┤{RESET} $ '
        )
        manager.update_history(user_input)
        command = user_input.split(' ', 1)
        menu(command, manager)
        
if __name__ == '__main__':
    main()
