from dataconverters import xls


__all__ = ['parse']


def parse(*args, **kwargs):
    kwargs['excel_type'] = 'xlsx'
    return xls.parse(*args, **kwargs)
