from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # This is needed for sessions and security
    app.config['SECRET_KEY'] = 'dev-key-123' 

    # We will register your routes here in a second
    # For now, let's just define a simple route so it works
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    return app