import React from 'react';
import './Orcamento.css'; // Arquivo de estilos separado

const Orcamento = () => {
  return (
    <div className="content">
      <div className="orcamento-container">
        <div className="top-row">
          {/* Quadro de Produto */}
          <div className="produto-box quadro">
            <h2>Produto</h2>
            <div className="input-group">
              <label>Produto</label>
              <input type="text" placeholder="Nome do Produto" />
            </div>
            <div className="produto-inputs">
              <div className="input-group">
                <label>Quantidade</label>
                <input type="number" placeholder="0" />
              </div>
              <div className="input-group">
                <label>Valor de Custo (R$)</label>
                <input type="number" placeholder="0.00" readOnly />
              </div>
              <div className="input-group">
                <label>Altura (cm)</label>
                <input type="number" placeholder="0.00" />
              </div>
              <div className="input-group">
                <label>Largura (cm)</label>
                <input type="number" placeholder="0.00" />
              </div>
              <div className="input-group">
                <label>Comprimento (m)</label>
                <input type="number" placeholder="0.00" />
              </div>
              <div className="input-group">
                <label>Valor do Item (R$)</label>
                <input type="number" placeholder="0.00" readOnly />
              </div>
            </div>
            <div className="button-group">
              <button className="add-button">Adicionar Produto</button>
              <button className="save-button">Limpar</button>
            </div>
          </div>
          {/* Quadro de Serviços */}
          <div className="servicos-box quadro">
            <h2>Serviços</h2>
            <div className="input-group">
              <label>Serviço</label>
              <input type="text" placeholder="Nome do Serviço" />
            </div>
            <div className="servico-inputs">
              <div className="input-group">
                <label>Hora(s)</label>
                <input type="number" placeholder="0" />
              </div>
              <div className="input-group">
                <label>Valor de Custo (R$)</label>
                <input type="number" placeholder="0.00" readOnly />
              </div>
            </div>
            <div className="button-group">
              <button className="add-button">Adicionar Serviço</button>
              <button className="save-button">Limpar</button>
            </div>
          </div>
        </div>
        {/* Quadro de Produtos Adicionados */}
        <div className="produtos-adicionados-box quadro">
          <h2>Lista de Produtos e/ou Serviços Adicionados</h2>
          <p className="mensagem-vazia">Nenhum Produto e/ou Serviços adicionados</p>
        </div>
        {/* Quadro de Total */}
        <div className="total-box quadro">
          <h2>Valor de Custo Total (R$)</h2>
          <input type="number" placeholder="0.00" readOnly />
        </div>
      </div>
    </div>
  );
};

export default Orcamento;
