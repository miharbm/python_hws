import asyncio
import aiohttp
import aiofiles
import os
import argparse
from pathlib import Path


BASE_URL = "https://picsum.photos/400/400"


async def download_image(session: aiohttp.ClientSession, idx: int, output_dir: Path):

    url = f"{BASE_URL}?random={idx}"

    async with session.get(url) as response:
        response.raise_for_status()
        content = await response.read()

    file_path = output_dir / f"image_{idx}.jpg"
    async with aiofiles.open(file_path, "wb") as f:
        await f.write(content)

    print(f"Downloaded: {file_path}")


async def main(count: int, output_dir: str):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timeout = aiohttp.ClientTimeout(total=30)
    connector = aiohttp.TCPConnector(limit=20)

    async with aiohttp.ClientSession(
        timeout=timeout,
        connector=connector
    ) as session:
        tasks = [
            download_image(session, i, output_path)
            for i in range(count)
        ]

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async image downloader (picsum.photos)")
    parser.add_argument("--count", type=int, required=True, help="Number of images to download")
    parser.add_argument("--output", type=str, default="images", help="Output directory")

    args = parser.parse_args()

    asyncio.run(main(args.count, args.output))
