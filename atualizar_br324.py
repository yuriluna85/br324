import os
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta

def fetch_rss_feed():
    url = "https://g1.globo.com/rss/g1/bahia/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
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
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def main():
    # Caminho do JSON dinâmico em relação ao local do script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "dados-transito.json")
    
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

    xml_data = fetch_rss_feed()
    rss_news = parse_news(xml_data)

    noticias_hoje = [n for n in rss_news if n["hoje"]]
    
    if not noticias_hoje:
        existentes = data.get("noticias", [])
        noticias_hoje = [n for n in existentes if n.get("data", "").startswith(agora.date().isoformat())]
        
    if not noticias_hoje:
        noticias_hoje = [
            {
                "titulo": "Sem ocorrências graves registradas nas últimas horas",
                "link": "",
                "fonte": "Mídias Locais",
                "data": agora.isoformat(),
                "resumo": "O tráfego na BR-324 opera sob condições normais nos principais trechos. Não há registros de acidentes severos ou interdições de faixas na rodovia."
            }
        ]

    status_geral = "Fluido"
    alertas = data.get("alertas", [
        {"ponto": "Pedágio de Simões Filho (Km 599)", "status": "Fluido", "mensagem": "Fluxo normal."},
        {"ponto": "Trecho de Amélia Rodrigues (Km 545)", "status": "Fluido", "mensagem": "Fluxo normal."},
        {"ponto": "Acesso a Feira de Santana (Km 518)", "status": "Fluido", "mensagem": "Fluxo normal."}
    ])

    noticias_texto = " ".join([n["titulo"] for n in noticias_hoje]).lower()
    if "acidente" in noticias_texto or "congestionamento" in noticias_texto or "bloque" in noticias_texto or "interd" in noticias_texto:
        status_geral = "Lento"
        alertas[0]["status"] = "Atenção"
        alertas[0]["mensagem"] = "Alerta de lentidão devido a ocorrência relatada nas notícias locais."
    elif "obras" in noticias_texto or "lentidão" in noticias_texto:
        status_geral = "Atenção"
        alertas[2]["status"] = "Atenção"
        alertas[2]["mensagem"] = "Atenção reduzida nas imediações devido a obras pontuais relatadas."

    tempo_normal = 75
    tempo_estimado = 95 if status_geral == "Lento" else (85 if status_geral == "Atenção" else 75)

    dados_atualizados = {
        "statusGeral": status_geral,
        "ultimaAtualizacao": agora.isoformat(),
        "tempoEstimadoMinutos": tempo_estimado,
        "tempoNormalMinutos": tempo_normal,
        "alertas": alertas,
        "noticias": noticias_hoje
    }

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados_atualizados, f, indent=2, ensure_ascii=False)

    print(f"Sucesso: dados-transito.json atualizado em {agora.strftime('%H:%M:%S')}!")

if __name__ == "__main__":
    main()
