from utils.crawl_data import crawl_data, save_data
from config.config import get_config


config = get_config()
url = "https://vietnamnet.vn/en"
data = crawl_data(url=url, max_num_news=10)
save_data(data, "vietnamnet.csv", config)
