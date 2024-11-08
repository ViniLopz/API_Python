from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi.middleware.cors import CORSMiddleware


# Configuração do FastAPI
app = FastAPI()

# Configurar as origens permitidas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Altere para a URL do seu front-end
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)

# Configuração do MySQL com SQLAlchemy
DATABASE_URL = "mysql+mysqlconnector://root:1234%40code@127.0.0.1:3306/pjoficina" 

# Conexão com o banco de dados
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos para o banco de dados
class ProdutoDB(Base):
    __tablename__ = 'produtos'
    id = Column("idProdutos", Integer, primary_key=True, autoincrement=True)
    nome = Column("Nome", String, nullable=False)
    valor_custo = Column("ValorCusto", Float, nullable=False)

class ServicoDB(Base):
    __tablename__ = "servicos"
    id = Column("idServicos", Integer, primary_key=True, autoincrement=True)
    tipo_servico = Column("TipoServico", String(45), nullable=False)
    valor_hora = Column("ValorHora", Float, nullable=False)

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Modelos de entrada para a API (sem o ID, que será gerado automaticamente pelo banco)
class Produto(BaseModel):
    nome: str
    valor_custo: float

class Servico(BaseModel):
    tipo_servico: str
    valor_hora: float

# Dependência para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- CRUD para Produtos ---
@app.get("/produtos", response_model=List[Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()

@app.post("/produtos", response_model=Produto)
def adicionar_produto(produto: Produto, db: Session = Depends(get_db)):
    db_produto = ProdutoDB(nome=produto.nome, valor_custo=produto.valor_custo)
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto_atualizado: Produto, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    db_produto.nome = produto_atualizado.nome
    db_produto.valor_custo = produto_atualizado.valor_custo
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.delete("/produtos/{produto_id}")
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    db_produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    db.delete(db_produto)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}

# --- CRUD para Serviços ---
@app.get("/servicos", response_model=List[Servico])
def listar_servicos(db: Session = Depends(get_db)):
    return db.query(ServicoDB).all()

@app.post("/servicos", response_model=Servico)
def adicionar_servico(servico: Servico, db: Session = Depends(get_db)):
    db_servico = ServicoDB(tipo_servico=servico.tipo_servico, valor_hora=servico.valor_hora)
    db.add(db_servico)
    db.commit()
    db.refresh(db_servico)
    return db_servico

@app.put("/servicos/{servico_id}", response_model=Servico)
def atualizar_servico(servico_id: int, servico_atualizado: Servico, db: Session = Depends(get_db)):
    db_servico = db.query(ServicoDB).filter(ServicoDB.id == servico_id).first()
    if not db_servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    db_servico.tipo_servico = servico_atualizado.tipo_servico
    db_servico.valor_hora = servico_atualizado.valor_hora
    db.commit()
    db.refresh(db_servico)
    return db_servico

@app.delete("/servicos/{servico_id}")
def deletar_servico(servico_id: int, db: Session = Depends(get_db)):
    db_servico = db.query(ServicoDB).filter(ServicoDB.id == servico_id).first()
    if not db_servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado.")
    db.delete(db_servico)
    db.commit()
    return {"detail": "Serviço deletado com sucesso"}
    

# --- Cálculo de Orçamento ---
class ProdutoOrcamento(BaseModel):
    id: int
    quantidade: int
    altura: float
    largura: float
    comprimento: float

class ServicoOrcamento(BaseModel):
    id: int
    horas_trabalhadas: int

class OrcamentoInput(BaseModel):
    produtos: List[ProdutoOrcamento]
    servicos: List[ServicoOrcamento]

@app.post("/calcular_orcamento/")
def calcular_orcamento(orcamento: OrcamentoInput, db: Session = Depends(get_db)):
    valor_total_produtos = 0.0
    valor_total_servicos = 0.0

    # Calcular o valor total dos produtos
    for produto_input in orcamento.produtos:
        produto_db = db.query(ProdutoDB).filter(ProdutoDB.id == produto_input.id).first()
        if not produto_db:
            raise HTTPException(status_code=404, detail=f"Produto com ID {produto_input.id} não encontrado.")

        # Cálculo usando o valor_custo do banco de dados multiplicado pela quantidade, altura, largura e comprimento
        custo_produto = (produto_input.quantidade * produto_db.valor_custo *
                         produto_input.altura * produto_input.largura * produto_input.comprimento)
        valor_total_produtos += round(custo_produto, 5)

    # Dividir o total de produtos por 10.000
    valor_total_produtos /= 10000

    # Calcular o valor total dos serviços
    for servico_input in orcamento.servicos:
        servico_db = db.query(ServicoDB).filter(ServicoDB.id == servico_input.id).first()
        if not servico_db:
            raise HTTPException(status_code=404, detail=f"Serviço com ID {servico_input.id} não encontrado.")
        
        custo_servico = servico_input.horas_trabalhadas * servico_db.valor_hora
        valor_total_servicos += round(custo_servico, 5)

    # Somando o valor total já arredondado para evitar erros de precisão
    valor_total = round(valor_total_produtos + valor_total_servicos, 5)

    return {
        "valor_total_produtos": valor_total_produtos,
        "valor_total_servicos": valor_total_servicos,
        "valor_total": valor_total
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
