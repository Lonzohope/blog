from .models import Quote
import urllib.request,json



base_url=None

def configure_request(app):
    global base_url
    base_url=app.config['QUOTE_BASE_URL']

def get_quote():
    get_quote_url=base_url.format()
    with urllib.request.urlopen(get_quote_url) as url:
        get_quote_data=url.read()
        get_quote_response=json.loads(get_quote_data)
        quote_results=None
        quote_results=get_quote_response
        quote_results=process_result(quote_results)


    return quote_results

def process_result(quote_list):
    quote_result=[]

    quote=quote_list
    author=quote_list

    quote_obj=Quote(quote,author)
    quote_result.append(quote_obj.quote)

    return quote_result
