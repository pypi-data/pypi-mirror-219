from sanic import Sanic, response
from sanic.exceptions import RequestTimeout, NotFound
from sanic.log import logger, access_logger, error_logger
from bbat.path import mkdir
from bbat.web import cors


app = Sanic('sanic_app')


# index
@app.route("/")
def ping(request):
    return response.text('Forbidden')

# Public static dir
mkdir('./static')
app.static('/static', './static/')

# middleware
@app.middleware("request")
async def before_request(request):
    if request.method == "OPTIONS":
        headers = cors.get_headers()
        return response.json({"code": 0}, headers=headers)

# Exception defined
@app.exception(RequestTimeout)
def timeout(request, exception):
    return response.json({"msg": "Request Timeout", "code": 408}, 408)

@app.exception(NotFound)
def notfound(request, exception):
    error_logger.warning("URI calledMy: {0} {1}".format(request.url, exception))
    return response.json({"msg": f"Requested URL {request.url} not found", "code": 404}, 404)

@app.exception(Exception)
def notfound(request, exception):
    error_logger.exception(exception)
    err = str(exception)
    return response.json({"msg": f"{err}", "code": -1}, status=200, ensure_ascii=False)


# Common Function
def resp(code=0, msg="", data={}):
    return response.json({"code": code, "msg": msg, "data": data}, ensure_ascii=False, default=str)

def success(result, msg="success"):
    return resp(code=0, msg=msg, data=result)

def error(msg="error", result={}):
    return resp(code=-1, msg=msg, data=result)