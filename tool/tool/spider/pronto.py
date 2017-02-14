import re

from .spider import Spider

class ProntoSpider(Spider):
    pronto_url = 'https://pronto.inside.nsn.com/pronto/problemReportSearch.html?freeTextdropDownID=prId&searchTopText=%s'
    analysis_url = 'https://pronto.inside.nsn.com/pronto/viewFaultAnalysis.html?fID=%s'

    def __init__(self, username, password):
        Spider.__init__(self, username, password)
        self.site = 'pronto'
    
    def collect_one_pronto(self, pid):
        html = self.get_page(self.pronto_url % pid)
        soup = self.get_soup(html)

        if_error = soup.find('span', 'error_nosearch')
        if None != if_error:
            return None

        ret = {}
        
        state = soup.find('div', 'current_status').get_text()
        ret['state'] = state

        tabs = soup.find_all('div', 'tab')
        for tab in tabs:
            title = tab.find('div', 'tit').get_text()
            if 'Fault Analysis' == title:
                ret['analysis'] = tab.find('a', 'text_decoration').get_text().strip()
                break

        blocks = soup.find_all('div', 'fieldBlock')
        for block in blocks:
            field = block.find('div', 'FieldName')
            if None == field:
                continue

            link = field.find('a', 'clickme')
            if None == link:
                continue

            key = link.get('title')
            value = block.find('div', 'inputBlock')
            if 'Title' == key:
                ret['title'] = value.get_text()
            elif 'Group in Charge' == key:
                group = value.get_text()
                ret['group'] = group
            elif 'Software' == key:
                value = value.find_all('li', 'breakWD')
                ret['release'] = value[0].get_text()
                ret['build'] = value[1].get_text()
            elif 'Additional' == key:
                value = value.find('input').get('value')
                monsho = re.findall(r'eNB-P-(\d{2}[AB]-\d{4}-\d{5})', value)
                if 0 != len(monsho):
                    ret['monsho'] = monsho[0]
                else:
                    ret['monsho'] = ''

        html = self.get_page(self.analysis_url % ret['analysis'])
        soup = self.get_soup(html)

        blocks = soup.find_all('div', 'fieldBlock')
        for block in blocks:
            field = block.find('div', 'FieldName')
            if None == field:
                continue

            link = field.find('a', 'clickme')
            if None == link:
                continue

            key = link.get('title')
            value = block.find('div', 'inputBlock')
            if 'Responsible Person' == key:
                ret['person'] = value.get_text()

        return ret






