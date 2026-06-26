import os

from dotenv import load_dotenv
from convex import ConvexClient

load_dotenv()

client = ConvexClient(os.getenv("CONVEX_URL"))


def save_analysis(image_name, result):

    if "items" not in result:
        return

    client.mutation(
        "analyses:saveAnalysis",
        {
            "imageName": image_name,
            "totalGarments": result.get(
                "total_garments",
                0
            ),
            "items": result.get(
                "items",
                []
            )
        }
    ) 