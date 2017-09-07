import re
def find_all_link(html):
        link = re.findall("href=\"//(\S+\.taobao\.com/\S+\?search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("\"//(\S+\.taobao\.com/search.htm)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("\"//(\S+search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("//(\S+search.htm\?search=y)\"",html)
        if len(link) >= 1:
            return link[0]
        link = re.findall("//(\S+search=y)\"", html)
        if len(link) >= 1:
            return link[0]
        return False


html = """
       <div class="all-cats popup-container">
<div class="all-cats-trigger popup-trigger">
<a class="link " href="//shop107687609.taobao.com/search.htm?search=y">
<span class="title"> 所有分类 </span>
<i class="popup-icon"></i>
</a>
"""

print (find_all_link(html))
