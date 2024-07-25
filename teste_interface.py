import streamlit as st
from docx import Document
import pypandoc

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
    doc.save(output_path)
    return output_path

# Função para converter DOCX para PDF


def converter_para_pdf(input_path):
    output_path = input_path.replace('.docx', '.pdf')
    pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)
    return output_path


logotipo = "artes/jpcb.png"

# Interface Streamlit
st.title("Gerador de Contratos")
st.image(caminho_logotipo, width=150)

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
