# Site NACODES - Núcleo de Ação Comunitária e Desenvolvimento Social

Sistema web desenvolvido para fortalecer a presença digital da ONG NACODES e facilitar o engajamento de voluntários e doadores.

## 📋 Documentação
- [Documentação Completa (PDF)](docs/documentacao_projeto.pdf)
- [Diagramas do Sistema](docs/diagramas/)
- [Prints das Telas](docs/prints_telas/)
- [Scripts do Banco](docs/database/nacodes_db.sql)

## 🎯 Sobre a NACODES
ONG fundada em 1998 que atua em comunidades do Rio de Janeiro promovendo inclusão e desenvolvimento social através de projetos educativos, culturais e de qualificação profissional.

**Missão**: Melhorar a qualidade de vida das famílias de baixa renda através da educação e desenvolvimento comunitário.

**Comunidades atendidas**:
- Dendê e Bancários (Ilha do Governador)
- Jacarezinho (Jacaré)  
- Tuiuti (Benfica)
- Parque União (Maré)

## 🛠 Tecnologias Utilizadas
- **Backend**: Python + Flask
- **Banco de Dados**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **Hospedagem**: Hostinger

## 🚀 Funcionalidades Principais

### Para Usuários:
- ✅ Cadastro e login de usuários
- ✅ Visualização de eventos e projetos
- ✅ Sistema de doações
- ✅ Formulário de contato
- ✅ Galeria de fotos

### Para Administradores:
- ✅ Gerenciamento de projetos
- ✅ Controle de usuários
- ✅ Gerenciamento de doações
- ✅ Publicação de eventos

## 📊 Arquitetura do Sistema

**Camada de Apresentação**: HTML, CSS, JavaScript  
**Camada de Lógica**: Python Flask  
**Camada de Dados**: MySQL  

## 🔧 Como Executar Localmente

### Pré-requisitos
- Python 3.x
- MySQL
- XAMPP (opcional)

### Instalação
1. Clone o repositório
```bash
git clone [url-do-repositorio]
cd nacodes-website
```

2. Instale as dependências
```bash
pip install -r requirements.txt
```

3. Configure o banco de dados
- Importe o arquivo `docs/database/nacodes_db.sql`
- Ajuste as credenciais no arquivo de configuração

4. Execute o projeto
```bash
python app.py
```

5. Acesse `http://localhost:5000`

## 📁 Estrutura do Projeto
```
nacodes-website/
├── app.py                    # Arquivo principal Flask
├── templates/                # Templates HTML
├── static/                   # CSS, JS, imagens
├── docs/                     # Documentação
│   ├── documentacao_projeto.pdf
│   ├── diagramas/
│   ├── prints_telas/
│   └── database/
├── requirements.txt          # Dependências Python
└── README.md                # Este arquivo
```

## 🌐 Deploy
O sistema está configurado para deploy na **Hostinger** com suporte completo a Python/Flask e MySQL.

## 👥 Equipe de Desenvolvimento

| Nome | Matrícula | Função |
|------|-----------|--------|
| **Luis Fernando Dantas Carvalho** | 0050020769 | **Coordenador do Grupo** |
| Caio Leal Bellas | 0050019961 | Desenvolvedor |
| Carlos Eduardo Júlio da Costa | 0050021975 | Desenvolvedor |
| Keven Pinto Fernandes | 0050021029 | Desenvolvedor |
| Luis Felipe Scangarelli de Andrade | 0050021098 | Desenvolvedor |
| Raphael Rocha Conde | 0050020646 | Desenvolvedor |

## 🏫 Informações Acadêmicas
**Instituição**: Centro Universitário La Salle do Rio de Janeiro  
**Curso**: Sistemas de Informação  
**Período**: Junho/2025  
**Disciplina**: Projeto Extensionista  

## 📞 Contato da ONG
**CNPJ**: 02.717.198/0001-54  
**Localização**: Jacaré, Rio de Janeiro, Brasil  
**Fundação**: 1998  

## 🤝 Contribuição
Este projeto foi desenvolvido como trabalho acadêmico em parceria com a ONG NACODES, visando fortalecer sua presença digital e ampliar seu impacto social.

## 📄 Licença
Este projeto foi desenvolvido para fins educacionais e em benefício da ONG NACODES.

---
*Desenvolvido com ❤️ para transformar vidas através da tecnologia*
