import os


class Job(object):

    def __init__(self, url, output_path):
        self._url = url
        self._output_path = output_path
        self._attempts = 0

    def url(self):
        return self._url

    def output_path(self):
        return self._output_path

    def attempts(self):
        return self._attempts

    def record_attempt(self):
        self._attempts += 1


def from_url_dict(url_dict, output_root):
    jobs = []
    for key, url in url_dict.iteritems():
        extension = os.path.splitext(url)[1]
        if not extension:
            extension = '.jpg'
        output_filename = key + extension
        output_path = os.path.join(output_root, output_filename)
        jobs.append(Job(url, output_path))
    return jobs
