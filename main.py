# --Importacoes--
import csv
import os
import shutil
import re
import unicodedata
import sys
from datetime import date

# --CONSTANTES--
FILE    = 'todo.csv'
TMP     = 'todo.temp'
HEADER  = ['task', 'done', 'date', 'pin', 'daily']
WIDTH   = shutil.get_terminal_size().columns # largura do terminal

YELLOW        = '\033[33m'
GREEN         = '\033[32m'
BRIGHT_GREEN  = '\033[92m'
GREY          = '\033[90m'
RESET         = '\033[0m'


def visible(text):
    colorless = re.sub(r'\033\[[0-9;]*m', '', text)
    extras = sum(1 for c in colorless if unicodedata.east_asian_width(c) in ('W', 'F'))
    return len(colorless) + extras


def centering(text, width=WIDTH):
    space = max(width - visible(text), 0)
    return ' ' * (space // 2) + text


def color_text(text, color=GREY):
    return color + text + RESET


def create(task, is_done=False, is_pinned=False, is_daily=False):
    is_new = not os.path.exists(FILE)

    with open(FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        
        # se o arquivo acabou de ser criado, insere o HEADER no topo
        if is_new:
            writer.writerow(HEADER)

        writer.writerow([task, is_done, date.today(), is_pinned, is_daily])


def read_all():
    os.system('clear')

    print(f'\n\n')
    print(centering(f'TO DO:\n'))

    with open(FILE, newline='') as f:
        task_list = csv.reader(f)
        next(task_list) # pula o HEADER

        tasks = [t for t in task_list if t]

        # se a lista estiver vazia, encerra a execucao da funcao
        if not tasks:
            return

        # modifica dinamicamente a quantidade de tracos printados
        aux = max(len(t[0]) for t in tasks) + 9

        for task in tasks:
            is_done = task[1]   == 'True'
            is_pinned = task[3] == 'True'
            is_daily = task[4]  == 'True'

            done       = 'ok'       if is_done   else '  '
            color      = '\033[90m' if is_done   else ''
            show_pin   = '📌 '      if is_pinned else '   '
            show_daily = '🗓️'       if is_daily  else ' '

            task_name = f'{task[0]} '
            missing = max(aux - len(task_name), 0)

            if is_done:
                task_name = color_text(task_name, GREY)

            dashes = color_text('-' * missing, GREY)

            display_line = (
                f'{show_daily}'
                f'{show_pin}'
                f'{task_name}'
                f'{dashes}'
                f'{color}[{done}]{RESET}'
                '    '
            )

            print(centering(display_line))


def update_is_done(task):
    with open(FILE, newline='') as src, open(TMP, 'w', newline='') as dst:
        task_list = csv.reader(src)
        writer = csv.writer(dst)

        writer.writerow(HEADER)
        next(task_list, None)

        for t in task_list:
            if t and t[0] == task:
                done = t[1] == 'True'
                #    task  done      date          pin   daily
                t = [t[0], not done, date.today(), t[3], t[4]] # inverte o booleano done

            writer.writerow(t) # reescreve o arquivo com o campo atualizado

    os.replace(TMP, FILE)


def update_is_pinned(task):
    with open(FILE, newline='') as src, open(TMP, 'w', newline='') as dst:
        task_list = csv.reader(src)
        writer = csv.writer(dst)

        writer.writerow(HEADER)
        next(task_list, None)

        for t in task_list:
            if t and t[0] == task:
                pinned = t[3] == 'True'
                #    task  done  date  pin         daily
                t = [t[0], t[1], t[2], not pinned, t[4]] # inverte o booleano pinned

            writer.writerow(t) # reescreve o arquivo com o campo atualizado

    os.replace(TMP, FILE)


def pinned_tasks_first(recently_pinned):
    pinned_tasks = []
    not_pinned_tasks = []

    with open(FILE, newline='') as src:
        task_list = csv.reader(src)
        next(task_list, None)

        for task in task_list:
            pinned = task[3] == 'True'
            if pinned and task[0] == recently_pinned:
                pinned_tasks.append(task)

            elif task[0] == recently_pinned:
                not_pinned_tasks.append(task)

    with open(FILE, newline='') as src:
        task_list = csv.reader(src)
        next(task_list, None)

        for task in task_list:
            pinned = task[3] == 'True'
            if pinned and task[0] != recently_pinned:
                pinned_tasks.append(task)
                
            elif task[0] != recently_pinned:
                not_pinned_tasks.append(task)
 
    with open(TMP, 'w', newline='') as dst:
        writer = csv.writer(dst)
        writer.writerow(HEADER)
        writer.writerows(pinned_tasks)
        writer.writerows(not_pinned_tasks)

    os.replace(TMP, FILE)


def update_is_daily(task):
    with open(FILE, newline='') as src, open(TMP, 'w', newline='') as dst:
        task_list = csv.reader(src)
        writer = csv.writer(dst)

        writer.writerow(HEADER)
        next(task_list, None)

        for t in task_list:
            if t and t[0] == task:
                daily = t[4] == 'True'
                #    task  done  date          pin   daily
                t = [t[0], t[1], date.today(), t[3], not daily] # inverte o booleano daily

            writer.writerow(t) # reescreve o arquivo com o campo atualizado

    os.replace(TMP, FILE) 


def delete(task):
    with open(FILE, newline='') as src, open(TMP, 'w', newline='') as dst:
        task_list = csv.reader(src)
        writer = csv.writer(dst)

        writer.writerow(HEADER)
        next(task_list, None)

        for t in task_list:
            pinned = t[3] == 'True'
            # nao escreve a tarefa que deve ser apagada,
            # a nao ser que ela esteja fixada
            if t[0] != task or pinned:
                writer.writerow(t)

    os.replace(TMP, FILE) 


def delete_all():
    with open(FILE, newline='') as src, open(TMP, 'w', newline='') as dst:
        task_list = csv.reader(src)
        writer = csv.writer(dst)

        writer.writerow(HEADER)
        next(task_list, None)

        for t in task_list:
            pinned = t[3] == 'True'
            if pinned:
                writer.writerow(t)

    os.replace(TMP, FILE)


def unmark_tasks():
    with open(FILE, newline='') as src, open(TMP, 'w', newline='') as dst:
        task_list = csv.reader(src)
        writer = csv.writer(dst)

        writer.writerow(HEADER)
        next(task_list, None)

        for task in task_list:
            if task[1] == 'True':
                #       task     done   date          pin      daily  
                task = [task[0], False, date.today(), task[3], task[4]]

            writer.writerow(task)

    os.replace(TMP, FILE)


def show_info():
    os.system('clear')

    with open('info.txt', encoding='utf-8') as f:
        info = f.read()

    formtd_info = info.format(YELLOW=YELLOW, RESET=RESET)
    print(formtd_info)

    input(f'\n  {GREY}Pressione {YELLOW}ENTER{RESET} {GREY}para voltar...{RESET}')


def menu(option):
    match option:
        case ['info']:
            show_info()
            display()

        case ['add', *_]:
            create(option[1].upper())
            display()

        case ['rmv', *_]:
            delete(option[1].upper())
            display()
            
        case ['done', *_]:
            update_is_done(option[1].upper())
            display()

        case ['pin', *_]:
            update_is_pinned(option[1].upper())
            pinned_tasks_first(option[1].upper())
            display()

        case ['dly', *_]:
            update_is_daily(option[1].upper())
            display()
        
        case ['cl']:
            delete_all()
            display()

        case ['umrkall']:
            unmark_tasks()
            display()

        case ['rfsh']:
            return

        case ['ex']:
            sys.exit()


def display():
    read_all()
    print('')
    print(centering(
        f'{GREY}Digite {YELLOW}info{RESET}{GREY} '
        f'para ver a lista de comandos.{RESET}'
    ))


def update_daily_tasks():
    daily_tasks = []
    current_day = str(date.today())
    is_new = not os.path.exists(FILE)

    with open(FILE, 'r+', newline='') as f:
        writer = csv.writer(f)
        task_list = csv.reader(f)
        
        if is_new:
            writer.writerow(HEADER)
        
        tasks = [t for t in task_list if t]

        # se a lista estiver vazia, encerra a execucao da funcao
        if not tasks:
            return

        for task in tasks:
            daily = task[4] == 'True'
            if daily:
                is_done = task[1]  == 'True'
                task_day = task[2]

                daily_tasks.append((task[0], is_done, task_day))

    # a cada novo dia, se a tarefa foi concluida
    # no dia anterior, ela volta a estar pendente
    for task_name, is_done, task_day in daily_tasks:
        if is_done and task_day != current_day:
            update_is_done(task_name)


def main():
    os.system('clear')

    while(True):
        update_daily_tasks()
        display()

        user_input = input(
            f'\n\n{GREY}┌────({GREEN}user@todolist'
            f'{RESET}{GREY})\n└─┤{RESET} $ '
        ).split(' ', 1)

        menu(user_input)


if __name__ == '__main__':
    main()