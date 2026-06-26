import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const saveAnalysis = mutation({

    args: {

        imageName: v.string(),

        totalGarments: v.number(),

        items: v.array(
            v.object({
                type: v.string(),
                fabric: v.string(),
                color: v.string(),
                confidence: v.number()
            })
        )

    },

    handler: async (ctx, args) => {

        await ctx.db.insert(
            "analyses",
            {

                imageName: args.imageName,

                totalGarments: args.totalGarments,

                items: args.items,

                createdAt: Date.now()

            }
        );

    }

}); 