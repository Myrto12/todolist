from flask import Flask, render_template,request,redirect,url_for
import json
from datetime import datetime
app = Flask(__name__)

'''def getTasks():
    with open('Tasks.json',encoding="utf8") as json_file:
       return json.load(json_file)'''
    
def getTasks(): #chatgpt
    try:
        with open('Tasks.json', encoding="utf8") as json_file:
            return json.load(json_file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []  # Επιστροφή κενής λίστας αν το αρχείο δεν υπάρχει ή είναι άκυρο
    
def addtask(task):
    Tasks = getTasks()
    Tasks.append(task)
    with open('Tasks.json','w',encoding="utf8") as json_file:
        return json.dump(Tasks,json_file,ensure_ascii=False)

def change_state(id):
    Tasks = getTasks()
    task = next(filter(lambda x: x['id'] == int(id), Tasks))
    task['state'] = abs(task['state'] - 1) 
    with open('Tasks.json','w',encoding="utf8") as json_file:
        return json.dump(Tasks,json_file,ensure_ascii=False)
    
    
def delete_task(id):
    Tasks = getTasks()
    Tasks = [task for task in Tasks if task['id'] != int(id)]  # List comprehension(chatgpt)s
    with open('Tasks.json', 'w', encoding="utf8") as json_file:
        json.dump(Tasks, json_file, ensure_ascii=False)
    

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        task_name = request.form.get('task_name','all')
        taskdict = {
            'id' : int(datetime.timestamp(datetime.now())),
            'name' : task_name,
            'state' : 0,
            'created at' : datetime.now().strftime("%d/%m/%Y, %H:%M:%S"),
            'deadline' : None
        }
        addtask(taskdict)
    return render_template('index.html',Tasks=getTasks())

@app.route('/change_state/<id>')
def change(id):
    change_state(id)
    return redirect(url_for('index'))

@app.route('/delete/<id>')
def delete(id):
    delete_task(id)
    return redirect(url_for('index'))
    
if __name__=='__main__':
    app.run(debug=True)

