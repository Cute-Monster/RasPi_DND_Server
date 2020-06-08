import pprint
import json

def my_wrapper(func):
    def method_decor(x):
        if x <5:
            func(x)
    return method_decor


@my_wrapper
def testing_this(x):
    print(x)


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


class TestExcepion(Exception):
    pass

if __name__ == '__main__':
    levels = {
        (1, 3): "test",
        (4, 6): "Hello"
    }
    for item in list(levels.keys()):
        if item[0] <= 2 <= item[1]:
            pprint.pprint(levels[item])


    # pprint.pprint(levels)
    # test['first'] = {
    #     "her": 45
    # }
    #
    # if test['first']:
    #     print("her")
    #     pprint.pprint(test)
    # else:
    #     print("Hui")
    # g = graph()
    # pprint.pprint(json.dumps(g))
    # for i in range(0,5):
    #     graph()
    # test = {
    #     "1": {
    #         "test": "Hi"
    #     },
    #     "2": "Not"
    # }
    # test.setdefault("default", "this is default")
    # # test.update({
    # #     "hello":1
    # # })
    # test["1"]["test"] = "fuck"
    # shit = test.get("1").copy()
    # test["1"]["test"] = "fuck"
    # pprint.pprint(shit)
    # pprint.pprint(test)
    # try:
    #     for word in ['test', "HELLO"]:
    #         if word.isupper():
    #             raise TestExcepion("Word is upper")
    # except TestExcepion as test:
    #     print(test.withtraceback(test))

