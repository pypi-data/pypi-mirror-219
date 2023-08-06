def clean_domain(url) -> str:
    # assert "." in url, "URL must contain a dot"
    url = url.lower().strip()
    url = url.replace("http://", "").replace("https://", "").replace("www.", "")
    return url.split("/")[0]
