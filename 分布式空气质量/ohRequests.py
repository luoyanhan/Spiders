import requests
from faker import Faker


class ohRequests(object):
    def __init__(self, retries=1):
        self.faker = Faker()
        self.GET = 'get'
        self.POST = 'post'
        self.RETRIES = retries

    def __request(self,
                  method,
                  url,
                  headers={},
                  cookies=None,
                  proxies=None,
                  params=None,
                  data=None,
                  timeout=5):

        headers['user-agent'] = self.faker.user_agent()

        for i in range(self.RETRIES):
            req_methond = requests.post if method == 'post' else requests.get

            try:
                response = req_methond(url,
                                       headers=headers,
                                       cookies=cookies,
                                       proxies=proxies,
                                       data=data,
                                       timeout=timeout,
                                       params=params
                                       )
                response.encoding = 'utf-8'
                return response.text

            except Exception as e:
                print('HTTPError, Msg: {}'.format(e))

            print("Requests Error. Retry[{}], max retries[{}]".format(i + 1, self.RETRIES))

        return None

    def get(self, url, **kwargs):
        return self.__request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.__request('post', url, **kwargs)

    def faker_user_agent(self):
        return self.faker.user_agent()


if __name__ == '__main__':
    r = ohRequests()
    req = r.get("http://aqicn.org/city/all/cn/")
    print(req)