用于刷新pbix文件（powerbi中文版）
需要传入pbix的文件路径

示例：
from pbix_plus import pbix_refresher as r

path = r'c:\111.pbix'
r.refresher(path)