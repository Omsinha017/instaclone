from instaclone.celery import app

@app.task(name='sum_two_numbers')
def add(x, y):
    return x+ y