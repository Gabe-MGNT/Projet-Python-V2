from app import app

app=app.get_dashboard()

if __name__ == "__main__":
    """Exécute le dashboard depuis le fichier 'app.py' dans le dossier 'app'"""
    app.run_server(debug=True)





