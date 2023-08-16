import aiohttp


default_headers = {
    'Content-Type': 'application/json',
    'Accept': '*/*'
}

def join_headers(additional_headers):
    return {**default_headers, **additional_headers}

async def get(url: str, additional_headers: dict = {}):
    headers = join_headers(additional_headers)

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            json = await response.json()
            status = response.status

            return json, status

async def post(url: str, data: dict, additional_headers: dict = {}):
    headers = join_headers(additional_headers)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            json = await response.json()
            status = response.status

            return json, status 

async def put():
    print('put')

async def delete():
    print('delete')