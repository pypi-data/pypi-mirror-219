import aiofiles
import os
from urllib.parse import urljoin
import urllib.request
import lxml.etree
from fish_tool.net.proxy_16yun import async_get
from fish_tool.log_tool import logs, InfoError

html_char__file_char = {  # 支持windows文件系统 也支持压缩成zip文件
    '/': '·┇',
    '\t': '·t',
    '\\': '·┊',
    '?': '·？',
    ' ': '·▅',
    ':': '·▋',
    '*': '·▆',
    '"': "·'",
    '|': '·▎',
    '<': '·〈',
    '>': '·〉',
}
start__file_char = [
    ('https://', '·S'),
    ('http://', '·H'),
]


def root(*paths):
    path = os.path.join(os.path.dirname(__file__), '../../', *paths)
    return os.path.abspath(path)


def html_to_file_name(html_name):
    file_name = urllib.request.unquote(html_name)  # url编码转成中文
    for start, char in start__file_char:
        if file_name.startswith(start):
            file_name = file_name.replace(start, char)

    for html_char, file_char in html_char__file_char.items():
        file_name = file_name.replace(html_char, file_char)
    return file_name


def file_to_html_name(file_name):
    pre = ''
    for start_html, start_char in start__file_char:
        if file_name.startswith(start_char):
            pre = start_html
            file_name = file_name.replace(start_char, '')
    for html_char, file_char in html_char__file_char.items():
        file_name = file_name.replace(file_char, html_char)
    html_name = pre + urllib.request.quote(file_name)  # 中文转成url编码
    return html_name


def _test_file_name():
    assert len(set(html_char__file_char.values())) == len(html_char__file_char)
    for url in [
        'https://www.bilibili.com/video/BV1cA{41}1s7Kz',
        'https://www.ciweimao.com/book_list/weilai<huan>xiang/',
        'http://www.xiaolvji.com/u/aif(i)sh'
    ]:
        file = html_to_file_name(url)
        url2 = file_to_html_name(file)
        if url2 != url:
            logs.brief.info(f'Error {url2} {url}')
        logs.brief.info(f'{file} ===> {url2}')


async def async_read(path, encoding="utf-8"):
    async with aiofiles.open(path, encoding=encoding) as f:
        return await f.read()


async def async_write(txt, path, mod='w', encoding="utf-8"):
    assert mod in ['w', 'a']
    async with aiofiles.open(path, mod, encoding=encoding) as f:
        await f.write(txt)


async def async_write_html(url, path, charset=None, proxy=False):
    resp = await async_get(url, proxy=proxy)
    if charset:
        text = resp.content.decode(charset, "ignore")
        await async_write(text, path, mod='w', encoding=charset)
    else:
        text = resp.text
        await async_write(text, path, mod='w', encoding="utf-8")


class Etree:
    def __init__(self, html, url, node=None):
        """
        :param html: 网页的文本内容
        :param url:  网页地址
        """
        if node is None:
            self.tree = lxml.etree.HTML(html)
        else:
            self.tree = node
        self.raw_url = url

    def url(self, path):
        # path中的键名必须是小写的（不区分大小写）， 而值是区分大小写的
        out = self.txt(path)
        out = urljoin(self.raw_url, out) if out else ''
        return out

    def urls(self, path):
        # path中的键名必须是小写的（不区分大小写）， 而值是区分大小写的
        ts = self.txts(path)
        out = [urljoin(self.raw_url, t) if t else '' for t in ts]
        return out

    @staticmethod
    def trans_txt(txt):
        if isinstance(txt, lxml.etree._Element):
            txt = txt.text
            if txt is None:
                return None
        txt = txt.replace(u'\xa0', u'')  # \xa0 是不间断空白符
        txt = txt.replace(u'\u3000', u'  ')  # \u3000 是全角的空白符
        return txt

    def txt(self, path):
        # path中的键名必须是小写的（不区分大小写）， 而值是区分大小写的
        if not path:
            return ''
        resps = self.tree.xpath(path)
        out = resps[0] if resps else ''
        out = self.trans_txt(out)
        return out

    def txts(self, path):
        # path中的键名必须是小写的（不区分大小写）， 而值是区分大小写的
        nodes = self.tree.xpath(path)
        out = []
        for txt in nodes:
            txt = self.trans_txt(txt)
            if txt is not None:
                out.append(txt)
        return out

    def nodes(self, path):
        # path中的键名必须是小写的（不区分大小写）， 而值是区分大小写的
        trees = self.tree.xpath(path)
        out = [Etree(html='', url=self.raw_url, node=tree) for tree in trees if tree is not None]
        return out

    def __str__(self):
        return lxml.etree.tostring(self.tree).decode('utf8')

    def __getitem__(self, item):
        return self.tree.attrib[item]

    def __setitem__(self, key, value):
        self.tree.attrib[key] = value
