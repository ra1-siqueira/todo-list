# Lista de Afazeres para Terminal

Programa em Python executado pelo terminal que permite criar, remover e fixar tarefas, além de outras funcionalidades adicionais. Cada funcionalidade é executada por comandos semelhantes aos comandos de terminal do Linux.

## Funcionalidades

- Criar uma tarefa, removê-la, marcar como concluída
- Fixar uma tarefa, o que faz com que ela suba para o topo da lista e não possa ser removida
- Marcar uma tarefa como `diária`, fazendo com que ela se atualize para `pendente` a cada novo dia

## Requisitos

- Python 3.10 ou superior

## Como usar

```bash
git clone https://github.com/ra1-siqueira/todo-list.git
cd todo-list
./todo
```

Os comandos disponíveis estão especificados no arquivo `info.txt`, que pode ser acessado dentro do programa digitando `info` e apertando `ENTER`.

As tarefas são gravadas em `todo.csv`. Caso queira apagar todas as tarefas manualmente nesse arquivo, não apague o cabeçalho, ou simplesmente descarte o arquivo (o programa vai criá-lo novamente).
