def dedent_text(text: str):
    return '\n'.join([m.lstrip() for m in text.split('\n')]).strip()


def prompt_template(dedent=True, fix_whitespace=True):
    def real_decorator(func):
        def wrapper(*args, **func_kwargs):
            result = func(*args, **func_kwargs)
            if dedent:
                result = dedent_text(result)
            if fix_whitespace:
                result = result.strip()
            return result

        return wrapper

    return real_decorator
