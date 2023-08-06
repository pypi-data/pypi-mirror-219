import image_sky


def simple_foo(x):
    return 10*x


if __name__ == "__main__":
    wrenexec = image_sky.default_executor()
    #f = wrenexec.call_async(simple_foo, 10)
    #zz = f.result()

    futures = wrenexec.map(simple_foo, [19,11,13,14,15])
    zz = image_sky.get_all_results(futures)
    print(zz)