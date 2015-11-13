def get_run_length(arr, start):
    ret = 1

    for v in arr[start:]:
        if v == 0:
            ret += 1
        else:
            return ret

    return ret

def gen(runs, named_data):
    export = []
    i = 0

    while i < len(runs):
       run = get_run_length(runs, i)
       export.append((named_data[i].lat, named_data[i].lon, run))
       i += run

    return export
