"""
Parse Reddit RSS feed and extract post information
"""
import xmltodict
import json
import os
from kestra import Kestra


def main():
    # Obtém o conteúdo XML do feed via variável de ambiente
    xml_content = os.getenv('FEED_XML_CONTENT')
    
    if not xml_content:
        raise Exception("FEED_XML_CONTENT environment variable not set")
    
    # Converte XML para dicionário Python
    feed_dict = xmltodict.parse(xml_content)
    
    # Extrai os posts
    posts = feed_dict['feed']['entry']
    
    # Processa cada post
    processed_posts = []
    for post in posts:
        processed_post = {
            'titulo': post['title'],
            'autor': post['author']['name'],
            'link': post['link']['@href'],
            'data_publicacao': post['published'],
            'conteudo_html': post['content']['#text']
        }
        processed_posts.append(processed_post)
    
    # Mapeia campos para o formato esperado pelo agente
    mapped_data = []
    for post in processed_posts:
        mapped_data.append({
            'title': post['titulo'],
            'contentSnippet': post['conteudo_html'].strip()
        })
    
    # Salva o primeiro post (ou você pode iterar sobre todos)
    if mapped_data:
        selected_post = mapped_data[0]
        Kestra.outputs({
            'post_title': selected_post['title'],
            'post_content': selected_post['contentSnippet'],
            'all_posts': json.dumps(mapped_data)
        })


if __name__ == '__main__':
    main()
