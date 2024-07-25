import streamlit as st
from docx import Document
import pdfkit
import os

# Função para preencher o contrato


def preencher_contrato(nome, rg, cpf, endereco, bairro, cidade, uf, dataevento, tipo_contrato):
    # Carrega o modelo de contrato
    doc = Document(f'modelos/{tipo_contrato}.docx')

    for paragrafo in doc.paragraphs:
        if '<<NOME>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('<<NOME>>', nome)
        if '<<RG>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('<<RG>>', rg)
        if '<<CPF>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('<<CPF>>', cpf)
        if '<<ENDERECO>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('<<ENDERECO>>', endereco)
        if '<<BAIRRO>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('<<BAIRRO>>', bairro)
        if '<<CIDADE>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('<<CIDADE>>', cidade)
        if '<<UF>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace('<<UF>>', uf)
        if '<<DATAEVENTO>>' in paragrafo.text:
            paragrafo.text = paragrafo.text.replace(
                '<<DATAEVENTO>>', dataevento)

    output_path = f'contratos/Contrato_{nome}.docx'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    return output_path

# Função para converter DOCX para PDF usando pdfkit


def converter_para_pdf(input_path):
    output_path = input_path.replace('.docx', '.pdf')

    # Caminho do executável wkhtmltopdf
    # No ambiente Streamlit Cloud ou outros ambientes, pode ser necessário ajustar isso
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')

    try:
        pdfkit.from_file(input_path, output_path, configuration=config)
    except Exception as e:
        raise RuntimeError(f"Erro ao converter para PDF: {e}")

    return output_path


# Configurações da interface do Streamlit
logotipo = "artes/jpcb.png"

col1, col2, col3 = st.columns([2, 3, 2])
with col1:
    st.image(logotipo, width=150)
with col2:
    st.title("Gerador de Contratos")
with col3:
    st.image(logotipo, width=150)

# Seleção do tipo de contrato
tipo = st.selectbox('Selecione o tipo de contrato:',
                    ['Ouro', 'Prata', 'Bronze'])

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
    # Verificar se todos os campos estão preenchidos
    if not (nome and rg and cpf and endereco and bairro and cidade and uf and dataevento):
        st.error("Por favor, preencha todos os campos.")
    else:
        try:
            docx_path = preencher_contrato(
                nome, rg, cpf, endereco, bairro, cidade, uf, dataevento, tipo)
            pdf_path = converter_para_pdf(docx_path)
            st.success(f"Contrato gerado com sucesso: {pdf_path}")

            # Opções de download
            with open(docx_path, "rb") as file:
                st.download_button(
                    label="Baixar Contrato (DOCX)",
                    data=file,
                    file_name=f"Contrato_{nome}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

            with open(pdf_path, "rb") as file:
                st.download_button(
                    label="Baixar Contrato (PDF)",
                    data=file,
                    file_name=f"Contrato_{nome}.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
