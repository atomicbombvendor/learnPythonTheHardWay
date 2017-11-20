import web

urls = (
    '/','index'
)

app = web.application(urls, globals())


class index(object):
    def POST(self):
        greeting = "Hello World"
        return greeting

    def GET(self):
        # 默认调用GET方法
        greeting = "Hello World"
        return greeting


if __name__ == "__main__":
    app.run()