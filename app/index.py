from app import app
from flask import session

@app.before_first_request
def clear_all_sessions():
    session.clear()  # Limpa a sessão atual de qualquer usuário
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)