import typer

from appgallery_spy.crawl import crawl as appgallery_crawl

app = typer.Typer()


@app.command()
def crawl(app_id: str):
    typer.echo("Crawling the appgallery..")
    appgallery_crawl(app_id)


if __name__ == "__main__":
    app()
