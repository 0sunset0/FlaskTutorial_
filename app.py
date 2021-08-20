from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id
class Fcuser(db.Model): 
    __tablename__ = 'fcuser'   #테이블 이름 : fcuser
    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    password = db.Column(db.String(64))     #패스워드를 받아올 문자열길이 
    userid = db.Column(db.String(32))       #이하 위와 동일
    username = db.Column(db.String(8))

@app.route('/', methods=['POST','GET'])
def index():
    if request.method =='POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return '삭제할 수 없습니다.'

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method=='POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/') #메인으로 돌아감
        except:
            return '업데이트 할 수 없습니다'
    else:
        return render_template('update.html', task=task)

@app.route('/register', methods=['GET','POST']) #회원가입
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        #회원정보 생성
        userid = request.form.get('userid') 
        username = request.form.get('username')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password) # 들어오나 확인해볼 수 있다. 


        if not (userid and username and password and re_password) :
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        else: #모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
            fcuser = Fcuser()         
            fcuser.password = password           #models의 FCuser 클래스를 이용해 db에 입력한다.
            fcuser.userid = userid
            fcuser.username = username      
            db.session.add(fcuser)
            db.session.commit()
            #return "회원가입 완료"
            return render_template('register.html')

@app.route('/login', methods=['GET','POST']) #로그인
def login():  
    # form = LoginForm() #로그인 폼 생성
    # if form.validate_on_submit(): #유효성 검사
    #     session['userid'] = form.data.get('userid') #form에서 가져온 userid를 session에 저장
    
        
    #     return redirect('/') #로그인에 성공하면 홈화면으로 redirect
            
    return render_template('login.html')

if __name__ == "__main__":
    
    db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()

    app.run(debug=True)
    

