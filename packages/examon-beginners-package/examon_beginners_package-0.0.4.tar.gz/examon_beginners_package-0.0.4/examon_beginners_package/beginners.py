from functools import wraps
from examon_core.examon_item_registry import ExamonItemRegistry
from examon_core.question_factory import QuestionFactory


def examon_item(choices=None, tags=None, hints=None,
                generated_choices=None, param1=None):
    def inner_function(function):
        processed_question = QuestionFactory.build(
            function=function, choice_list=choices,
            tags=tags, hints=hints,
            generated_choices=generated_choices,
            param1=param1, metrics=True)
        ExamonItemRegistry.add(processed_question)
        return function

        # @wraps(function)
        # def wrapper(*args, **kwargs):
        #     function(*args, **kwargs)
        #     return wrapper

    return inner_function

@examon_item(choices=[
    'Hello, Bob. How are you?', 'Hello, Jeff. How are you?',
    'Hello, Bob.', 'Hello, Jeff.', '. How are you?'],
    tags=['strings'])
def question_11():
    name = 'Jeff'
    name = 'Bob'
    greeting = f'Hello, {name}'
    greeting += ". How are you?"
    return greeting

print(question_11())