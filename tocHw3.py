# ----------------------------------------------------------------------------
#
# Name: Jie Han Chen(JIElite)
# Student ID: F74016077
#
# This code is including 3 function:
#   1. get_outlink_list(fd, reversable)
#   2. get_link_number(website)
#   3. print_data(weblist, top)
#
# The first function is using for get a sorted list of input data, the element
# is consist of  [webURI, outlink number]. You can choose the data list is
# ascending or descending.
#
# The second function: get_link_number(website) is using for get the number of
# outlink for each URI. It use regex to parse the json-like data.
#
# The third function: print_data(weblist, top) has to parameter. The first is
# for input list which is the result of get_outlink_list(fd, reversable), and
# The second parameter is for request.
#
# ----------------------------------------------------------------------------

import sys
import operator
import os.path
import re
import time


def print_data(weblist, top):
    """
    print_data(weblist, top) is using for output the data which is requested
    by user. If the user request 10 data, it should check fallthrough whether
    the outlink number of 11th data is as same as 10th.
    """
    num_of_data = len(weblist)

    for i in xrange(top):
        try:
            print "{0}:{1}".format(weblist[i][0], weblist[i][1])
        except IndexError:
            print "Your request is more than total number of data"
            print "There are total: {0} data".format(num_of_data)
            return

    # Processing the remaining webpage with same outlink number
    if top < num_of_data:
        try:
            while weblist[top-1][1] == weblist[top][1]:
                print "{0}:{1}".format(weblist[top][0], weblist[top][1])
                top = top + 1
        except IndexError:
            return
    return


def get_link_number(line_msg):
    """
    This function should be not public, and it can get outlink number of each
    website. It decide the number of outlink by using regex to search ''"url":'
    and '"href"' pattern. Finally, add the result for each pattern to get
    the number of outlink.
    """
    try:
        # Try to searh Outlinks, if return match object, means there
        # exist some outlinks of this uri
        links = re.search(r'"Links":\[{.+}\](,"Head"|},"Entity-Digest")', line_msg)
        list_links = links.group()

        find_url = re.findall(r'"url":', list_links)
        num_of_url = len(find_url)

        find_href = re.findall(r'"href":', list_links)
        num_of_href = len(find_href)

        num_of_outlink = num_of_href + num_of_url
    except AttributeError:
        # This means there are no "Links" tag
        num_of_outlink = 0

    return num_of_outlink


def get_outlink_list(fd, reversable):
    '''
    This function return a sorted list, the key depends on number of outlink.
    The second parameter is for choosing the outlink is ascending(reversable = True)
    or descending(reversable = False). Finally it returns a list including
    [website uri, outlink number ] as each element in the list.
    '''
    weblist = []

    for line_msg in fd:
        url = re.search('"WARC-Target-URI":"([^"]*)"', line_msg)
        num_of_outlink = get_link_number(line_msg)
        weblist.append([url.group(1), num_of_outlink])

    weblist.sort(key=operator.itemgetter(1), reverse=reversable)
    return weblist


if __name__ == "__main__":

    start_time = time.time()

    try:
        filename = sys.argv[1]
        if os.path.exists(filename):
            pass
        else:
            raise IOError
    except IndexError:
        print "There is no input file"
        sys.exit(0)
    except IOError:
        print "There is no such file: {0}".format(filename)
        sys.exit(0)

    with open(filename, "r") as fd:
        try:
            top_k = int(sys.argv[2])
        except IndexError as index_err:
            print "There is no input top_k"
            sys.exit(0)
        except ValueError:
            print "The top_k must be integer"
            sys.exit(0)
        weblist = get_outlink_list(fd, True)
        print_data(weblist, top_k)

    finish_time = time.time()
    print "Elapsed Time: ", finish_time - start_time
