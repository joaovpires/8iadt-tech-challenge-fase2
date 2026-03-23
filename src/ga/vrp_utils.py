import math

DEPOT = 0


def euclidean(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def split_routes_by_depot(chromosome):
    routes = []
    current = []

    for gene in chromosome:
        if gene == DEPOT:
            if current and current != [DEPOT]:
                current.append(DEPOT)
                routes.append(current)
            current = [DEPOT]
        else:
            current.append(gene)

    if current and current != [DEPOT]:
        current.append(DEPOT)
        routes.append(current)

    return routes


def build_points(deliveries):
    return {d.id: d for d in deliveries}


def count_missing_clients(chromosome, deliveries):
    expected = {d.id for d in deliveries if d.id != DEPOT}
    visited = [g for g in chromosome if g != DEPOT]
    return len(expected - set(visited))


def count_duplicate_clients(chromosome):
    seen = set()
    duplicates = 0

    for g in chromosome:
        if g == DEPOT:
            continue
        if g in seen:
            duplicates += 1
        else:
            seen.add(g)

    return duplicates