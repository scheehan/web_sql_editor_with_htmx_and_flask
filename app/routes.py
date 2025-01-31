from app import app
from flask import render_template, request, redirect, url_for

from app.db import get_db


@app.route('/')
def index():
    
    conn = get_db()
    
    myposts = conn.execute('''
                          SELECT * FROM users;
                          ''').fetchall()
    conn.close()
    
    return render_template('index.html', myposts=myposts)

@app.route('/delete/<int:number>', methods=['GET', 'POST'])
def delete(number):

    conn = get_db()
    cur = conn.cursor()
        
    cur.execute("DELETE FROM users WHERE id = ?", (number,))

    conn.commit()
    
    conn.close()

    return redirect('/') 


@app.route('/edit/<int:number>', methods=['GET', 'POST'])
def edit(number):
    
    conn = get_db()
    cur = conn.cursor()
    
    if request.method == 'POST':
        item_id      = number
        item_name    = request.form['username']
        item_ext  = request.form['ext']
        item_email = request.form['email']
        
        
        if request.headers['HX-Prompt'] == 'Yes':

            cur.execute('UPDATE users SET username = ?, ext = ?, email = ?'
                            ' WHERE id = ?',
                            (item_name, item_ext, item_email, item_id))
            conn.commit()

            return redirect('/')
        
        edit = conn.execute('SELECT * FROM users WHERE id = ?', (number,)).fetchone()
        conn.close()
    
        return redirect('/')

    
            
    edit = conn.execute('SELECT * FROM users WHERE id = ?', (number,)).fetchone()
    conn.close()
    
    return render_template('edit.html', edit=edit)


@app.route('/add', methods=['GET', 'POST'])
def add():
    conn = get_db()
    cur = conn.cursor()

    if request.method == 'POST':
        item_name    = request.form['username']
        item_ext  = request.form['ext']
        item_email = request.form['email']
        
        cur.execute("""INSERT INTO users (username, ext, email) VALUES (?, ?, ?)""", 
                    (item_name, item_ext, item_email))
        conn.commit()
        
        return redirect('/') 
    
    return render_template("add.html")


@app.route('/test')
def mytest():
    return render_template("test.html")
