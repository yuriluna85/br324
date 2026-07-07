import os
import json
import csv
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timezone, timedelta

def fetch_rss_feed(scraper_api_key=None):
    target_url = "https://g1.globo.com/rss/g1/bahia/"
    if scraper_api_key:
        url = f"http://api.scraperapi.com?api_key={scraper_api_key}&url={urllib.parse.quote(target_url)}"
    else:
        url = target_url
        
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            return response.read()
    except Exception as e:
        print(f"Erro ao buscar RSS: {e}")
        return None

def parse_news(xml_data):
    if not xml_data:
        return []
        
    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"Erro ao parsear XML: {e}")
        return []

    news_list = []
    keywords = ["br-324", "br 324", "br324", "viabahia", "simões filho", "amélia rodrigues", "feira de santana", "pedágio"]

    # Fuso horário local (UTC-3)
    tz_local = timezone(timedelta(hours=-3))
    hoje = datetime.now(tz_local).date()

    for item in root.findall(".//item"):
        title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        description = item.find("description").text if item.find("description") is not None else ""
        pub_date_str = item.find("pubDate").text if item.find("pubDate") is not None else ""
        
        clean_desc = re_sub_html(description) if description else ""
        content_to_check = f"{title} {clean_desc}".lower()
        has_keyword = any(kw in content_to_check for kw in keywords)

        if has_keyword:
            pub_date = None
            if pub_date_str:
                try:
                    clean_date_str = pub_date_str.rsplit(' ', 1)[0]
                    pub_date = datetime.strptime(clean_date_str, "%a, %d %b %Y %H:%M:%S")
                    pub_date = pub_date.replace(tzinfo=timezone.utc) - timedelta(hours=3)
                except Exception as ex:
                    print(f"Erro no parse de data: {ex}")
                    pub_date = datetime.now(tz_local)

            is_today = True
            if pub_date:
                is_today = (pub_date.date() == hoje)
                pub_date_iso = pub_date.isoformat()
            else:
                pub_date_iso = datetime.now(tz_local).isoformat()

            news_list.append({
                "titulo": title,
                "link": link,
                "fonte": "G1 Bahia",
                "data": pub_date_iso,
                "resumo": clean_desc[:200] + "..." if len(clean_desc) > 200 else clean_desc,
                "hoje": is_today
            })
            
    return news_list

def re_sub_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def fetch_serper_news(api_key):
    if not api_key:
        return []
    url = "https://google.serper.dev/news"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    # Query específica para BR-324 Feira de Santana Salvador
    payload = {
        "q": 'BR-324 "Feira de Santana" OR "Salvador" noticias',
        "gl": "br",
        "hl": "pt-br"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            res_data = response.read()
            data = json.loads(res_data.decode("utf-8"))
            return data.get("news", [])
    except Exception as e:
        print(f"Erro ao buscar Serper News: {e}")
        return []

def parse_relative_date(date_str, tz_local):
    agora = datetime.now(tz_local)
    date_str = date_str.lower().strip()
    
    # Tenta encontrar números
    numbers = re.findall(r'\d+', date_str)
    num = int(numbers[0]) if numbers else 1
    
    if any(x in date_str for x in ["minuto", "minute", "min"]):
        return agora - timedelta(minutes=num)
    elif any(x in date_str for x in ["hora", "hour", "h"]):
        return agora - timedelta(hours=num)
    elif any(x in date_str for x in ["dia", "day", "d"]):
        return agora - timedelta(days=num)
    elif any(x in date_str for x in ["semana", "week", "sem"]):
        return agora - timedelta(weeks=num)
    elif any(x in date_str for x in ["mês", "mes", "month"]):
        return agora - timedelta(days=num * 30)
    else:
        # Tenta formatos comuns
        for fmt in ("%b %d, %Y", "%d de %b de %Y", "%d/%m/%Y", "%Y-%m-%d"):
            try:
                clean_date = date_str.replace(" de ", " ").replace(".", "")
                parsed_dt = datetime.strptime(clean_date, fmt)
                return parsed_dt.replace(tzinfo=tz_local)
            except Exception:
                continue
        return agora

def fetch_google_news_rss():
    query = urllib.parse.quote('BR-324 ("Feira de Santana" OR "Salvador")')
    url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=12) as response:
            return response.read()
    except Exception as e:
        print(f"Erro ao buscar Google News RSS: {e}")
        return None

def parse_google_news_rss(xml_data):
    if not xml_data:
        return []
        
    try:
        root = ET.fromstring(xml_data)
    except Exception as e:
        print(f"Erro ao parsear XML do Google News: {e}")
        return []

    news_list = []
    keywords = ["br-324", "br 324", "br324", "viabahia", "simões filho", "amélia rodrigues", "feira de santana", "pedágio", "rodovia vasco filho"]

    # Fuso horário local (UTC-3)
    tz_local = timezone(timedelta(hours=-3))
    hoje = datetime.now(tz_local).date()

    for item in root.findall(".//item"):
        raw_title = item.find("title").text if item.find("title") is not None else ""
        link = item.find("link").text if item.find("link") is not None else ""
        pub_date_str = item.find("pubDate").text if item.find("pubDate") is not None else ""
        
        title = raw_title
        fonte = "Google Notícias"
        if " - " in raw_title:
            parts = raw_title.rsplit(" - ", 1)
            title = parts[0]
            fonte = parts[1]
            
        source_elem = item.find("source")
        if source_elem is not None and source_elem.text:
            fonte = source_elem.text

        content_to_check = title.lower()
        has_keyword = any(kw in content_to_check for kw in keywords)

        if has_keyword:
            pub_date = None
            if pub_date_str:
                try:
                    clean_date_str = pub_date_str.rsplit(' ', 1)[0]
                    pub_date = datetime.strptime(clean_date_str, "%a, %d %b %Y %H:%M:%S")
                    pub_date = pub_date.replace(tzinfo=timezone.utc) - timedelta(hours=3)
                except Exception as ex:
                    print(f"Erro no parse de data do Google News: {ex}")
                    pub_date = datetime.now(tz_local)

            is_today = True
            if pub_date:
                is_today = (pub_date.date() == hoje)
                pub_date_iso = pub_date.isoformat()
            else:
                pub_date_iso = datetime.now(tz_local).isoformat()

            news_list.append({
                "titulo": title,
                "link": link,
                "fonte": fonte,
                "data": pub_date_iso,
                "resumo": "Notícia consolidada via Google Notícias.",
                "hoje": is_today
            })
            
    return news_list

def main():
    # Caminhos dinâmicos em relação ao script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "dados-transito.json")
    data_dir = os.path.join(script_dir, "data")
    
    # Fuso horário local (UTC-3)
    tz_local = timezone(timedelta(hours=-3))
    agora = datetime.now(tz_local)
    
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    else:
        data = {}

    scraper_api_key = os.environ.get("SCRAPER_API_KEY")
    serper_api_key = os.environ.get("SERPER_API_KEY")

    xml_data = fetch_rss_feed(scraper_api_key)
    rss_news = parse_news(xml_data)

    serper_articles = []
    if serper_api_key:
        print("Buscando notícias via Serper API...")
        raw_serper = fetch_serper_news(serper_api_key)
        for art in raw_serper:
            title = art.get("title", "")
            link = art.get("link", "")
            snippet = art.get("snippet", "")
            date_str = art.get("date", "")
            source = art.get("source", "Google Notícias")
            
            pub_date = parse_relative_date(date_str, tz_local)
            
            # Verificar palavras-chave no título ou snippet para garantir relevância
            keywords = ["br-324", "br 324", "br324", "viabahia", "simões filho", "amélia rodrigues", "feira de santana", "pedágio", "rodovia vasco filho"]
            content_to_check = f"{title} {snippet}".lower()
            has_keyword = any(kw in content_to_check for kw in keywords)
            
            if has_keyword:
                is_today = (pub_date.date() == agora.date())
                serper_articles.append({
                    "titulo": title,
                    "link": link,
                    "fonte": source,
                    "data": pub_date.isoformat(),
                    "resumo": snippet[:200] + "..." if len(snippet) > 200 else snippet,
                    "hoje": is_today
                })
    else:
        print("Buscando notícias via API gratuita de RSS do Google News...")
        xml_gnews = fetch_google_news_rss()
        serper_articles = parse_google_news_rss(xml_gnews)

    # Combinar RSS e Serper
    todos_artigos = rss_news + serper_articles

    # Remover duplicatas por link e título normalizado
    artigos_dedup = []
    links_vistos = set()
    titulos_vistos = set()

    for art in todos_artigos:
        link = art.get("link", "").strip()
        titulo_norm = "".join(filter(str.isalnum, art.get("titulo", "").lower()))
        
        if link and link in links_vistos:
            continue
        if titulo_norm in titulos_vistos:
            continue
            
        if link:
            links_vistos.add(link)
        titulos_vistos.add(titulo_norm)
        artigos_dedup.append(art)

    # Ordenar por data decrescente
    artigos_dedup.sort(key=lambda x: x.get("data", ""), reverse=True)

    noticias_hoje = [n for n in artigos_dedup if n["hoje"]]
    
    if not noticias_hoje:
        existentes = data.get("noticias", [])
        noticias_hoje = [n for n in existentes if n.get("data", "").startswith(agora.date().isoformat())]
        
    if not noticias_hoje:
        # Padrão de segurança: Tolerância Zero a alucinações (Usando termo "Notícia de Teste" conforme regra)
        noticias_hoje = [
            {
                "titulo": "Notícia de Teste: Sem ocorrências graves registradas nas últimas horas",
                "link": "",
                "fonte": "Mídias Locais",
                "data": agora.isoformat(),
                "resumo": "O tráfego na BR-324 opera sob condições normais nos principais trechos. Não há registros de acidentes severos ou interdições de faixas na rodovia."
            }
        ]

    status_geral = "Fluido"
    alertas = [
        {"ponto": "Pedágio de Simões Filho (Km 599)", "status": "Fluido", "mensagem": "Fluxo normal."},
        {"ponto": "Trecho de Amélia Rodrigues (Km 545)", "status": "Fluido", "mensagem": "Fluxo normal."},
        {"ponto": "Acesso a Feira de Santana (Km 518)", "status": "Fluido", "mensagem": "Fluxo normal."}
    ]

    noticias_texto = " ".join([n["titulo"] for n in noticias_hoje]).lower()
    
    # Determinar a causa da lentidão baseada nas notícias
    causa_lentidao = "Nenhuma"
    if "acidente" in noticias_texto or "colisão" in noticias_texto or "batida" in noticias_texto:
        status_geral = "Lento"
        causa_lentidao = "Acidente"
        alertas[0]["status"] = "Lento"
        alertas[0]["mensagem"] = "Lentidão acentuada devido a registro de acidente nas imediações."
    elif "obras" in noticias_texto or "recapeamento" in noticias_texto or "interdição" in noticias_texto:
        status_geral = "Atenção"
        causa_lentidao = "Obra"
        alertas[1]["status"] = "Atenção"
        alertas[1]["mensagem"] = "Fluxo com atenção redobrada devido a obras de manutenção na pista."
    elif "lentidão" in noticias_texto or "congestionamento" in noticias_texto:
        status_geral = "Atenção"
        causa_lentidao = "Congestionamento"
        alertas[2]["status"] = "Atenção"
        alertas[2]["mensagem"] = "Aumento no fluxo habitual de veículos com retenção localizada."

    tempo_normal = 75
    tempo_estimado = 95 if status_geral == "Lento" else (85 if status_geral == "Atenção" else 75)
    qtd_alertas_ativos = sum(1 for a in alertas if a["status"] != "Fluido")

    # 1. CRIAR E SALVAR REGISTRO EM CSV (ORGANIZAÇÃO POR DATA: data/ano/mes/dia.csv)
    ano_str = agora.strftime("%Y")
    mes_str = agora.strftime("%m")
    dia_str = agora.strftime("%Y-%m-%d")
    
    pasta_mes = os.path.join(data_dir, ano_str, mes_str)
    os.makedirs(pasta_mes, exist_ok=True)
    
    csv_path = os.path.join(pasta_mes, f"{dia_str}.csv")
    csv_exists = os.path.exists(csv_path)
    
    with open(csv_path, "a", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not csv_exists:
            writer.writerow(["horario", "status_geral", "tempo_estimado", "tempo_normal", "qtd_noticias", "causa_lentidao", "alertas_ativos"])
        writer.writerow([
            agora.strftime("%H:%M:%S"),
            status_geral,
            tempo_estimado,
            tempo_normal,
            len(noticias_hoje),
            causa_lentidao,
            qtd_alertas_ativos
        ])

    # 2. CALCULAR MÉTRICAS HISTÓRICAS (Lendo todos os arquivos CSV acumulados)
    total_registros = 0
    contagem_status = {"Fluido": 0, "Atenção": 0, "Lento": 0}
    total_acidentes = 0
    total_obras = 0
    total_congestionamento = 0
    soma_tempo = 0

    if os.path.exists(data_dir):
        for root, dirs, files in os.walk(data_dir):
            for file in files:
                if file.endswith(".csv"):
                    f_path = os.path.join(root, file)
                    try:
                        with open(f_path, "r", encoding="utf-8") as f:
                            reader = csv.reader(f)
                            header = next(reader, None)
                            if not header:
                                continue
                            
                            # Obter índices correspondentes
                            idx_status = header.index("status_geral") if "status_geral" in header else -1
                            idx_tempo = header.index("tempo_estimado") if "tempo_estimado" in header else -1
                            idx_causa = header.index("causa_lentidao") if "causa_lentidao" in header else -1
                            
                            for row in reader:
                                if len(row) > max(idx_status, idx_tempo, idx_causa):
                                    st = row[idx_status]
                                    if st in contagem_status:
                                        contagem_status[st] += 1
                                    
                                    try:
                                        soma_tempo += float(row[idx_tempo])
                                    except ValueError:
                                        soma_tempo += 75
                                        
                                    causa = row[idx_causa]
                                    if causa == "Acidente":
                                        total_acidentes += 1
                                    elif causa == "Obra":
                                        total_obras += 1
                                    elif causa == "Congestionamento":
                                        total_congestionamento += 1
                                        
                                    total_registros += 1
                    except Exception as e:
                        print(f"Erro ao ler CSV {f_path}: {e}")

    # Fallback se não houver registros históricos
    if total_registros == 0:
        contagem_status[status_geral] = 1
        soma_tempo = tempo_estimado
        if causa_lentidao == "Acidente":
            total_acidentes = 1
        elif causa_lentidao == "Obra":
            total_obras = 1
        elif causa_lentidao == "Congestionamento":
            total_congestionamento = 1
        total_registros = 1

    percent_fluido = round((contagem_status["Fluido"] / total_registros) * 100, 1)
    percent_atencao = round((contagem_status["Atenção"] / total_registros) * 100, 1)
    percent_lento = round((contagem_status["Lento"] / total_registros) * 100, 1)
    tempo_medio = round(soma_tempo / total_registros, 1)

    # Determinar causa principal de lentidão
    causas_ranking = {
        "Acidente": total_acidentes,
        "Obra": total_obras,
        "Congestionamento": total_congestionamento
    }
    causa_principal = max(causas_ranking, key=causas_ranking.get)
    if causas_ranking[causa_principal] == 0:
        causa_principal = "Nenhuma"

    # Injetar os dados atualizados com o bloco de métricas
    dados_atualizados = {
        "statusGeral": status_geral,
        "ultimaAtualizacao": agora.isoformat(),
        "tempoEstimadoMinutos": tempo_estimado,
        "tempoNormalMinutos": tempo_normal,
        "alertas": alertas,
        "noticias": noticias_hoje,
        "metricas": {
            "totalRegistros": total_registros,
            "percentualFluido": percent_fluido,
            "percentualAtencao": percent_atencao,
            "percentualLento": percent_lento,
            "totalAcidentes": total_acidentes,
            "totalObras": total_obras,
            "totalCongestionamento": total_congestionamento,
            "causaPrincipalLentidao": causa_principal,
            "tempoMedioMinutos": tempo_medio
        }
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados_atualizados, f, indent=2, ensure_ascii=False)

    print(f"Sucesso: dados-transito.json atualizado em {agora.strftime('%H:%M:%S')} com {total_registros} registros históricos no CSV!")

if __name__ == "__main__":
    main()
