# explain.py
# オブジェクトの中身を表示する
# python でよくわからないオブジェクトの中身を表示する
# https://qiita.com/halhorn/items/7b8351c5eafbfa28d768

import types


def explain(item, shows_private=False, shows_method=False):
    '''
    与えた python オブジェクトの詳細を表示します。
    '''
    print('EXPLAIN ------------------')
    print(item)
    print(type(item))
    print('ATTRIBUTES:')
    for d in dir(item):
        if d == 'type':
            continue
        if not shows_private and d.startswith('_'):
            continue
        attr = getattr(item, d)
        if not shows_method and (
                isinstance(attr, types.MethodType) or
                isinstance(attr, types.BuiltinMethodType) or
                isinstance(attr, types.CoroutineType) or
                isinstance(attr, types.FunctionType) or
                isinstance(attr, types.BuiltinFunctionType) or
                isinstance(attr, types.GeneratorType)
        ):
            continue
        print('{}:\t{}'.format(d, attr))
