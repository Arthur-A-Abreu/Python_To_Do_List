from flask import Flask, render_template, request, redirect, url_for
import sqlite3

#Cria o app
app = Flask(__name__)

#Função para conectar ao banco de dados
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

#Ciar tabela se não existir
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS task (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()
print("Banco e tabela verificados")


#Define uma rota
# GET and POST to do a Point Between the Client and the Server
@app.route('/',methods=['GET', 'POST'])
def home():
    conn = get_db_connection()

    if request.method == 'POST':
        task = request.form['task']
        conn.execute('INSERT INTO task (name) VALUES (?)', (task,))
        conn.commit()
        return redirect('/')

    tasks = conn.execute('SELECT * FROM task').fetchall()
    conn.close()


    return render_template('index.html', tasks=tasks)


#Deletar tarefas
@app.route("/delete/<int:id>")
def delete_task(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM task WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

#Edit the Task
@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()

    if request.method == 'POST':
        new_name = request.form["task"]
        conn.execute(
            "UPDATE task SET name = ? WHERE id = ?",
            (new_name, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("home"))
    
    task = conn.execute(
        "SELECT * FROM task WHERE id = ?",
        (id,)  
    ).fetchone()
    conn.close()

    return render_template("edit.html", task=task)

if __name__ == '__main__':

    app.run(debug=True)
