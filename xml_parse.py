import re
from urllib import unquote
import xml.etree.ElementTree as ET

def convert_url_to_dict(url):
    url_dict = dict()
    for param in url.split("&"):
        if '=' not in param:
            print("'=' not in %s" % param)
            break

        key, value = param.split("=")
        url_dict[key] = value

    return url_dict

def ET_XMLParser(xml_content, f):
    xmlp = ET.XMLParser(encoding="utf-8")
    try:
        root = ET.fromstring(xml_content.encode("utf8"), parser=xmlp)
    except Exception as e:
        print("parse xml failed %s") % str(e)
        f.write("error=%s\n" % str(e))
        return None

    return root

def _parsexml_get(request, response_content):
    def getxml(content, head_strip):
        xml = ''
        pat = re.compile(r"^%s\('(?P<xml>.*)'\)" % head_strip)
        r = pat.match(content)
        if r:
            xml = r.group('xml')
            #print(r.groups())
        return xml

    url_dict = convert_url_to_dict(request)
    try:
        query_word = unquote(url_dict["query"]).decode("utf8").encode("gbk")
    except Exception as e:
        print("unquote query: %s failed, %s" % (url_dict["query"], str(e)))
        return False

    if 'callback' not in url_dict:
        return None

    head_strip = url_dict["callback"]

    #print("query_word: %s" % query_word)
    xml_content = getxml(response_content, head_strip)

    f = open("get.result", "a")
    f.write("[%s]\n" % query_word)
    root = ET_XMLParser(xml_content, f)
    if root is None:
        return None

    for headinfo in root.findall('headinfo'):
        for sql_key in ["sqlstring1", "sqlstring"]:
            sql_value = (headinfo.get(sql_key) or "").strip()
            #print("%s=%s" % (sql_key, sql_value.encode("gbk")))
            f.write("%s=%s\n" % (sql_key, sql_value.encode("gbk")))

    f.close()

    f = open("get.url", "a")
    f.write("%s:\n" % query_word)
    for key in ["picaddress", "wapurl"]:
        elements = root.findall('.//*[@%s]' % key)
        for e in elements:
            url =  e.get(key) or "not exist"
            #print("%s=%s" % (key, url))
            f.write("- url: %s\n" % url)
            f.write("  status: untest\n")
            f.write("  flag: %s\n" % key)

    elements = root.findall('.//imgsrc')
    for imgsrc in elements:
        url = imgsrc.text or "not exist"
        #print("imgsrc=%s" % url)
        f.write("- url: %s\n" % url)
        f.write("  status: untest\n")
        f.write("  flag: imgsrc\n")

    f.close()

    #print("%s" % (xml_content.encode("gbk")))
    return ''
def _parsexml_post(request, response_content):
    url_dict = convert_url_to_dict(request)
    try:
        query_word = unquote(url_dict["queryString"]).decode("utf16").encode("gbk")
    except Exception as e:
        print("unquote queryString: %s failed, %s" % (url_dict["queryString"], str(e)))
        return False

    f = open("post.result", "a")
    f.write("[%s]\n" % query_word)
    root = ET_XMLParser(response_content, f)
    if root is None:
        return False

    for headinfo in root.findall('headinfo'):
        for sql_key in ["sqlstring1", "sqlstring2"]:
            sql_value = (headinfo.get(sql_key) or "").strip()
            #print("%s=%s" % (sql_key, sql_value.encode("gbk")))
            f.write("%s=%s\n" % (sql_key, sql_value.encode("gbk")))
    f.close()

    f = open("post.url", "a")
    f.write("%s:\n" % query_word)
    for key in ["picaddress", "wapurl"]:
        elements = root.findall('.//*[@%s]' % key)
        for e in elements:
            url =  e.get(key) or "not exist"
            #print("%s=%s" % (key, url))
            f.write("- url: %s\n" % url)
            f.write("  status: untest\n")
            f.write("  flag: %s\n" % key)

    elements = root.findall('.//imgsrc')
    for imgsrc in elements:
        url = imgsrc.text or "not exist"
        #print("imgsrc=%s" % url)
        f.write("- url: %s\n" % url)
        f.write("  status: untest\n")
        f.write("  flag: imgsrc\n")

    f.close()
    #print("%s" % (response_content.encode("gbk")))
    return ""

def parsexml(method = 'get', request = '', response_content = ''):
    #print("%s: %s" % (method, request))

    if method == 'get':
        return _parsexml_get(request, response_content)
    elif method == 'post':
        return _parsexml_post(request, response_content)
    else:
        print("incorrect method %s" % method)

    return None

