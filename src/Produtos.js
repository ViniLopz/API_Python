import React from 'react';
import './Produtos.css'; // Arquivo de estilos separado

const CadastroProdutos = () => {
  return (
    <div className="content">
      <div className="formulario-cadastro">
        <h2>Cadastro de Produtos</h2>
        <div className="input-group">
          <label>Produto</label>
          <input type="text" placeholder="Nome do produto" />
        </div>
        <div className="input-group">
          <label>Custo (R$)</label>
          <input type="number" placeholder="0.00" />
        </div>
        <div className="button-group">
          <button>Cadastrar</button>
          <button>Limpar</button>
        </div>
        
        <h3>Lista de Produtos</h3>
        <div className="lista-produtos">
          <p>Nenhum produto adicionado</p>
        </div>
        
        {/* Botões de Salvar e Editar */}
        <div className="button-group">
          <button className="save-button">Salvar</button>
          <button className="edit-button">Editar</button>
        </div>
      </div>
    </div>
  );
};

export default CadastroProdutos;