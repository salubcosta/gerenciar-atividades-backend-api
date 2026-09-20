from flask_openapi3 import OpenAPI, Tag, Info
from flask_cors import CORS
from flask import redirect
from database.database import Base, engine
from routes.categoria_routes import categoria_bp
from routes.projeto_routes import projeto_bp
from routes.registro_routes import registro_bp
from routes.pessoa_routes import pessoa_bp

# Cria todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

info = Info(title="API Gerenciamento de Atividades por Projeto", version="1.0.0")

app = OpenAPI(__name__, info=info)

# Permite que os endpoints sejam consumidos por frontend externo
CORS(app=app)

# Registra os blueprints
app.register_api(categoria_bp)
app.register_api(projeto_bp)
app.register_api(registro_bp)
app.register_api(pessoa_bp)


redirect_tag = Tag(name="Redirecionamento", description="Redirecionamento automático para docs do OpenAPI")
@app.get("/", tags=[redirect_tag])
def home():
    """
    Rota para redirecionamento
    """
    return redirect("/openapi/swagger")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )