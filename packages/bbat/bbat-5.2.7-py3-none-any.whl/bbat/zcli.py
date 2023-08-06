import typer

main = typer.Typer()

@main.command(help='hi')
def hi():
    from bbat import hi

@main.command()
def server(host='localhost', port:int=3306, user='root', password='123456', database='project'):
    from bbat.web.db_server import app
    from bbat.db.aio_mysql import Mysql
    
    print('>>>', f"mysql://{user}:{password}@{host}:{port}/{database}")
    db = Mysql(host, port, database, user, password)
    app.ctx.db = db
    app.run()



@main.command(help='md5加密')
def md5(val):
    from bbat.crypto import md5
    print(md5(val))


@main.command(help='base64加密，解密--decode')
def base64(val, decode:bool=False):
    from bbat.crypto import base64_encode, base64_decode
    if decode:
        print(base64_decode(val))
        return 
    print(base64_encode(val))



@main.command(help='机器--配置/使用量')
def machine():
    from bbat.machine import info
    [print(name, value) for name, value in info().items()]


@main.command(help='命令行chatGPT聊天')
def chatgpt(val, key="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"):
    from bbat.llm.chatgpt import generate
    import openai
    
    openai.api_key = key
    messages = [{'role': 'user', 'content': val}]
    for role, content in generate(messages):
        if role == 'role':
            continue
        print(content, flush=True, end="")


@main.command(help='有道翻译')
def translate(val):
    from bbat.text import Translator
    translator = Translator()
    print(translator(val), '\n')


if __name__ == "__main__":
    main()
