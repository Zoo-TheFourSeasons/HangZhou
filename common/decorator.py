from flask import make_response, request


def make_response_with_headers(data):
    response = make_response(data)
    response.headers['Connection'] = 'Keep-Alive'
    # response.headers['Access-Control-Allow-Origin'] = 'http://localhost:63342'
    response.headers['Access-Control-Allow-Credentials'] = 'true'

    return response


def data_paging(ins, key_name, exclude=None, fields=None):
    items = sorted(ins.keys())
    if 'search' in request.args and request.args['search']:
        search = request.args['search']

        items_ = []
        if fields:
            for k in fields:
                for item in items:
                    v = ins[item][k]
                    # print('v: ' + v + ' k: ' + k + ' search: ' + search)
                    if v == search:
                        items_.append(item)
                        continue

            for item in items:
                if search in item and item not in items_:
                    items_.append(item)
        else:
            items_ = [item for item in items if search in item]
        items = items_

    total = len(items)

    if 'sort' in request.args and 'order' in request.args:
        sort = request.args['sort']
        order = request.args['order']
        if sort and order:
            items_need_sort = (item for item in items if sort in ins[item])
            items_cannot_sort = [item for item in items if sort not in ins[item]]
            items_sort = ((item, ins[item][sort]) for item in items_need_sort)
            if order == 'asc':
                items_sort = sorted(items_sort, key=lambda x: x[1])
            else:
                items_sort = sorted(items_sort, key=lambda x: x[1], reverse=True)
            items = [item[0] for item in items_sort] + items_cannot_sort

    if 'offset' in request.args and 'limit' in request.args:
        offset = request.args['offset']
        limit = request.args['limit']
        if offset and limit:
            items = items[int(offset): int(offset) + int(limit)]

    rows = []
    for item in items:
        temp = ins[item]
        if exclude:
            for ex in exclude:
                temp.pop(ex, None)

        temp.update({key_name: item, 'id': item})
        rows.append(temp)
    return total, rows
