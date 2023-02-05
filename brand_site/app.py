from . import create_app

app = create_app()


@app.template_filter()
def replace_n(value):
    return value.replace('\n', '<br />')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
