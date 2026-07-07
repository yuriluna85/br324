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
- **Automação (CI/CD)**: GitHub Actions para atualização programada e contínua do banco de dados do trânsito.

---

## 📜 Log de Atualizações (Changelog)

### 📅 07/07/2026 - Integração de APIs de Notícias, Consentimento e Otimizações
- 📰 **Fontes Avançadas**: Integração das APIs Serper (Google News) e Scraper API (Proxy para RSS) em [atualizar_br324.py](file:///G:/Meu%20Drive/APP/2.%20Projetos%20e%20Aplica%C3%A7%C3%B5es/2.2%20Aplica%C3%A7%C3%B5es%20e%20C%C3%B3digos%20(GitHub)/YLuna85%20LABs%20APPs/br324/atualizar_br324.py) para busca em tempo real de matérias sobre a rodovia entre Salvador e Feira de Santana.
- ⚙️ **Configuração Dinâmica**: Criação de [.env.example](file:///G:/Meu%20Drive/APP/2.%20Projetos%20e%20Aplica%C3%A7%C3%B5es/2.2%20Aplica%C3%A7%C3%B5es%20e%20C%C3%B3digos%20(GitHub)/YLuna85%20LABs%20APPs/br324/.env.example) definindo as variáveis `SERPER_API_KEY` e `SCRAPER_API_KEY`, e atualização do workflow do GitHub Actions em [.github/workflows/atualizar_transito.yml](file:///G:/Meu%20Drive/APP/2.%20Projetos%20e%20Aplica%C3%A7%C3%B5es/2.2%20Aplica%C3%A7%C3%B5es%20e%20C%C3%B3digos%20(GitHub)/YLuna85%20LABs%20APPs/br324/.github/workflows/atualizar_transito.yml) para injetar as credenciais a partir de secrets.
- 🛡️ **Segurança e Privacidade**: Implementação de banner de consentimento de cookies e modal de Política de Privacidade no portal em [index.html](file:///G:/Meu%20Drive/APP/2.%20Projetos%20e%20Aplica%C3%A7%C3%B5es/2.2%20Aplica%C3%A7%C3%B5es%20e%20C%C3%B3digos%20(GitHub)/YLuna85%20LABs%20APPs/br324/index.html) em Vanilla CSS/JS com suporte a acessibilidade (A11y/WCAG) e persistência de dados em `localStorage`.
- ⚡ **Otimização de Carregamento**: Adicionado atributo `loading="lazy"` ao iframe do Waze Live Map para priorizar a renderização de elementos principais do DOM e acelerar o tempo de carregamento da página.

### 📅 30/06/2026 - Lançamento da Aplicação e Integração de SEO
- 🚀 **Lançamento do Portal**: Inicialização da interface em tema Dark/Glassmorphism com o Waze Live Map e **seletor de rotas dinâmicas** (Feira ➔ Salvador / Salvador ➔ Feira) com ordenação espacial dos alertas e links rápidos de GPS.
- 🌐 **Otimização de SEO (White Hat)**: Inclusão de meta tags estruturadas, tags Open Graph (OG) e dados estruturados JSON-LD.
- 💵 **Monetização Ativa**: Slots de anúncios estruturados e acessíveis destinados ao Google AdSense e AdMob.
- 🤖 **Script de Automação**: Criação de script Python em `atualizar_br324.py` na raiz do projeto para processar notícias de trânsito em lote.
- 🔧 **Responsividade do Mapa**: Correção do bug de renderização do iframe do Waze no mobile através de altura fixa de 420px em telas menores, evitando a sobreposição do botão de expansão.
- 🔗 **Correção de Links de Notícias**: Ajuste no frontend e backend para ocultar dinamicamente o link de leitura de matérias quando a URL for vazia, nula ou genérica (boletins autorais e de fallback).
- ⚙️ **Integração de CI/CD**: Configuração de workflow do GitHub Actions em `.github/workflows/atualizar_transito.yml` para rodar o robô de 30 em 30 minutos e atualizar o portal.
- 📊 **Observatório de Métricas**: Armazenamento histórico dos dados de tráfego em arquivos CSV estruturados (`data/ano/mes/dia.csv`) e inserção de aba de Métricas & Estatísticas na interface com distribuição percentual e categorização de causa raiz (obras vs. acidentes).
