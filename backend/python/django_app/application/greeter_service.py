# implement port contract using domain logic
# use case, what should happen when someone calls this feature

from django_app.domain.greeting import greeting


def greet(name):
    return greeting(name)
