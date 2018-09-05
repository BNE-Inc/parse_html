import re
import requests
from lxml import html, etree
import traceback


ch_dict = {'０':'0', '１':'1', '２':'2','３':'3','４':'4','５':'5','６':'6','７':'7','８':'8','～':'~',
'９':'9','ａ':'a','Ａ':'A','ｂ':'b','Ｂ':'B','ｃ':'c','Ｃ':'C','ｄ':'d','Ｄ':'D','ｅ':'e','Ｅ':'E',
'ｆ':'f','Ｆ':'F','ｇ':'g','Ｇ':'G','ｈ':'h','Ｈ':'H','ｉ':'i','Ｉ':'I','ｊ':'j','Ｊ':'J','ｋ':'k','Ｋ':'K',
'ｌ':'l','Ｌ':'L','ｍ':'m','Ｍ':'M','ｎ':'n','Ｎ':'N','ｏ':'o','Ｏ':'O','ｐ':'p','Ｐ':'P','ｑ':'q','Ｑ':'Q',
'ｒ':'r','Ｒ':'R','ｓ':'s','Ｓ':'S','ｔ':'t','Ｔ':'T','ｕ':'u','Ｕ':'U','ｖ':'v','Ｖ':'V','ｗ':'w','Ｗ':'W',
'ｘ':'x','Ｘ':'X','ｙ':'y','Ｙ':'Y','ｚ':'z','Ｚ':'Z','！':'!','＂':'"','＃':'#','＄':'$','％':'%','＆':'&',
'＇':"'",'（':'(','）':')','＊':'*','＋':'+','，':',','－':'-','．':'.','／':'/','：':':','；':';','＜':'<',
'＝':'=','＞':'>','？':'?','＠':'@','［':'[','＼':'\\','］':']','＾':'^','＿':'_','｀':'`','｛':'{','｜':'|',
'｝':'}','｟':'⦅','｠':'⦆','￠':'¢','￡':'£','￢':'¬','￣':'¯','￤':'¦','￥':'¥','￦':'₩','│':'￨','←':'￩',
'↑':'￪','→':'￫','↓':'￬','■':'￭','○':'￮','　':' ','ｱ':'ア','ｲ':'イ','ｳﾞ':'ヴ','ｳ':'ウ','ｴ':'エ','ｵ':'オ','ｰ':'ー',
'ｶﾞ':'ガ','ｶ':'カ','ｷﾞ':'ギ','ｷ':'キ','ｸﾞ':'グ','ｸ':'ク','ｹﾞ':'ゲ','ｹ':'ケ','ｺﾞ':'ゴ','ｺ':'コ','ｻﾞ':'ザ','ｻ':'サ',
'ｼﾞ':'ジ','ｼ':'シ','ｽﾞ':'ズ','ｽ':'ス','ｾﾞ':'ゼ','ｾ':'セ','ｿﾞ':'ゾ','ｿ':'ソ','ﾀﾞ':'ダ','ﾀ':'タ','ﾁﾞ':'ヂ','ﾁ':'チ',
'ﾂﾞ':'ヅ','ﾂ':'ツ','ﾃﾞ':'デ','ﾃ':'テ','ﾄﾞ':'ド','ﾄ':'ト','ﾅ':'ナ','ﾆ':'ニ','ﾇ':'ヌ','ﾈ':'ネ','ﾉ':'ノ','ﾊﾞ':'バ',
'ﾊﾟ':'パ','ﾊ':'ハ','ﾋﾞ':'ビ','ﾋﾟ':'ピ','ﾋ':'ヒ','ﾌﾞ':'ブ','ﾌﾟ':'プ','ﾌ':'フ','ﾍﾞ':'ベ','ﾍﾟ':'ペ','ﾍ':'ヘ','ﾎﾞ':'ボ',
'ﾎﾟ':'ポ','ﾎ':'ホ','ﾏ':'マ','ﾐ':'ミ','ﾑ':'ム','ﾒ':'メ','ﾓ':'モ','ﾔ':'ヤ','ﾕ':'ユ','ﾖ':'ヨ','ﾗ':'ラ','ﾘ':'リ',
'ﾙ':'ル','ﾚ':'レ','ﾛ':'ロ','ﾜ':'ワ','ﾜﾞ':'ヷ','ｦ':'ヲ','ｦﾞ':'ヺ','ﾝ':'ン','ｧ':'ァ','ｨ':'ィ','ｩ':'ゥ','ｪ':'ェ',
'ｫ':'ォ','ｬ':'ャ','ｭ':'ュ','ｮ':'ョ','ｯ':'ッ','ﾞ':'゛','ﾟ':'゜','､':'、','｡':'。','･':'・','｢':'「','｣':'」'}


two_byte_exp = r'[ａ-ｚＡ-Ｚ０-９！＂＃＄％＆＇（）＊＋，,－．／：；＜＝＞？＠［＼］＾＿｀｛｜｝～｟｠￠￡￢￣￤￥￦│←↑→↓■○　｡-･ｧ-ｲｴｵﾅ-ﾉﾏ-ﾛﾝ-ﾟ]|[ｦｳｶ-ﾄﾜ]ﾞ?|[ﾊ-ﾎ][ﾞ|ﾟ]?'
p = re.compile (two_byte_exp)
s = re.compile (r'\s+')


def two_byte_to_single_dict(m):
    if m.group(0) in ch_dict:
        return ch_dict[m.group(0)]
    else:
        return ''


def normalize(string):
    return p.sub (two_byte_to_single_dict, string)


def adjust_space (string):
    return s.sub (' ', string)


def parse_selector (selectors):
    output = ''
    if selectors:
        for selector in selectors:
            if selector.text:
                cleaned_text = normalize(adjust_space(selector.text).strip())
                if len(cleaned_text) > 0:
                    if len(output) == 0:
                        output = cleaned_text
                    else:
                        output += ' ' + cleaned_text
    return output


class parse_html:
    def __init__(self, url):
        r = requests.get(url)
        self.output = ''
        if r.status_code == 200:
            try:
                r.encoding = r.apparent_encoding
                self.response = html.fromstring(r.text)
            except:
                self.response = None
        else:
            self.response = None

    def concat_text(self, new_text):
        if len(new_text) > 0:
            if len(self.output) == 0:
                self.output = new_text
            else:
                self.output += ' ' + new_text

    def parse(self, tags):
        if self.response is not None:
            tags = set(tags)
            if 'title' in tags:
                selectors = self.response.xpath ('//title')
                if selectors:
                    parsed_text = parse_selector(selectors)
                    self.concat_text(parsed_text)
                tags.discard ('title')
            if 'content' in tags:
                content = self.response.xpath ("//meta[@name='description']/@content")
                parsed_text = content[0] if content else ''
                self.concat_text(parsed_text)
                tags.discard ('content')
            if 'p' in tags or 'h1' in tags or 'h2' in tags or 'h3' in tags or 'h4' in tags or 'h5' in tags or 'h6' in tags:
                xpath_keys = "//body//*["
                cnt = 0
                for tag in tags:
                    if tag in {'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
                        if cnt == 0:
                            xpath_keys += "(self::{})".format (tag)
                        else:
                            xpath_keys += " or (self::{})".format (tag)

                        cnt += 1
                if cnt > 0:
                    xpath_keys += "]"
                    selectors = self.response.xpath(xpath_keys)
                    if selectors:
                        parsed_text = parse_selector(selectors)
                        self.concat_text(parsed_text)
        return self

    def get_text(self):
        return self.output

    def clean_text(self):
        self.output = ''
