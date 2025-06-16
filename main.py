from bs4 import BeautifulSoup
import sys
import os
import email
from email import policy

def extraer_tweets_de_html(archivo_html):
    """Extrae tweets de un archivo HTML estático o MHTML"""
    
    # Verificar que el archivo existe
    if not os.path.exists(archivo_html):
        print(f"Error: El archivo {archivo_html} no existe")
        return
    
    # Leer el archivo
    try:
        with open(archivo_html, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return
    
    # Verificar si es MHTML y extraer HTML
    html_content = content
    if content.startswith('MIME-Version:') or 'Content-Type: multipart/related' in content:
        print("Detectado archivo MHTML, extrayendo HTML...")
        try:
            msg = email.message_from_string(content, policy=policy.default)
            for part in msg.walk():
                if part.get_content_type() == 'text/html':
                    html_content = part.get_content()
                    break
        except Exception as e:
            print(f"Error al procesar MHTML: {e}")
            return
    
    # Parsear el HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Encontrar todos los tweets (articles)
    articles = soup.find_all('article')
    
    print(f"Se encontraron {len(articles)} tweets en el archivo")
    
    # Agregar debugging para ver si hay errores
    tweets_procesados = 0
    
    for i, article in enumerate(articles):
        try:
            print(f"\n--- Tweet #{i+1} ---")
            
            # Extraer el texto completo del tweet
            try:
                tweet_text = article.find('div', {'data-testid': 'tweetText'})
                if tweet_text:
                    print("Texto:", tweet_text.get_text())
                else:
                    print("Texto: (no encontrado)")
            except Exception as e:
                print(f"Texto: (error al extraer: {e})")
            
            # Verificar si hay una encuesta
            try:
                # Buscar divs que contengan porcentajes
                opciones_encuesta = article.find_all('div', string=lambda text: text and '%' in text)
                if opciones_encuesta:
                    print("Encuesta detectada:")
                    # Usar un set para evitar duplicados
                    opciones_unicas = set()
                    for opcion in opciones_encuesta:
                        texto = opcion.get_text().strip()
                        if texto not in opciones_unicas:
                            opciones_unicas.add(texto)
                            print("  →", texto)
                    
                    # Buscar cantidad de votos usando el patrón del XPath
                    # El XPath apunta a: div[3]/div/div/div/div/div/span[1]/span
                    votos_element = None
                    
                    # Buscar el contenedor de la encuesta y navegar hasta los votos
                    poll_containers = article.find_all('div', recursive=True)
                    for container in poll_containers:
                        spans = container.find_all('span')
                        for span in spans:
                            texto_span = span.get_text().strip()
                            if 'votos' in texto_span.lower() or 'votes' in texto_span.lower():
                                votos_element = span
                                break
                        if votos_element:
                            break
                    
                    if votos_element:
                        votos_texto = votos_element.get_text().strip()
                        print(f"  Total: {votos_texto}")
                    else:
                        print("  Total: (no encontrado)")
                else:
                    print("Encuesta: No detectada")
            except Exception as e:
                print(f"Encuesta: Error al buscar: {e}")
            
            tweets_procesados += 1
            
        except Exception as e:
            print(f"Error procesando tweet #{i+1}: {e}")
            continue
    
    print(f"\nResumen: Se procesaron {tweets_procesados} de {len(articles)} tweets encontrados")

# Uso del script
if __name__ == "__main__":
    if len(sys.argv) == 1:
        # Usar archivo por defecto
        archivo_html = "pages/prueba1.mhtml"
        print(f"Usando archivo por defecto: {archivo_html}")
    elif len(sys.argv) == 2:
        archivo_html = sys.argv[1]
    else:
        print("Uso: python main.py [archivo_html]")
        print("Si no se especifica archivo, se usará pages/prueba.mhtml por defecto")
        print("Ejemplo: python main.py tweet_page.html")
        sys.exit(1)
    
    extraer_tweets_de_html(archivo_html)