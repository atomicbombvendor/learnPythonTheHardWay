import web

urls = (
    '/hello', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('../templates/')


class Index(object):
    def GET(self):
        # 默认的参数值，如果url中没有参数值就会报错
        form = web.input(name="Nobody", greeting="greeting")
        greeting2 = "Hello, %s, %s" % (form.name, form.greeting)

        return render.foo(greeting = greeting2)

    def POST(self):
        form = web.input(name="Nobody", greet="hello")
        greeting = "%s, %s" % (form.greet, form.name)
        return render.foo(greeting=greeting)

if __name__ == "__main__":
    app.run()