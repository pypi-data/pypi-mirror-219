import requests


def http(url, method="GET", json=False, timeout=3, encoding=None, **kwargs):
    """Args
    url - 地址
    method - http method
    json - return json type"""
    params = {}
    params["timeout"] = timeout
    params["headers"] = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " "Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE "}
    kwargs.update(params)
    resp = requests.request(method, url, **kwargs)
    resp.encoding = encoding if encoding else resp.apparent_encoding
    return resp.json() if json else resp


def download(url, output="./"):
    """Args
    url - URL to download
    output - Output file"""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    filename = url.split("/")[-1]
    with open(f"{output}/{filename}", "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    return output


def xpath(url, path="//text()", encoding="utf-8", **kwargs):
    """
    Args:
        url - string URL to
        path - xpath ql
        encoding - default utf-8
    """
    from lxml.etree import HTML

    if not isinstance(path, list):
        path = [path]
    result = []
    resp = http(url, encoding=encoding)
    html = HTML(resp.text)
    for pth in path:
        xpath_parsed = html.xpath(pth, **kwargs)
        result.append(xpath_parsed)
    return result


if __name__ == "__main__":
    url = "https://top.baidu.com/board?tab=realtime"
    res = xpath(url, "//div[@class='c-single-text-ellipsis']/text()")
    print(res, len(res))
