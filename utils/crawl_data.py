import requests
import re
import pandas as pd

from pathlib import Path
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

MAX_NUM_NEWS = 10


def create_driver() -> WebDriver:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extension")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def get_html(driver: WebDriver, url: str) -> None | str:
    response = requests.get(url)

    if response.status_code != 200:
        return None

    driver.get(url)
    html_content = driver.page_source

    return html_content


def get_base_url(url: str) -> str:
    base_url_pattern = re.compile(r"^(http[s]?://[^/]+)", re.IGNORECASE)
    base_url = base_url_pattern.match(url).group(0)
    return base_url


def get_urls(driver: WebDriver, url: str) -> list[str]:
    base_url = get_base_url(url)

    html = get_html(driver, url)
    if html is None:
        return []

    soup = BeautifulSoup(html, "html.parser")
    html_a = soup.find_all("a")

    postfix_urls = []
    for a in html_a:
        href_value = a["href"].strip() if a.has_attr("href") else None
        if (
            href_value is not None
            and href_value.startswith("/en/")
            and href_value not in postfix_urls
            and "tag" not in href_value
        ):
            postfix_urls.append(href_value)

    urls = [base_url + url for url in postfix_urls]

    return urls


def clean_author(author: str) -> str:
    author = re.sub(r"[^\w\s+\(\)\-]", "", author)
    author = re.sub(r"\s+", " ", author).strip()
    return author


def get_news_detail(
    driver: WebDriver,
    url: str,
    max_num_news: int = MAX_NUM_NEWS,
) -> list[dict[str, str]]:
    visited_urls = []
    url_list = [url]
    news_list = []
    count = 0

    base_url = get_base_url(url)

    while len(url_list) > 0 and count < max_num_news:
        current_url = url_list.pop(0)
        visited_urls.append(current_url)
        count += 1

        print(f"Processing {current_url}...")

        html = get_html(driver, current_url)
        if html is None:
            continue

        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.string.strip()

        date = ""
        date_tag = soup.find("div", class_="bread-crumb-detail__time")
        if date_tag is not None:
            date = date_tag.get_text().strip()

        images = paragraphs = soup.find("div", id="maincontent").find_all(
            "table", class_="image"
        )
        image_captions = []
        for image in images:
            caption = image.find("p")
            if caption is not None:
                image_captions.append(caption.get_text().strip())

        inner_articles = soup.find("div", id="maincontent").find(
            "div", class_="inner-article"
        )
        inner_article_texts = []
        if inner_articles is not None:
            inner_article_p = inner_articles.find_all("p")
            for p in inner_article_p:
                inner_article_texts.append(p.get_text().strip())

        p_tags = soup.find("div", id="maincontent").find_all("p")

        paragraphs = []
        for _, p in enumerate(p_tags):
            text = p.get_text().strip()
            if (
                text != ""
                and text not in image_captions
                and text not in inner_article_texts
            ):
                paragraphs.append(p)

        content = ""
        author = ""
        for _, p in enumerate(paragraphs):
            text = p.get_text().strip()
            if re.match(r"^[\.\'\")}\]]$", text[-1]):
                content += text + "\n"
            else:
                last_pos_dot = text.rfind(".")
                if last_pos_dot != -1:
                    content += text[: last_pos_dot + 1].strip() + "\n"
                    author = text[last_pos_dot + 1 :].strip()
                else:
                    author = text
        content = content.strip()

        author = clean_author(author)
        if author == "":
            span_tag = soup.find("div", id="maincontent").find("span")
            if span_tag is not None:
                author = span_tag.get_text().strip()
        if author == "":
            em_tags = soup.find("div", id="maincontent").find_all("em")
            em_texts = []
            for em_tag in em_tags:
                text = em_tag.get_text().strip()
                if text != "":
                    em_texts.append(text)
            if len(em_texts) > 0:
                author = em_texts[-1]
        if author == "":
            article_tags = soup.find("div", id="maincontent").find_all("article")
            article_texts = []
            for article_tag in article_tags:
                text = article_tag.get_text().strip()
                if text != "":
                    article_texts.append(text)
            if len(article_texts) > 0:
                author = article_texts[-1]
        author = clean_author(author)

        summary = soup.find("h2", class_="content-detail-sapo").get_text().strip()

        tags = []
        tag_content = soup.find("div", class_="tag-cotnent")
        html_tags = tag_content.find_all("a") if tag_content is not None else []
        for html_tag in html_tags:
            tag_value = (
                html_tag["title"].strip()
                if html_tag.has_attr("title")
                else html_tag.get_text().strip()
            )
            if tag_value not in tags and tag_value != "":
                tags.append(tag_value)

        html_a = soup.find_all("a")
        news_links = []
        for a in html_a:
            href_value = a["href"].strip() if a.has_attr("href") else None
            if (
                href_value is not None
                and href_value.startswith("/en/")
                and href_value not in news_links
                and href_value != current_url
                and "tag" not in href_value
            ):
                news_links.append(a["href"])
        for link in news_links:
            if link not in visited_urls and link not in url_list:
                url_list.append(base_url + link)

        news = {
            "url": current_url,
            "title": title,
            "date": date,
            "content": content,
            "summary": summary,
            "author": author,
            "tags": tags,
        }
        news_list.append(news)

    return news_list


def crawl_data(
    url: str,
    max_num_news: int = MAX_NUM_NEWS,
) -> list[dict[str, str]]:
    driver = create_driver()

    data = []
    if (not url.endswith(".html")) or (url.endswith(".html") and "tag" in url):
        urls = get_urls(driver, url)
        for url in urls:
            data += get_news_detail(driver, url, max_num_news)
    else:
        data = get_news_detail(driver, url, max_num_news)

    driver.quit()
    print("Done!")

    return data


def save_data(data: list[dict[str, str]], filename: str, config: dict) -> None:
    Path(config["dataset_dir"]).mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(data)
    df.to_csv(Path(config["dataset_dir"], filename), index=False)
