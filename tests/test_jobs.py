import unittest

from downloader import jobs


class JobTest(unittest.TestCase):

    def test_constructor(self):
        job = jobs.Job('http://www.mock.com/image.jpg',
                       '/dummy/output/path.jpg')
        self.assertEqual(job.url(), 'http://www.mock.com/image.jpg')
        self.assertEqual(job.output_path(), '/dummy/output/path.jpg')
        self.assertEqual(job.attempts(), 0)

    def test_record_attempt_increments_attempts(self):
        job = jobs.Job('http://www.mock.com/image.jpg',
                       '/dummy/output/path.jpg')
        self.assertEqual(job.attempts(), 0)
        job.record_attempt()
        self.assertEqual(job.attempts(), 1)
        job.record_attempt()
        self.assertEqual(job.attempts(), 2)


class FromUrlDictTest(unittest.TestCase):

    def assertJobsEqual(self, job_a, job_b):
        self.assertEqual(job_a.url(), job_b.url())
        self.assertEqual(job_a.output_path(), job_b.output_path())
        self.assertEqual(job_a.attempts(), job_b.attempts())

    def test_builds_job_list(self):
        job_list = jobs.from_url_dict({
            'foo-key':
            'https://mock.com/image-foo.jpg',
            'bar-key':
            'https://bar-page.com/image2.png',
            'baz-key':
            'https://wizzbang.com/bang.jpeg',
            'fwop-key':
            'https://qwer.com/img',
        }, '/dummypath/')
        job_list.sort(key=lambda j: j.url())
        self.assertJobsEqual(job_list[0],
                             jobs.Job('https://bar-page.com/image2.png',
                                      '/dummypath/bar-key.png'))
        self.assertJobsEqual(job_list[1],
                             jobs.Job('https://mock.com/image-foo.jpg',
                                      '/dummypath/foo-key.jpg'))
        self.assertJobsEqual(job_list[2],
                             jobs.Job('https://qwer.com/img',
                                      '/dummypath/fwop-key.jpg'))
        self.assertJobsEqual(job_list[3],
                             jobs.Job('https://wizzbang.com/bang.jpeg',
                                      '/dummypath/baz-key.jpeg'))
