from inspect import isawaitable
import json




async def async_all(gen, *, check=isawaitable):
    for elem in gen:
        if check(elem):
            elem = await elem
        if not elem:
            return False
    return True


async def maybe_coroutine(f, *args, **kwargs):
    value = f(*args, **kwargs)
    if isawaitable(value):
        return await value
    else:
        return value

def get_params_from_func(params,*iskl):
    p = {}
    for a,b in params.items():
        if a == "cls":
            continue
        elif a in iskl:
            continue
        elif b is None:
            continue
        else:
            p.update({a:b})
    return p

def get_params_from_class(params,*iskl):
    return get_params_from_func(params,*iskl)



def find(predicate, seq):
    for element in seq:
        if predicate(element):
            return element
    return None


def to_json(obj):
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=True)
