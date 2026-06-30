# 🛣️ BR-324 em Tempo Real | Monitor de Tráfego e Notícias
> **Projeto desenvolvido sob a chancela 🔬 YLuna85 LABs & AlmeidaLuna TECHs**

Monitor de tráfego, ocorrências e notícias em tempo real sobre a rodovia federal **BR-324** no trecho que liga **Salvador a Feira de Santana**. A aplicação apresenta alertas dinâmicos de pista, mapa ao vivo com a camada de tráfego integrada e consolidação diária dos principais incidentes.

---

## 📌 Sobre a Aplicação
O portal foi projetado para motoristas e passageiros que trafegam diariamente na BR-324. A aplicação compila notícias das últimas horas e exibe o tempo estimado de viagem de forma dinâmica.

## ✨ Funcionalidades Principais
- 🗺️ **Mapa em Tempo Real**: Integração do Live Map do Waze indicando fluxo, retenções e alertas.
- ⚡ **Alertas de Pista**: Boletins sobre pontos específicos (pedágios de Simões Filho e Amélia Rodrigues).
- 📰 **Notícias Automatizadas**: Filtro dinâmico de notícias locais relacionadas à rodovia (via RSS).
- ♿ **Acessibilidade Universal (A11y/WCAG)**: Controles de redimensionamento de fonte (A+/A-) e modo Alto Contraste (🌓).
- 📱 **Monetização e Responsividade**: Design Mobile-First com espaços de anúncios estruturados e responsivos para Google AdSense e AdMob.

## 🛠️ Tecnologias Utilizadas
- **Frontend**: HTML5 Semântico, Vanilla CSS (Glassmorphism e Variáveis Dinâmicas), JavaScript (ES6+).
- **Backend (Scripts)**: Python 3 para processamento de feeds RSS e automação do banco de dados local.

---

## 📜 Log de Atualizações (Changelog)

### 📅 30/06/2026 - Lançamento da Aplicação e Integração de SEO
- 🚀 **Lançamento do Portal**: Inicialização da interface em tema Dark/Glassmorphism com o Waze Live Map e **seletor de rotas dinâmicas** (Feira ➔ Salvador / Salvador ➔ Feira) com ordenação espacial dos alertas e links rápidos de GPS.
- 🌐 **Otimização de SEO (White Hat)**: Inclusão de meta tags estruturadas, tags Open Graph (OG) e dados estruturados JSON-LD.
- 💵 **Monetização Ativa**: Slots de anúncios estruturados e acessíveis destinados ao Google AdSense e AdMob.
- 🤖 **Script de Automação**: Criação de script Python em `atualizar_br324.py` na raiz do projeto para processar notícias de trânsito em lote.
- 🔧 **Responsividade do Mapa**: Correção do bug de renderização do iframe do Waze no mobile através de altura fixa de 420px em telas menores, evitando a sobreposição do botão de expansão.
