from jinja2schema.model import Dictionary, Scalar, List, Unknown, Tuple


def _format_attrs(var):
    return (u'label={0.label}, required={0.required}, '
            u'constant={0.constant}, linenos={0.linenos}').format(var).encode('utf-8')


def _indent(lines, spaces):
    indent = ' ' * spaces
    return [indent + line for line in lines]


def _debug_repr(var):
    rv = []
    if isinstance(var, (Dictionary, Tuple, List)):
        if isinstance(var, Dictionary):
            rv.append('Dictionary({}, {{'.format(_format_attrs(var)))
            content = []
            for key, value in var.iteritems():
                key_repr = key + ': '
                value_repr = _debug_repr(value)
                content.append(key_repr + value_repr[0])
                content.extend(_indent(value_repr[1:], spaces=len(key_repr)))
            rv.extend(_indent(content, spaces=4))
            rv.append('})')
        elif isinstance(var, Tuple):
            rv.append('Tuple({},'.format(_format_attrs(var)))
            for el in var.items:
                el_repr = _debug_repr(el)
                el_repr[-1] += ','
                rv.extend(_indent(el_repr, spaces=4))
            rv[-1] = rv[-1][:-1]  # remove comma from the last tuple item
            rv.append(')')
        elif isinstance(var, List):
            rv.append('List({},'.format(_format_attrs(var)))
            rv.extend(_indent(_debug_repr(var.item), spaces=4))
            rv.append(')')
    elif isinstance(var, Scalar):
        rv = ['Scalar({})'.format(_format_attrs(var))]
    elif isinstance(var, Unknown):
        rv = ['Unknown({})'.format(_format_attrs(var))]
    return rv


def debug_repr(var):
    return '\n'.join(_debug_repr(var))