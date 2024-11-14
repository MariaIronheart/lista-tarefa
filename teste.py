import unittest
from flet import Page
from todo import ToDo  

class TestToDoUnit(unittest.TestCase):
    def setUp(self):
        # Cria uma página mock para teste
        self.page = Page()
        self.todo_app = ToDo(self.page)

    def test_adicionar_tarefa(self):
        # Simula a adição de uma tarefa
        self.todo_app.task = "Nova Tarefa"
        self.todo_app.add(None, None)  # None aqui simula o evento e o input_task
        tarefas = self.todo_app.db_execute('SELECT * FROM tasks')
        self.assertIn(("Nova Tarefa", "incomplete"), tarefas)

    def test_marcar_como_concluida(self):
        # Adiciona e marca a tarefa como concluída
        self.todo_app.db_execute('INSERT INTO tasks VALUES (?, ?)', ["Tarefa Teste", "incomplete"])
        checkbox_mock = type('', (), {})()
        checkbox_mock.label = "Tarefa Teste"
        checkbox_mock.value = True  # Marca como concluída

        self.todo_app.checked(checkbox_mock)
        tarefas = self.todo_app.db_execute('SELECT * FROM tasks WHERE name = ?', ["Tarefa Teste"])
        self.assertEqual(tarefas[0][1], "complete")

    def test_editar_tarefa(self):
        # Adiciona e edita o nome da tarefa
        self.todo_app.db_execute('INSERT INTO tasks VALUES (?, ?)', ["Tarefa Original", "incomplete"])
        self.todo_app.edit("Tarefa Original")
        self.todo_app.db_execute('UPDATE tasks SET name = ? WHERE name = ?', ["Tarefa Editada", "Tarefa Original"])
        
        tarefas = self.todo_app.db_execute('SELECT * FROM tasks WHERE name = ?', ["Tarefa Editada"])
        self.assertEqual(tarefas[0][0], "Tarefa Editada")

    def test_remover_tarefa(self):
        # Adiciona e remove uma tarefa
        self.todo_app.db_execute('INSERT INTO tasks VALUES (?, ?)', ["Tarefa para Remover", "incomplete"])
        self.todo_app.delete("Tarefa para Remover")
        
        tarefas = self.todo_app.db_execute('SELECT * FROM tasks WHERE name = ?', ["Tarefa para Remover"])
        self.assertEqual(len(tarefas), 0)

if __name__ == '__main__':
    unittest.main()


#TESTE DE INTEGRAÇÃO
class TestToDoIntegration(unittest.TestCase):
    def setUp(self):
        self.page = Page()
        self.todo_app = ToDo(self.page)

    def test_fluxo_completo(self):
        # Adiciona uma tarefa
        self.todo_app.task = "Tarefa Completa"
        self.todo_app.add(None, None)
        
        # Marca como concluída
        checkbox_mock = type('', (), {})()
        checkbox_mock.label = "Tarefa Completa"
        checkbox_mock.value = True
        self.todo_app.checked(checkbox_mock)

        # Edita a tarefa
        self.todo_app.edit("Tarefa Completa")
        self.todo_app.db_execute('UPDATE tasks SET name = ? WHERE name = ?', ["Tarefa Editada", "Tarefa Completa"])

        # Filtra e verifica a tarefa como concluída
        tarefas = self.todo_app.db_execute('SELECT * FROM tasks WHERE status = "complete"')
        self.assertTrue(any(tarefa[0] == "Tarefa Editada" for tarefa in tarefas))

if __name__ == '__main__':
    unittest.main()


#TESTE DE SISTEMA
class TestToDoSystem(unittest.TestCase):
    def setUp(self):
        self.page = Page()
        self.todo_app = ToDo(self.page)

    def test_uso_completo(self):
        # Adiciona várias tarefas
        self.todo_app.task = "Estudar Python"
        self.todo_app.add(None, None)
        
        self.todo_app.task = "Praticar SQL"
        self.todo_app.add(None, None)

        # Marca a primeira tarefa como concluída
        checkbox_mock = type('', (), {})()
        checkbox_mock.label = "Estudar Python"
        checkbox_mock.value = True
        self.todo_app.checked(checkbox_mock)

        # Filtra e verifica as tarefas concluídas e não concluídas
        concluida = self.todo_app.db_execute('SELECT * FROM tasks WHERE status = "complete"')
        nao_concluida = self.todo_app.db_execute('SELECT * FROM tasks WHERE status = "incomplete"')
        
        self.assertEqual(len(concluida), 1)
        self.assertEqual(len(nao_concluida), 1)
        self.assertEqual(concluida[0][0], "Estudar Python")
        self.assertEqual(nao_concluida[0][0], "Praticar SQL")

if __name__ == '__main__':
    unittest.main()
