from filters_sdk import FilterList, Filter, preinstalled_filters_list
from filter_types import FilterType, FilterParam
import math


def main():
    filter_list = FilterList()

    preinstalled_filters = preinstalled_filters_list()
    print(preinstalled_filters)

    elem1 = Filter()
    param = FilterParam(FilterType.ft_band_stop, 250, 100)
    elem1.init_by_param(param)

    elem2 = Filter()
    elem2.init_by_param(FilterParam(FilterType.ft_band_stop, 250, 60))

    elem3 = Filter()
    elem3.init_by_param(FilterParam(FilterType.ft_band_stop, 250, 50))

    filter_list.add_filter(elem1)
    filter_list.add_filter(elem2)
    filter_list.add_filter(elem3)

    rawData = [math.sin(50*x)*2*3.14/180 for x in range(10)]
    print(rawData)
    rawData = filter_list.filter_array(rawData)
    print(rawData)

    del elem1
    del elem2
    del elem3

    del filter_list


if __name__ == '__main__':
    main()
