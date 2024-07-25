import streamlit as st
from docx import Document
import os

# Função para preencher o contrato
def preencher_contrato(nome, rg, cpf, endereco, bairro, cidade, uf, dataevento, tipo_contrato):
    doc = Document(f'modelos/{tipo_contrato}.docx')

    for paragrafo in doc.paragraphs:
        paragrafo.text = paragrafo.text.replace('<<NOME>>', nome)
        paragrafo.text = paragrafo.text.replace('<<RG>>', rg)
        paragrafo.text = paragrafo.text.replace('<<CPF>>', cpf)
        paragrafo.text = paragrafo.text.replace('<<ENDERECO>>', endereco)
        paragrafo.text = paragrafo.text.replace('<<BAIRRO>>', bairro)
        paragrafo.text = paragrafo.text.replace('<<CIDADE>>', cidade)
        paragrafo.text = paragrafo.text.replace('<<UF>>', uf)
        paragrafo.text = paragrafo.text.replace('<<DATAEVENTO>>', dataevento)

    output_path = f'/tmp/contratos/Contrato_{nome}.docx'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path

# Configurações da interface do Streamlit
logotipo = "artes/jpcb.png"  # Substitua pelo caminho real do seu logotipo

col1, col2, col3 = st.columns([2, 3, 2])
with col1:
    st.image(logotipo, width=150)
with col2:
    st.title("Gerador de Contratos")
with col3:
    st.image(logotipo, width=150)

# Seleção do tipo de contrato
tipo = st.selectbox('Selecione o tipo de contrato:', ['Ouro', 'Prata', 'Bronze'])

# Coleta de informações do cliente
nome = st.text_input("Nome do cliente:")
rg = st.text_input("RG:")
cpf = st.text_input("CPF:")
endereco = st.text_input("Endereço (Rua e Número):")
bairro = st.text_input("Bairro:")
cidade = st.text_input("Cidade:")
uf = st.text_input("Estado (UF):")
dataevento = st.text_input("Data do evento (ex: 01 de janeiro de 2024):")

# Botão para gerar contrato
if st.button("Gerar Contrato"):
    if not all([nome, rg, cpf, endereco, bairro, cidade, uf, dataevento]):
        st.error("Por favor, preencha todos os campos.")
    else:
        try:
            docx_path = preencher_contrato(nome, rg, cpf, endereco, bairro, cidade, uf, dataevento, tipo)
            st.success("Contrato gerado com sucesso!")

            # Opção de download do DOCX
            with open(docx_path, "rb") as file:
                st.download_button(
                    label="Baixar Contrato (DOCX)",
                    data=file,
                    file_name=f"Contrato_{nome}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
