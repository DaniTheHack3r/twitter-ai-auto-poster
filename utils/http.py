import aiohttp

class HTTPManager():
    def __init__(self):
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*'
        }

    def __join_headers(self, additional_headers):
        return {**self.default_headers, **additional_headers}

    async def get(self, url: str, additional_headers: dict = {}):
        headers = self.__join_headers(additional_headers)

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                json = await response.json()
                status = response.status

                return json, status

    async def post(self, url: str, data: dict, additional_headers: dict = {}):
        headers = self.__join_headers(additional_headers)

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                json = await response.json()
                status = response.status

                return json, status 

    async def put(self):
        print('put')

    async def delete(self):
        print('delete')