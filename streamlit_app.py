import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# Classes para as entidades
class MaoDeObra:
    def __init__(self):
        self.file_path = 'maos_de_obra.json'
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            data = pd.read_json(self.file_path)
            data['Custo_Hora'] = data['Custo_Hora'].astype(float)
            return data
        else:
            return pd.DataFrame(columns=['Nome', 'Custo_Hora'])
    
    def save_data(self):
        self.data.to_json(self.file_path, orient='records', indent=4)
    
    def adicionar(self, nome, custo_hora):
        novo_registro = pd.DataFrame({'Nome': [nome], 'Custo_Hora': [custo_hora]})
        self.data = pd.concat([self.data, novo_registro], ignore_index=True)
        self.save_data()
    
    def atualizar(self, index, nome, custo_hora):
        self.data.at[index, 'Nome'] = nome
        self.data.at[index, 'Custo_Hora'] = custo_hora
        self.save_data()
    
    def remover(self, index):
        self.data = self.data.drop(index).reset_index(drop=True)
        self.save_data()
    
    def visualizar(self):
        st.dataframe(self.data.style.set_properties(**{'text-align': 'left'}))

class MateriaPrima:
    def __init__(self):
        self.file_path = 'materias_primas.json'
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            data = pd.read_json(self.file_path)
            data['Custo_Unidade'] = data['Custo_Unidade'].astype(float)
            return data
        else:
            return pd.DataFrame(columns=['Nome', 'Custo_Unidade'])
    
    def save_data(self):
        self.data.to_json(self.file_path, orient='records', indent=4)
    
    def adicionar(self, nome, custo_unidade):
        novo_registro = pd.DataFrame({'Nome': [nome], 'Custo_Unidade': [custo_unidade]})
        self.data = pd.concat([self.data, novo_registro], ignore_index=True)
        self.save_data()
    
    def atualizar(self, index, nome, custo_unidade):
        self.data.at[index, 'Nome'] = nome
        self.data.at[index, 'Custo_Unidade'] = custo_unidade
        self.save_data()
    
    def remover(self, index):
        self.data = self.data.drop(index).reset_index(drop=True)
        self.save_data()
    
    def visualizar(self):
        st.dataframe(self.data.style.set_properties(**{'text-align': 'left'}))

class Imposto:
    def __init__(self):
        self.file_path = 'impostos.json'
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            data = pd.read_json(self.file_path)
            data['Percentual'] = data['Percentual'].astype(float)
            return data
        else:
            return pd.DataFrame(columns=['Estado', 'Percentual'])
    
    def save_data(self):
        self.data.to_json(self.file_path, orient='records', indent=4)
    
    def adicionar(self, estado, percentual):
        novo_registro = pd.DataFrame({'Estado': [estado], 'Percentual': [percentual]})
        self.data = pd.concat([self.data, novo_registro], ignore_index=True)
        self.save_data()
    
    def atualizar(self, index, estado, percentual):
        self.data.at[index, 'Estado'] = estado
        self.data.at[index, 'Percentual'] = percentual
        self.save_data()
    
    def remover(self, index):
        self.data = self.data.drop(index).reset_index(drop=True)
        self.save_data()
    
    def visualizar(self):
        st.dataframe(self.data.style.set_properties(**{'text-align': 'left'}))

class Produto:
    def __init__(self):
        self.file_path = 'produtos.json'
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.file_path):
            # Carregar dados e converter colunas de dicionários
            data = pd.read_json(self.file_path)
            if not data.empty:
                data['Maos_de_Obra'] = data['Maos_de_Obra'].apply(lambda x: json.loads(x))
                data['Materias_Primas'] = data['Materias_Primas'].apply(lambda x: json.loads(x))
            else:
                data = pd.DataFrame(columns=['Nome', 'Maos_de_Obra', 'Materias_Primas'])
            return data
        else:
            return pd.DataFrame(columns=['Nome', 'Maos_de_Obra', 'Materias_Primas'])
    
    def save_data(self):
        # Converter colunas de dicionários para strings JSON
        data_to_save = self.data.copy()
        data_to_save['Maos_de_Obra'] = data_to_save['Maos_de_Obra'].apply(lambda x: json.dumps(x))
        data_to_save['Materias_Primas'] = data_to_save['Materias_Primas'].apply(lambda x: json.dumps(x))
        data_to_save.to_json(self.file_path, orient='records', indent=4)
    
    def adicionar(self, nome, maos_de_obra, materias_primas):
        novo_registro = pd.DataFrame({
            'Nome': [nome],
            'Maos_de_Obra': [maos_de_obra],
            'Materias_Primas': [materias_primas]
        })
        self.data = pd.concat([self.data, novo_registro], ignore_index=True)
        self.save_data()
    
    def atualizar(self, index, nome, maos_de_obra, materias_primas):
        self.data.at[index, 'Nome'] = nome
        self.data.at[index, 'Maos_de_Obra'] = maos_de_obra
        self.data.at[index, 'Materias_Primas'] = materias_primas
        self.save_data()
    
    def remover(self, index):
        self.data = self.data.drop(index).reset_index(drop=True)
        self.save_data()
    
    def visualizar(self):
        st.dataframe(self.data.style.set_properties(**{'text-align': 'left'}))

class Aplicativo:
    def __init__(self):
        self.mao_de_obra = MaoDeObra()
        self.materia_prima = MateriaPrima()
        self.imposto = Imposto()
        self.produto = Produto()
    
    def run(self):
        st.set_page_config(page_title="Precificação de Venda", page_icon="💰", layout="wide")
        st.title('💰 Webapp de Precificação de Venda')
        
        # Menu na barra lateral
        menu_options = ['Dashboard', 'Mão de Obra', 'Matérias-Primas', 'Produtos', 'Impostos', 'Calcular Preço']
        st.sidebar.title('Menu')
        st.sidebar.markdown('Selecione uma opção:')
        
        # Adicionar botão para limpar a sessão (opcional)
        if st.sidebar.button('Limpar Sessão'):
            st.session_state.clear()
            st.experimental_rerun()
        
        # Verificar se 'page' está no session_state e é válido
        if 'page' not in st.session_state or st.session_state.page not in menu_options:
            st.session_state.page = 'Dashboard'
        
        # Atualização: Fornecer um label significativo e ocultá-lo se desejado
        choice = st.sidebar.radio(
            'Navegação',  # Label significativo
            menu_options,
            index=menu_options.index(st.session_state.page),
            label_visibility='collapsed'  # Oculta o label, mas mantém para acessibilidade
        )
        st.session_state.page = choice
    
        if st.session_state.page == 'Dashboard':
            self.dashboard()
        elif st.session_state.page == 'Mão de Obra':
            self.gestao_mao_de_obra()
        elif st.session_state.page == 'Matérias-Primas':
            self.gestao_materias_primas()
        elif st.session_state.page == 'Produtos':
            self.gestao_produtos()
        elif st.session_state.page == 'Impostos':
            self.gestao_impostos()
        elif st.session_state.page == 'Calcular Preço':
            self.calcular_preco()
    
    def dashboard(self):
        st.header('📊 Dashboard')
        # Exemplo de gráficos e tabelas
        st.subheader('Resumo dos Dados')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Total de Mão de Obra', len(self.mao_de_obra.data))
        with col2:
            st.metric('Total de Matérias-Primas', len(self.materia_prima.data))
        with col3:
            st.metric('Total de Produtos', len(self.produto.data))
        
        # Ajustando para mais colunas
        st.subheader('Custos de Mão de Obra e Matérias-Primas')
        col1, col2 = st.columns(2)
        with col1:
            if not self.mao_de_obra.data.empty:
                fig_mao = px.bar(self.mao_de_obra.data, x='Nome', y='Custo_Hora', title='Custo por Hora de Mão de Obra')
                st.plotly_chart(fig_mao, use_container_width=True)
            else:
                st.info('Nenhuma Mão de Obra cadastrada.')
        with col2:
            if not self.materia_prima.data.empty:
                fig_materia = px.bar(self.materia_prima.data, x='Nome', y='Custo_Unidade', title='Custo por Unidade de Matérias-Primas')
                st.plotly_chart(fig_materia, use_container_width=True)
            else:
                st.info('Nenhuma Matéria-Prima cadastrada.')
        
        st.subheader('Produtos Cadastrados')
        if not self.produto.data.empty:
            st.dataframe(self.produto.data[['Nome']])
        else:
            st.info('Nenhum Produto cadastrado.')
    
    def gestao_mao_de_obra(self):
        st.header('👷 Gestão de Mão de Obra')
        tabs = st.tabs(['Adicionar', 'Atualizar', 'Remover', 'Visualizar'])

        with tabs[0]:
            st.subheader('Adicionar Mão de Obra')
            with st.form('Adicionar Mão de Obra'):
                nome = st.text_input('Nome da Mão de Obra')
                custo = st.number_input('Custo por Hora', min_value=0.0, step=0.01)
                submit = st.form_submit_button('Adicionar')
                if submit:
                    self.mao_de_obra.adicionar(nome, custo)
                    st.success('Mão de Obra adicionada com sucesso!')

        with tabs[1]:
            st.subheader('Atualizar Mão de Obra')
            if not self.mao_de_obra.data.empty:
                indices = self.mao_de_obra.data.index.tolist()
                index = st.selectbox('Selecione a Mão de Obra', indices, format_func=lambda x: self.mao_de_obra.data.iloc[x]['Nome'])
                nome = st.text_input('Novo Nome', value=self.mao_de_obra.data.iloc[index]['Nome'])
                custo = st.number_input(
                    'Novo Custo por Hora',
                    min_value=0.0,
                    step=0.01,
                    value=float(self.mao_de_obra.data.iloc[index]['Custo_Hora'])
                )
                if st.button('Atualizar'):
                    self.mao_de_obra.atualizar(index, nome, custo)
                    st.success('Mão de Obra atualizada com sucesso!')
            else:
                st.info('Nenhuma Mão de Obra cadastrada.')

        with tabs[2]:
            st.subheader('Remover Mão de Obra')
            if not self.mao_de_obra.data.empty:
                indices = self.mao_de_obra.data.index.tolist()
                index = st.selectbox('Selecione a Mão de Obra para remover', indices, format_func=lambda x: self.mao_de_obra.data.iloc[x]['Nome'])
                if st.button('Remover'):
                    self.mao_de_obra.remover(index)
                    st.success('Mão de Obra removida com sucesso!')
            else:
                st.info('Nenhuma Mão de Obra cadastrada.')

        with tabs[3]:
            st.subheader('Lista de Mão de Obra')
            self.mao_de_obra.visualizar()

    def gestao_materias_primas(self):
        st.header('🧱 Gestão de Matérias-Primas')
        tabs = st.tabs(['Adicionar', 'Atualizar', 'Remover', 'Visualizar'])

        with tabs[0]:
            st.subheader('Adicionar Matéria-Prima')
            with st.form('Adicionar Matéria-Prima'):
                nome = st.text_input('Nome da Matéria-Prima')
                custo = st.number_input('Custo por Unidade', min_value=0.0, step=0.01)
                submit = st.form_submit_button('Adicionar')
                if submit:
                    self.materia_prima.adicionar(nome, custo)
                    st.success('Matéria-Prima adicionada com sucesso!')

        with tabs[1]:
            st.subheader('Atualizar Matéria-Prima')
            if not self.materia_prima.data.empty:
                indices = self.materia_prima.data.index.tolist()
                index = st.selectbox('Selecione a Matéria-Prima', indices, format_func=lambda x: self.materia_prima.data.iloc[x]['Nome'])
                nome = st.text_input('Novo Nome', value=self.materia_prima.data.iloc[index]['Nome'])
                custo = st.number_input(
                    'Novo Custo por Unidade',
                    min_value=0.0,
                    step=0.01,
                    value=float(self.materia_prima.data.iloc[index]['Custo_Unidade'])
                )
                if st.button('Atualizar'):
                    self.materia_prima.atualizar(index, nome, custo)
                    st.success('Matéria-Prima atualizada com sucesso!')
            else:
                st.info('Nenhuma Matéria-Prima cadastrada.')

        with tabs[2]:
            st.subheader('Remover Matéria-Prima')
            if not self.materia_prima.data.empty:
                indices = self.materia_prima.data.index.tolist()
                index = st.selectbox('Selecione a Matéria-Prima para remover', indices, format_func=lambda x: self.materia_prima.data.iloc[x]['Nome'])
                if st.button('Remover'):
                    self.materia_prima.remover(index)
                    st.success('Matéria-Prima removida com sucesso!')
            else:
                st.info('Nenhuma Matéria-Prima cadastrada.')

        with tabs[3]:
            st.subheader('Lista de Matérias-Primas')
            self.materia_prima.visualizar()

    def gestao_impostos(self):
        st.header('💲 Gestão de Impostos por Estado')
        tabs = st.tabs(['Adicionar', 'Atualizar', 'Remover', 'Visualizar'])

        with tabs[0]:
            st.subheader('Adicionar Imposto')
            with st.form('Adicionar Imposto'):
                estado = st.text_input('Estado')
                percentual = st.number_input('Percentual de Imposto (%)', min_value=0.0, step=0.01)
                submit = st.form_submit_button('Adicionar')
                if submit:
                    self.imposto.adicionar(estado, percentual)
                    st.success('Imposto adicionado com sucesso!')

        with tabs[1]:
            st.subheader('Atualizar Imposto')
            if not self.imposto.data.empty:
                indices = self.imposto.data.index.tolist()
                index = st.selectbox('Selecione o Imposto', indices, format_func=lambda x: self.imposto.data.iloc[x]['Estado'])
                estado = st.text_input('Novo Estado', value=self.imposto.data.iloc[index]['Estado'])
                percentual = st.number_input(
                    'Novo Percentual de Imposto (%)',
                    min_value=0.0,
                    step=0.01,
                    value=float(self.imposto.data.iloc[index]['Percentual'])
                )
                if st.button('Atualizar'):
                    self.imposto.atualizar(index, estado, percentual)
                    st.success('Imposto atualizado com sucesso!')
            else:
                st.info('Nenhum Imposto cadastrado.')

        with tabs[2]:
            st.subheader('Remover Imposto')
            if not self.imposto.data.empty:
                indices = self.imposto.data.index.tolist()
                index = st.selectbox('Selecione o Imposto para remover', indices, format_func=lambda x: self.imposto.data.iloc[x]['Estado'])
                if st.button('Remover'):
                    self.imposto.remover(index)
                    st.success('Imposto removido com sucesso!')
            else:
                st.info('Nenhum Imposto cadastrado.')

        with tabs[3]:
            st.subheader('Lista de Impostos')
            self.imposto.visualizar()

    def gestao_produtos(self):
        st.header('📦 Gestão de Produtos')
        tabs = st.tabs(['Adicionar', 'Atualizar', 'Remover', 'Visualizar'])

        with tabs[0]:
            st.subheader('Adicionar Produto')
            with st.form('Adicionar Produto'):
                nome = st.text_input('Nome do Produto')
                st.markdown('**Selecionar Mão de Obra Necessária**')
                maos_de_obra_selecionadas = st.multiselect('Mãos de Obra', self.mao_de_obra.data['Nome'])
                horas = {}
                for mao in maos_de_obra_selecionadas:
                    hora = st.number_input(f'Horas para {mao}', min_value=0.0, step=0.01)
                    horas[mao] = hora
                st.markdown('**Selecionar Matérias-Primas Necessárias**')
                materias_primas_selecionadas = st.multiselect('Matérias-Primas', self.materia_prima.data['Nome'])
                quantidades = {}
                for materia in materias_primas_selecionadas:
                    quantidade = st.number_input(f'Quantidade de {materia}', min_value=0.0, step=0.01)
                    quantidades[materia] = quantidade
                submit = st.form_submit_button('Adicionar')
                if submit:
                    self.produto.adicionar(nome, horas, quantidades)
                    st.success('Produto adicionado com sucesso!')

        with tabs[1]:
            st.subheader('Atualizar Produto')
            if not self.produto.data.empty:
                indices = self.produto.data.index.tolist()
                index = st.selectbox('Selecione o Produto', indices, format_func=lambda x: self.produto.data.iloc[x]['Nome'])
                produto = self.produto.data.iloc[index]
                nome = st.text_input('Novo Nome', value=produto['Nome'])
                st.markdown('**Atualizar Mão de Obra Necessária**')
                maos_de_obra_selecionadas = st.multiselect('Mãos de Obra', self.mao_de_obra.data['Nome'], default=list(produto['Maos_de_Obra'].keys()))
                horas = {}
                for mao in maos_de_obra_selecionadas:
                    hora = st.number_input(
                        f'Horas para {mao}',
                        min_value=0.0,
                        step=0.01,
                        value=float(produto['Maos_de_Obra'].get(mao, 0))
                    )
                    horas[mao] = hora
                st.markdown('**Atualizar Matérias-Primas Necessárias**')
                materias_primas_selecionadas = st.multiselect('Matérias-Primas', self.materia_prima.data['Nome'], default=list(produto['Materias_Primas'].keys()))
                quantidades = {}
                for materia in materias_primas_selecionadas:
                    quantidade = st.number_input(
                        f'Quantidade de {materia}',
                        min_value=0.0,
                        step=0.01,
                        value=float(produto['Materias_Primas'].get(materia, 0))
                    )
                    quantidades[materia] = quantidade
                if st.button('Atualizar'):
                    self.produto.atualizar(index, nome, horas, quantidades)
                    st.success('Produto atualizado com sucesso!')
            else:
                st.info('Nenhum Produto cadastrado.')

        with tabs[2]:
            st.subheader('Remover Produto')
            if not self.produto.data.empty:
                indices = self.produto.data.index.tolist()
                index = st.selectbox('Selecione o Produto para remover', indices, format_func=lambda x: self.produto.data.iloc[x]['Nome'])
                if st.button('Remover'):
                    self.produto.remover(index)
                    st.success('Produto removido com sucesso!')
            else:
                st.info('Nenhum Produto cadastrado.')

        with tabs[3]:
            st.subheader('Lista de Produtos')
            self.produto.visualizar()

    def calcular_preco(self):
        st.header('🧮 Calcular Preço Final do Produto')
        if not self.produto.data.empty:
            indices = self.produto.data.index.tolist()
            index_produto = st.selectbox('Selecione o Produto', indices, format_func=lambda x: self.produto.data.iloc[x]['Nome'])
            produto = self.produto.data.iloc[index_produto]

            # Calcular custo de mão de obra
            custo_mao_de_obra = 0
            for mao, horas in produto['Maos_de_Obra'].items():
                custo_hora = self.mao_de_obra.data[self.mao_de_obra.data['Nome'] == mao]['Custo_Hora'].values[0]
                custo_mao_de_obra += custo_hora * horas

            # Calcular custo de matérias-primas
            custo_materias_primas = 0
            for materia, quantidade in produto['Materias_Primas'].items():
                custo_unidade = self.materia_prima.data[self.materia_prima.data['Nome'] == materia]['Custo_Unidade'].values[0]
                custo_materias_primas += custo_unidade * quantidade

            custo_total = custo_mao_de_obra + custo_materias_primas

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Custo de Mão de Obra", f"R$ {custo_mao_de_obra:.2f}")
            with col2:
                st.metric("Custo de Matérias-Primas", f"R$ {custo_materias_primas:.2f}")

            st.subheader(f"Custo Total de Produção: R$ {custo_total:.2f}")

            # Aplicar imposto
            if not self.imposto.data.empty:
                estado = st.selectbox('Selecione o Estado', self.imposto.data['Estado'])
                percentual_imposto = self.imposto.data[self.imposto.data['Estado'] == estado]['Percentual'].values[0]
                # Adicionar porcentagem de lucro
                percentual_lucro = st.number_input('Porcentagem de Lucro Desejado (%)', min_value=0.0, step=0.01)
                preco_com_lucro = custo_total * (1 + percentual_lucro / 100)
                preco_final = preco_com_lucro * (1 + percentual_imposto / 100)
                st.subheader(f"Preço Final com Imposto ({percentual_imposto}%): R$ {preco_final:.2f}")
                st.markdown(f"**Detalhamento:**\n- Preço com Lucro ({percentual_lucro}%): R$ {preco_com_lucro:.2f}\n- Imposto Aplicado: R$ {preco_final - preco_com_lucro:.2f}")
            else:
                st.info('Nenhum Imposto cadastrado. Adicione um imposto para calcular o preço final.')
        else:
            st.info('Nenhum Produto cadastrado.')

if __name__ == '__main__':
    app = Aplicativo()
    app.run()