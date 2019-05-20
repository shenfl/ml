#
import os


def get_graph_from_data(input_file):
    if not os.path.exists(input_file):
        return {}
    graph = {}
    score_thr = 4
    fp = open(input_file)
    for line in fp:
        item = line.strip().split("::")
        if len(item) < 3:
            continue
        userid, itemid, rating = item[0], "item_" + item[1], item[2]
        if float(rating) < score_thr:
            continue
        if userid not in graph:
            graph[userid] = {}
        graph[userid][itemid] = 1
        if itemid not in graph:
            graph[itemid] = {}
        graph[itemid][userid] = 1
    fp.close()
    return graph


if __name__ == "__main__":
    graph = get_graph_from_data("ratings.dat")
    print(graph["1"])
