import pprint
import json


def graph() -> dict:
    from networkx.generators.random_graphs import erdos_renyi_graph
    import random
    n = random.choice([1,2,3,4,5,6,7,8,9,10])
    p = random.choice([0.3, 0.4, 0.5])
    g = erdos_renyi_graph(n, p)
    print(f"Nodes: {g.nodes}\n"
          f"Edges: {g.edges}")
    return {
        "nodes": list(g.nodes),
        "edges": list(g.edges)
    }

if __name__ == '__main__':
    # g = graph()
    # pprint.pprint(json.dumps(g))
    # for i in range(0,5):
    #     graph()
    test = {
        "1": {
            "test": "Hi"
        },
        "2": "Not"
    }
    test.setdefault("default", "this is default")
    # test.update({
    #     "hello":1
    # })
    test["1"]["test"] = "fuck"
    shit = test.get("1").copy()
    test["1"]["test"] = "fuck"
    pprint.pprint(shit)
    pprint.pprint(test)


