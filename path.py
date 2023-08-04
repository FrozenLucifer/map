import json


# with open('data.json', 'r') as data:
#     V = json.load(data)


def find_min_ind(a: list, u: list, l: int):
    min_value = None
    min_index = None
    for i in range(l):
        if not u[i] and a[i] != float('inf') and (min_value is None or a[i] < min_value):
            min_index = i
            min_value = a[i]
    return min_index


def get_path(prev, end):
    path = [end]
    i = end
    while prev[i] != -1:
        path.append(prev[i])
        i = prev[i]
    return list(reversed(path))


def find_path(data, start, end):
    l = len(data)

    distances = [float('inf')] * l
    distances[start] = 0

    prev = [0] * l
    prev[start] = -1

    visited = [False] * l

    while False in visited:
        x = find_min_ind(distances, visited, l)
        if x is not None:
            _, _, cons = data[x]
            for i, dst in cons:
                if not visited[i]:
                    if dst + distances[x] < distances[i]:
                        distances[i] = dst + distances[x]
                        prev[i] = x
            visited[x] = True
        else:
            break
    if distances[end] != float('inf'):
        print(f'Путь от {start} до {end}:')
        print(*get_path(prev, end), sep=' -> ')
        print(f'Длина: {distances[end]}')
        print('-' * 20)
        return get_path(prev, end), distances[end]
    else:
        print(f'Пути от {start} до {end} не существует')
        return None, None


if __name__ == '__main__':
    with open('data_tmp.json', 'r') as data:
        V = json.load(data)
    find_path(V, 1, 0)
