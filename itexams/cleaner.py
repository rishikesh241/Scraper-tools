from bs4 import BeautifulSoup


def clean_itexams_html(html: str, source_url: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for script in soup.find_all("script"):
        script_text = script.string or script.get_text()
        if "google-analytics" in script_text or "gtag" in script_text:
            script.decompose()

    if soup.head:
        if not soup.head.find("base"):
            base_tag = soup.new_tag("base", href=source_url)
            soup.head.insert(0, base_tag)

    return str(soup)
