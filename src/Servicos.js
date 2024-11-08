import React from 'react';
import './Servicos.css'; // Arquivo de estilos separado

const CadastroServicos = () => {
  return (
    <div className="content">
      <div className="formulario-cadastro">
        <h2>Cadastro de Serviços</h2>
        <div className="input-group">
          <label>Serviços</label>
          <input type="text" placeholder="Nome do serviço" />
        </div>
        <div className="input-group">
          <label>Custo (R$)</label>
          <input type="number" placeholder="0.00" />
        </div>
        <div className="button-group">
          <button>Cadastrar</button>
          <button>Limpar</button>
        </div>
        <h3>Lista de Serviços</h3>
        <div className="lista-produtos">
          <p>Nenhum serviço adicionado</p>
        </div>
        <div className="button-group">
          <button className="save-button">Salvar</button>
          <button className="edit-button">Editar</button>
        </div>
      </div>
    </div>
  );
};

export default CadastroServicos;