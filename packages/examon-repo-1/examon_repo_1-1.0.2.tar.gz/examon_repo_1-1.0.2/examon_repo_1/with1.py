from examon_core.examon_item import examon_item



@examon_item(choices=[3, None, 'enter'], tags=['with', 'moderate'])
def question_01():
    class LookingGlass:
        def __enter__(self):
            return 'enter'

        def __exit__(self, exc_type, exc_value, traceback):
            return 'exit'

    with LookingGlass() as what:
        return what
